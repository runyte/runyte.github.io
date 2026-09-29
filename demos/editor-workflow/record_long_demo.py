#!/usr/bin/env python3
"""Append a real 20-second gruvbox scene to the saved matrix demo."""
import argparse
import getpass
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def command(text, wait=.3):
    return {'op': 'command', 'text': text, 'interval': 0, 'wait': wait}


def frame_hashes(path, frames):
    data = subprocess.check_output([
        'ffmpeg', '-v', 'error', '-nostdin', '-i', str(path), '-map', '0:v:0',
        '-frames:v', str(frames), '-f', 'framemd5', '-',
    ], text=True)
    return [line.split(',')[-1].strip() for line in data.splitlines()
            if line and not line.startswith('#')]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skills-root', type=Path, required=True)
    parser.add_argument('--binary', type=Path, required=True)
    parser.add_argument('--font-dir', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--intro', type=Path, default=HERE / 'runyte-editor-demo.mp4')
    args = parser.parse_args()
    output = args.output_dir.resolve()
    if output == REPO or REPO in output.parents:
        parser.error('Record outside the repository, then copy the reviewed final MP4.')
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        parser.error('Use a new, empty output directory.')
    if not shutil.which('htop'):
        parser.error('Install htop before recording this scene.')
    intro = args.intro.resolve()
    intro_record = json.loads((HERE / 'reviewed-take.json').read_text())
    if hashlib.sha256(intro.read_bytes()).hexdigest() != intro_record['video_sha256']:
        parser.error('The intro must match the saved, reviewed 20-second take.')
    spec = importlib.util.spec_from_file_location(
        'record', args.skills_root / 'runyte-demo-videos/scripts/record.py')
    recorder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(recorder)
    continuation = recorder.recipe_from(json.loads((HERE / 'long-recipe.json').read_text()))
    opening = recorder.recipe_from(json.loads((HERE / 'recipe.json').read_text()))
    binary = str(args.binary.resolve())
    version = subprocess.check_output([binary, '--version'], text=True).strip()
    binary_hash = hashlib.sha256(Path(binary).read_bytes()).hexdigest()
    previous = dict(os.environ)
    with tempfile.TemporaryDirectory(prefix='runyte-long-') as directory, \
            tempfile.TemporaryDirectory(prefix='rxl-') as settings:
        root = Path(directory)
        runtime = Path(settings) / 'runtime'
        config = Path(settings) / 'config.yaml'
        config.write_text('theme: matrix\nlsp:\n  enable: false\n')
        env = recorder.capture_driver.isolated_env(runtime)
        env.update(SHELL='/bin/sh', ENV='/dev/null', PS1='$ ', HISTFILE='/dev/null',
                   GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
        # htop uses real counters and its own PID. Omit the username column,
        # personal config, and per-CPU meters that would crowd the small pane.
        htop_config = Path(settings) / 'htoprc'
        htop_config.write_text(
            'htop_version=3.4.1\nconfig_reader_min_version=3\n'
            'fields=0 18 38 39 2 46 47 49 1\n'
            'screen:Main=PID PERCENT_CPU PERCENT_MEM M_RESIDENT TIME Command\n'
            '.sort_key=PERCENT_CPU\n.sort_direction=-1\n.tree_view=0\n'
            'hide_kernel_threads=1\nhide_userland_threads=1\n'
            'show_program_path=0\nshow_cpu_usage=1\nshow_cpu_frequency=0\n'
            'color_scheme=0\ndelay=5\nheader_layout=two_50_50\n'
            'column_meters_0=CPU Memory Swap\ncolumn_meter_modes_0=1 1 1\n'
            'column_meters_1=Tasks LoadAverage Uptime\ncolumn_meter_modes_1=2 2 2\n')
        env['HTOPRC'] = str(htop_config)
        os.environ.clear()
        os.environ.update(env)
        hosts = []
        try:
            for name in ('Release', 'Workbench'):
                workspace = root / name.lower()
                shutil.copytree(HERE / 'fixture', workspace)
                (workspace / 'docs/launch.md').write_bytes((HERE / 'launch.md').read_bytes())
                (workspace / '.gitignore').write_text('.runyte/\n__pycache__/\n')
                git = ['git', '-c', 'user.name=Demo', '-c', 'user.email=demo@example.com',
                       '-c', 'commit.gpgsign=false', '-c', 'core.hooksPath=/dev/null']
                for operation in (['init', '-q', '-b', 'main'], ['add', '.'],
                                  ['commit', '-qm', 'Prepare release checklist']):
                    subprocess.run(git + operation, cwd=workspace, env=env, check=True)
                if name == 'Workbench':
                    source = workspace / 'src/tasks.py'
                    source.write_text(source.read_text().replace('pending', 'ready'))
                host = subprocess.Popen([binary, '-c', str(config), '--serve'],
                                        cwd=workspace, env=env, stdout=subprocess.DEVNULL,
                                        stderr=subprocess.PIPE)
                hosts.append((workspace, host))
                deadline = time.monotonic() + 15
                while True:
                    listing = subprocess.run([binary, '-c', str(config), '--session-list'],
                                             env=env, capture_output=True, text=True)
                    ready = any(str(workspace) in row and 'running' in row
                                for row in listing.stdout.splitlines())
                    renamed = subprocess.run([
                        binary, '-c', str(config), '--session-rename', str(workspace), name,
                    ], env=env, capture_output=True, text=True)
                    if ready and renamed.returncode == 0:
                        break
                    if host.poll() is not None or time.monotonic() > deadline:
                        detail = host.stderr.read().decode() if host.poll() is not None else 'readiness timeout'
                        raise RuntimeError('Demo session did not become ready: ' + renamed.stderr + detail)
                    time.sleep(.1)
            # Reconstruct the previous ending before recording. The actual
            # first half is copied from the approved MP4, never re-created.
            setup = [command('session-attach ../workbench', .7), command('theme gruvbox'),
                     command('open src/tasks.py'), command('session-attach ../release', .7),
                     command('theme matrix')]
            setup += opening['setup'] + opening['actions'] + continuation['setup']
            recipe = {'setup': setup, 'actions': continuation['actions']}
            recipe_path = output / 'full-setup.recipe.json'
            recipe_path.write_text(json.dumps(recipe, indent=2) + '\n')
            raw = output / 'continuation-raw.mp4'
            fonts = args.font_dir
            options = recorder.parser().parse_args([
                '--binary', binary, '--cwd', str(root / 'release'), '--config', str(config),
                '--state-dir', str(runtime), '--arg=--persistent', '--theme', 'matrix',
                '--font', str(fonts / 'JetBrainsMonoNerdFont-Medium.ttf'),
                '--bold-font', str(fonts / 'JetBrainsMonoNerdFontMono-Bold.ttf'),
                '--italic-font', str(fonts / 'JetBrainsMonoNerdFont-MediumItalic.ttf'),
                '--bold-italic-font', str(fonts / 'JetBrainsMonoNerdFontMono-BoldItalic.ttf'),
                '--steps', str(recipe_path), '--output', str(raw),
                '--opening-hold', '0', '--closing-hold', '1',
                '--label', f'{version}; binary sha256 {binary_hash}; matrix to gruvbox; 40-second continuation',
            ])
            def scene(capture, play):
                started = time.monotonic()
                try:
                    for action in recipe['actions']:
                        play(action)
                        if action['op'] == 'checkpoint':
                            screen = capture.text()
                            if str(Path.home()) in screen or re.search(r'(?i)claude|codex|openai|anthropic', screen):
                                raise RuntimeError('Unexpected personal path or excluded product text')
                            if re.search(r'\b' + re.escape(getpass.getuser()) + r'\b', screen):
                                raise RuntimeError('Personal username in capture')
                            if action['name'] == 'Four live panes':
                                # Verify each quadrant, not just matches anywhere.
                                rows = screen.splitlines()
                                quadrants = {
                                    'file': '\n'.join(row[:100] for row in rows[:24]),
                                    'help': '\n'.join(row[100:] for row in rows[:24]),
                                    'terminal': '\n'.join(row[:100] for row in rows[24:48]),
                                    'explorer': '\n'.join(row[100:] for row in rows[24:48]),
                                }
                                for quadrant, marker in [('file', 'ready_tasks'), ('help', '[help]'),
                                                         ('terminal', 'htop'), ('explorer', '[explorer]')]:
                                    if marker not in quadrants[quadrant]:
                                        raise RuntimeError(f'Missing {marker} in {quadrant} quadrant')
                            slug = action['name'].lower().replace(' ', '-')
                            (output / f'{slug}.txt').write_text(screen)
                            print('CHECKPOINT', action['name'], flush=True)
                    if time.monotonic() - started > 18.5:
                        raise RuntimeError('Continuation actions exceeded 18.5 seconds.')
                    # Keep htop genuinely updating during the final reading hold.
                    play({'op': 'wait', 'wait': max(0, 19 - (time.monotonic() - started))})
                except BaseException:
                    (output / 'failure.txt').write_text(capture.text())
                    capture.render_image().save(output / 'failure.png')
                    raise
            print(json.dumps(recorder.record(options, recipe, playback=scene)), flush=True)
        finally:
            for workspace, host in hosts:
                try:
                    subprocess.run([binary, '-c', str(config), '--session-stop', str(workspace), '--force'],
                                   env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15)
                except subprocess.TimeoutExpired:
                    host.terminate()
                try:
                    host.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    host.kill()
                    host.wait()
            os.environ.clear()
            os.environ.update(previous)
    metadata = json.loads(raw.with_suffix('.recording.json').read_text())
    if max(e['end'] for e in metadata['timeline'] if 'name' in e) > 18.5:
        raise RuntimeError('Continuation exceeded 18.5 seconds; shorten pauses and record again.')
    # Trim/pad only the ending, keeping real htop updates throughout the raw take.
    second = output / 'continuation.mp4'
    subprocess.run([
        'ffmpeg', '-v', 'error', '-nostdin', '-y', '-i', str(raw),
        '-vf', 'tpad=stop_mode=clone:stop_duration=20', '-frames:v', '300',
        '-an', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p',
        '-movflags', '+faststart', str(second),
    ], check=True)
    shutil.copyfile(intro, output / 'intro.mp4')
    concat = output / 'concat.txt'
    concat.write_text("file 'intro.mp4'\nfile 'continuation.mp4'\n")
    final = output / 'runyte-editor-demo-40s.mp4'
    subprocess.run([
        'ffmpeg', '-v', 'error', '-nostdin', '-y', '-f', 'concat', '-safe', '1',
        '-i', str(concat), '-map', '0:v:0', '-c', 'copy', '-movflags', '+faststart', str(final),
    ], check=True)
    probe = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0',
        '-show_entries', 'stream=codec_name,width,height,r_frame_rate,nb_read_frames:format=duration',
        '-of', 'json', str(final),
    ], text=True))
    stream = probe['streams'][0]
    assert float(probe['format']['duration']) == 40, probe
    assert stream['nb_read_frames'] == '600' and stream['r_frame_rate'] == '15/1', probe
    assert (stream['width'], stream['height']) == (2400, 1300), probe
    assert frame_hashes(final, 300) == frame_hashes(intro, 300), 'The intro frames changed'
    for entry in metadata['timeline']:
        if 'name' in entry:
            slug = entry['name'].lower().replace(' ', '-')
            subprocess.run([
                'ffmpeg', '-v', 'error', '-nostdin', '-y',
                '-ss', str(20 + max(0, entry['start'] - .15)), '-i', str(final),
                '-frames:v', '1', str(output / f'{slug}.png'),
            ], check=True)
    provenance = {
        'version': version, 'binary_sha256': binary_hash, 'source_revision': None,
        'theme': 'matrix (0–20s), gruvbox (second half, after visible theme switch)',
        'font': 'JetBrainsMono Nerd Font Medium', 'geometry': '200x50',
        'probe': probe, 'intro_video_sha256': intro_record['video_sha256'],
        'intro_frames_verified_identical': 300,
        'video_sha256': hashlib.sha256(final.read_bytes()).hexdigest(),
        'recipe_sha256': hashlib.sha256((HERE / 'long-recipe.json').read_bytes()).hexdigest(),
        'checkpoint_seconds': {e['name']: round(20 + e['end'], 3)
                               for e in metadata['timeline'] if 'name' in e},
        'htop_version': subprocess.check_output(['htop', '--version'], text=True).strip(),
        'timing': 'Original first 300 frames; continuation at recorded speed; final hold fills 40 seconds.',
    }
    (output / 'provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
    print(json.dumps({'video': str(final), 'duration': 40, 'frames': 600}), flush=True)


if __name__ == '__main__':
    main()
