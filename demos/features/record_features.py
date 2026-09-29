#!/usr/bin/env python3
"""Record isolated, real Runyte feature clips. Outputs and sidecars stay temporary."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile

ESC = '\x1b'
TASKS = '''"""A tiny release checklist."""


def pending_tasks(tasks):
    pending = [task for task in tasks if not task["done"]]
    return sorted(pending, key=lambda task: task["priority"])


def summarize(tasks):
    pending = pending_tasks(tasks)
    return f"{len(pending)} tasks left before release"


tasks = [
    {"title": "Write release notes", "done": False, "priority": 1},
    {"title": "Run the tests", "done": False, "priority": 2},
    {"title": "Publish the package", "done": True, "priority": 3},
]

print(summarize(tasks))
'''
README = '''# Release checklist

A small project for a focused afternoon.

## Files

- src/tasks.py: sort the work that remains.
- docs/release.md: the release plan.
- notes.md: notes to organize.

## Before shipping

1. Write release notes.
2. Run the tests.
3. Publish the package.
'''
MARKDOWN = '''# Release plan

Small steps, clear priorities.

## Tasks

| Task | Owner | Status | Next step |
| --- | --- | --- | --- |
| Write release notes | Mira | In progress | Explain the new search workflow |
| Run the tests | Leon | Ready | Check all supported platforms |
| Update examples | Noor | Done | Keep the examples short and useful |
| Publish the package | Mira | Waiting | Finish the review first |

## Checklist

- Review the changes.
- Update the examples.
- Run the tests.
- Publish the package.

**One task at a time.** Keep the release small.
'''


def key(text, wait=.5): return {'op': 'key', 'text': text, 'wait': wait}
def type_(text, wait=.4): return {'op': 'type', 'text': text, 'interval': .12, 'wait': wait}
def command(text, wait=.5): return {'op': 'command', 'text': text, 'interval': .06, 'wait': wait}
def hold(seconds): return {'op': 'wait', 'wait': seconds}
def check(name, *required): return {'op': 'checkpoint', 'name': name, 'required': list(required), 'wait': .3}
def opened(path): return [command('open ' + path), {'op':'expect', 'text':path}]


def recipe(name):
    if name == 'directory-tree':
        return 'ocean-dark', opened('src/tasks.py'), [
            key(' dd', 1.4), check('Reveal active file', '[dir tree]', 'tasks.py'),
            key('k', .5), key('\r', 1.4), check('Open neighboring file', 'RELEASE_NAME'),
            key(' dt', 1.1), check('Tree hidden', 'RELEASE_NAME'),
            key(' dt', 1.3), check('Tree restored', '[dir tree]', 'config.py'),
        ]
    if name == 'modal-editing':
        return 'gruvbox', opened('src/tasks.py'), [
            key('s'), type_('pending'), key('\r', 2), check('All matches selected', 'pending'),
            key('c'), type_('ready', 1), key(ESC, 1.5), check('All matches changed', 'ready_tasks'),
            key('u', 1.8), check('Undo together', 'pending_tasks'),
            key('U', 1.8), key('\x13', .5), check('Redo and save', 'ready_tasks'),
        ]
    if name == 'key-hints':
        return 'ocean-dark', opened('src/tasks.py'), [
            key(' ', 2.5), check('Discover next keys'), key('g', 2.5), check('Discover Git actions'),
            key(ESC), key(' ?', 2), check('Contextual help'), hold(3), key(ESC, 1),
        ]
    if name == 'markdown':
        return 'nordbones-dark-soft', opened('docs/release.md'), [
            hold(1.5), key('?', 1), check('Rendered table', '[rendered', 'Release plan'), hold(3),
            key('?', 1.5), check('Back to source', '| Task |'),
            key('?', 1), check('Read the page', '[rendered'), hold(2),
        ]
    if name == 'file-management':
        return 'gruvbox', [key(' e', .8), check('Explorer ready', 'notes.md', 'scratch.txt')], [
            key('/notes\r'), key('gh', .2), key('i', .2), type_('docs/'), key(ESC),
            key('o', .2), type_('CHANGELOG.md'), key(ESC),
            key('/scratch\r'), key('x', .2), key('c', .2), key(ESC, 1),
            command('w'), check('Review filesystem plan', 'Filesystem plan', 'move notes.md', 'delete scratch.txt'),
            hold(2), key('\r', 1), check('Changes applied', 'CHANGELOG.md'), hold(2),
        ]
    if name == 'git':
        return 'rosebones-dark', opened('src/tasks.py'), [
            key(' gD', 1), check('Compare changes', 'pending_tasks', 'ready_tasks'), hold(3),
            command('diff-off', 1), key(' gg', 1), check('Changed files', 'src/tasks.py'),
            key('\ts', 1.5), check('Stage the change', 'staged'), hold(2),
        ]
    terminal = [key('\x17t', .7), type_("python3 src/tasks.py", .2),
                key('\r', .7), key('\x1c'), command('terminal-rename output')]
    if name == 'navigator':
        setup = opened('docs/release.md') + opened('src/tasks.py') + terminal + opened('README.md')
        return 'matrix', setup, [
            key(' n', 1), check('Buffers and terminal', 'Navigator', 'output', 'src/tasks.py'), hold(2),
            type_('tasks', 1), key('\r', 1.5), check('Visit file', 'pending_tasks'),
            key(' n'), type_('output', 1), key('\r', 1.5), check('Visit terminal', '2 tasks left before release'),
            key('\x1c'), key(' n', 1), check('Return to Navigator', 'Navigator'), hold(2),
        ]
    if name == 'finder':
        setup = terminal + opened('README.md')
        return 'everforest-dark-medium', setup, [
            key(' f'), type_('release', 1.5), check('Find a file', 'docs/release.md'),
            key('\t', 1.5), check('Search content', 'Contents', 'output'),
            key('\x1b[B', 1.5), key('\x1b[B', 1.5), check('Preview another match'), hold(2),
        ]
    raise ValueError(name)


NAMES = ('modal-editing', 'key-hints', 'markdown', 'finder', 'navigator', 'file-management', 'git', 'directory-tree')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('name', choices=NAMES)
    parser.add_argument('--skills-root', required=True, type=Path)
    parser.add_argument('--binary', required=True, type=Path)
    parser.add_argument('--font-dir', required=True, type=Path)
    parser.add_argument('--output-dir', required=True, type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    spec = importlib.util.spec_from_file_location('record', args.skills_root / 'runyte-demo-videos/scripts/record.py')
    recorder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(recorder)
    binary = args.binary.resolve()
    version = subprocess.check_output([str(binary), '--version'], text=True).strip()
    digest = hashlib.sha256(binary.read_bytes()).hexdigest()
    # A plain POSIX shell uses no personal interactive startup files.
    os.environ.update({'SHELL':'/bin/sh', 'ENV':'/dev/null', 'PS1':'$ ', 'HISTFILE':'/dev/null',
                       'GIT_CONFIG_GLOBAL':'/dev/null', 'GIT_CONFIG_NOSYSTEM':'1'})
    with tempfile.TemporaryDirectory(prefix='runyte-feature-') as directory:
        workspace = Path(directory) / 'release'
        (workspace / 'src').mkdir(parents=True)
        (workspace / 'docs').mkdir()
        files = {'README.md':README, 'src/tasks.py':TASKS, 'docs/release.md':MARKDOWN,
                 'notes.md':'# Notes\n\nKeep the release small.\n', 'scratch.txt':'Temporary notes.\n', '.gitignore':'.runyte/\n'}
        if args.name == 'directory-tree':
            files['src/config.py'] = ('"""Release settings."""\n\n'
                'RELEASE_NAME = "Autumn update"\n'
                'CHECKS = ["tests", "docs", "package"]\n'
                'REQUIRE_REVIEW = True\n')
        for name, text in files.items(): (workspace / name).write_text(text)
        def git(*parts):
            return subprocess.check_output(['git','-c','user.name=Demo','-c','user.email=demo@example.com',
                '-c','commit.gpgsign=false','-c','core.hooksPath=/dev/null',*parts], cwd=workspace, text=True)
        git('init','-q','-b','main')
        git('add','.')
        git('commit','-qm','Prepare a release checklist')
        if args.name == 'git':
            (workspace / 'src/tasks.py').write_text(TASKS.replace('pending', 'ready'))
        theme, setup, actions = recipe(args.name)
        data = {'setup':setup, 'actions':actions}
        output = args.output_dir / (args.name + '.mp4')
        recipe_path = args.output_dir / (args.name + '.recipe.json')
        recipe_path.write_text(json.dumps(data, indent=2) + '\n')
        fonts = args.font_dir
        options = recorder.parser().parse_args([
            '--binary',str(binary),'--cwd',str(workspace),'--arg=--standalone',
            '--font',str(fonts/'JetBrainsMonoNerdFont-Medium.ttf'),
            '--bold-font',str(fonts/'JetBrainsMonoNerdFontMono-Bold.ttf'),
            '--italic-font',str(fonts/'JetBrainsMonoNerdFont-MediumItalic.ttf'),
            '--bold-italic-font',str(fonts/'JetBrainsMonoNerdFontMono-BoldItalic.ttf'),
            '--theme',theme,'--steps',str(recipe_path),'--output',str(output),
            '--label',f'{version}; binary sha256 {digest}; {args.name}; {theme}',
        ])
        def play_scene(capture, play):
            try:
                for action in actions:
                    play(action)
                    if action['op'] == 'checkpoint':
                        if str(Path.home()) in capture.text():
                            raise RuntimeError('Personal path or prompt in capture')
                        if args.name == 'directory-tree' and action['name'] == 'Tree hidden':
                            assert '[dir tree]' not in capture.text()
                        slug = action['name'].lower().replace(' ', '-')
                        capture.render_image().save(args.output_dir / f'{args.name}-{slug}.png')
            except BaseException:
                capture.render_image().save(args.output_dir / f'{args.name}-failure.png')
                (args.output_dir / f'{args.name}-failure.txt').write_text(capture.text())
                raise
        print(json.dumps(recorder.record(options, data, playback=play_scene)), flush=True)
        if args.name == 'directory-tree':
            timing = json.loads(output.with_suffix('.recording.json').read_text())
            if timing['timeline'][-1]['end'] > 9:
                raise RuntimeError('Actions ran too slowly for a 10-second clip; record again')
            # Keep interaction speed intact; adjust only the final still to 150 frames.
            final = args.output_dir / 'directory-tree-final.mp4'
            subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
                '-i', str(output), '-vf', 'tpad=stop_mode=clone:stop_duration=10',
                '-t', '10', '-an', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p',
                '-movflags', '+faststart', str(final)], check=True)
            final.replace(output)
            subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
                '-ss', '2', '-i', str(output), '-frames:v', '1',
                str(args.output_dir / 'directory-tree-poster.webp')], check=True)
        if args.name == 'file-management':
            assert (workspace/'docs/notes.md').exists() and (workspace/'CHANGELOG.md').exists()
            assert not (workspace/'notes.md').exists() and not (workspace/'scratch.txt').exists()
        if args.name == 'modal-editing':
            assert (workspace/'src/tasks.py').read_text() == TASKS.replace('pending','ready')
        if args.name == 'git':
            assert 'ready_tasks' in git('diff','--cached')
        (args.output_dir / (args.name + '.provenance.json')).write_text(json.dumps({
            'version':version, 'binary_sha256':digest, 'theme':theme,
            'geometry':'200x50', 'font':'JetBrainsMono Nerd Font Medium',
        }, indent=2) + '\n')


if __name__ == '__main__': main()
