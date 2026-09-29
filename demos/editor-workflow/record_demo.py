#!/usr/bin/env python3
"""Record the 20-second editing workflow; keep all media outside this repo."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skills-root', type=Path, required=True)
    parser.add_argument('--binary', type=Path, required=True)
    parser.add_argument('--font-dir', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    output = args.output_dir.resolve()
    if output == REPO or REPO in output.parents:
        parser.error('Choose an output directory outside the repository, such as /tmp/runyte-editor-review.')
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        parser.error('Use a new, empty output directory for each take.')
    spec = importlib.util.spec_from_file_location(
        'record', args.skills_root / 'runyte-demo-videos/scripts/record.py')
    recorder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(recorder)
    recipe = recorder.recipe_from(json.loads((HERE / 'recipe.json').read_text()))
    binary = args.binary.resolve()
    version = subprocess.check_output([str(binary), '--version'], text=True).strip()
    digest = hashlib.sha256(binary.read_bytes()).hexdigest()
    os.environ.update(SHELL='/bin/sh', ENV='/dev/null', PS1='$ ', HISTFILE='/dev/null',
                      GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    checkpoints = []
    with tempfile.TemporaryDirectory(prefix='runyte-edit-') as directory:
        workspace = Path(directory) / 'release'
        workspace.mkdir()
        for source in (HERE / 'fixture').rglob('*'):
            if source.is_file():
                target = workspace / source.relative_to(HERE / 'fixture')
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(source.read_bytes())
        (workspace / '.gitignore').write_text('.runyte/\n__pycache__/\n')
        def git(*parts):
            return subprocess.check_output([
                'git', '-c', 'user.name=Demo', '-c', 'user.email=demo@example.com',
                '-c', 'commit.gpgsign=false', '-c', 'core.hooksPath=/dev/null', *parts,
            ], cwd=workspace, text=True)
        git('init', '-q', '-b', 'main')
        git('add', '.')
        git('commit', '-qm', 'Prepare release checklist')
        raw = output / 'workflow-raw.mp4'
        fonts = args.font_dir
        options = recorder.parser().parse_args([
            '--binary', str(binary), '--cwd', str(workspace), '--arg=--standalone',
            '--font', str(fonts / 'JetBrainsMonoNerdFont-Medium.ttf'),
            '--bold-font', str(fonts / 'JetBrainsMonoNerdFontMono-Bold.ttf'),
            '--italic-font', str(fonts / 'JetBrainsMonoNerdFont-MediumItalic.ttf'),
            '--bold-italic-font', str(fonts / 'JetBrainsMonoNerdFontMono-BoldItalic.ttf'),
            '--theme', 'matrix', '--steps', str(HERE / 'recipe.json'),
            '--output', str(raw), '--opening-hold', '0.5', '--closing-hold', '1',
            '--label', f'{version}; binary sha256 {digest}; editing workflow; matrix',
        ])
        def scene(capture, play):
            try:
                for action in recipe['actions']:
                    play(action)
                    if action['op'] == 'checkpoint':
                        screen = capture.text()
                        if str(Path.home()) in screen or re.search(r'(?i)claude|codex|openai|anthropic', screen):
                            raise RuntimeError('Unexpected personal path or excluded product text')
                        # Check the pane title as well as the source; the sidebar and
                        # picker previews can also contain matching filenames.
                        title = screen.splitlines()[0]
                        expected_title = {
                            'Explorer': '[explorer]',
                            'Explorer opened config': '[file]',
                            'Tree opened tasks': '[file]',
                            'Navigator opened file': '[file]',
                            'Navigator opened history': '[terminal',
                            'Navigator opened checks': '[terminal',
                        }.get(action['name'])
                        if expected_title and expected_title not in title:
                            raise RuntimeError(f'Wrong destination at {action["name"]}: {title}')
                        slug = action['name'].lower().replace(' ', '-')
                        (output / f'{slug}.txt').write_text(screen)
                        checkpoints.append(action['name'])
                        print('CHECKPOINT', action['name'], flush=True)
            except BaseException:
                (output / 'failure.txt').write_text(capture.text())
                capture.render_image().save(output / 'failure.png')
                raise
        print(json.dumps(recorder.record(options, recipe, playback=scene)), flush=True)
        original = (HERE / 'fixture/src/tasks.py').read_text()
        actual = (workspace / 'src/tasks.py').read_text()
        if actual != original.replace('pending', 'ready'):
            raise RuntimeError('The visible multi-selection edit was not saved correctly.')
        result = subprocess.check_output(['python3', 'src/tasks.py'], cwd=workspace, text=True)
        if result.strip() != '2 tasks left before release':
            raise RuntimeError('Edited fixture did not run correctly.')
    metadata = json.loads(raw.with_suffix('.recording.json').read_text())
    # Never cut an interaction to meet the requested duration. Only adjust the
    # ending still, and retain at least a second to read the last Navigator.
    end = metadata['timeline'][-1]['end']
    if end > 19:
        raise RuntimeError(f'Actions took {end:.2f}s; shorten pauses and record a new take.')
    final = output / 'runyte-editor-demo.mp4'
    subprocess.run([
        'ffmpeg', '-hide_banner', '-loglevel', 'error', '-nostdin', '-y',
        '-i', str(raw), '-vf', 'tpad=stop_mode=clone:stop_duration=20',
        '-frames:v', '300', '-an', '-c:v', 'libx264', '-crf', '18',
        '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(final),
    ], check=True)
    probe = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0',
        '-show_entries', 'stream=codec_name,width,height,r_frame_rate,nb_read_frames:format=duration',
        '-of', 'json', str(final),
    ], text=True))
    stream = probe['streams'][0]
    if not (float(probe['format']['duration']) == 20 and stream['nb_read_frames'] == '300'
            and stream['codec_name'] == 'h264' and stream['r_frame_rate'] == '15/1'
            and (stream['width'], stream['height']) == (2400, 1300)):
        raise RuntimeError(f'Unexpected final media properties: {probe}')
    for entry in metadata['timeline']:
        if 'name' in entry:
            slug = entry['name'].lower().replace(' ', '-')
            subprocess.run([
                'ffmpeg', '-hide_banner', '-loglevel', 'error', '-nostdin', '-y',
                # Sample inside the preceding reading pause. At the exact
                # checkpoint boundary the next key may already have painted.
                '-ss', str(max(0, entry['start'] - .15)), '-i', str(final), '-frames:v', '1',
                str(output / f'{slug}.png'),
            ], check=True)
    provenance = {
        'version': version, 'binary_sha256': digest, 'source_revision': None,
        'theme': 'matrix', 'font': 'JetBrainsMono Nerd Font Medium',
        'geometry': '200x50', 'probe': probe, 'checkpoints': checkpoints,
        'timing': 'Original interaction speed; ending still adjusted to exactly 20 seconds.',
        'video_sha256': hashlib.sha256(final.read_bytes()).hexdigest(),
        'recipe_sha256': hashlib.sha256((HERE / 'recipe.json').read_bytes()).hexdigest(),
        'checkpoint_seconds': {entry['name']: round(entry['end'], 3)
                               for entry in metadata['timeline'] if 'name' in entry},
    }
    (output / 'provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
    print(json.dumps({'video': str(final), 'duration': 20, 'frames': 300}), flush=True)


if __name__ == '__main__':
    main()
