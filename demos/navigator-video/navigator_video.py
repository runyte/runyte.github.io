#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""Record the Navigator video: Claude Code on the left, your own work on the right.

Three acts, one theme each: ocean-dark, gruvbox, matrix. `edit_video.py` cuts
the service waits and fits every act to exactly twenty seconds.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, str(Path(__file__).parent))
import scene  # noqa: E402

LEFT = slice(1, 99)
RIGHT = slice(101, 199)
PROMPT_FILE = 'prompt.md'
# Claude Code screen text the scene waits for. Adjust if Claude Code changes it.
CLAUDE_BUSY = 'esc to interrupt'
CLAUDE_READY = ('? for shortcuts', 'Try "')
CLAUDE_TRUST = 'trust the files'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--skills-root', type=Path, required=True)
    p.add_argument('--binary', type=Path, required=True)
    p.add_argument('--font-dir', type=Path, required=True)
    p.add_argument('--workspace', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--stand-in', action='store_true',
                   help='Rehearse every Runyte step with a shell in place of Claude Code; never publish this take')
    args = p.parse_args()
    spec = importlib.util.spec_from_file_location('record', args.skills_root/'runyte-demo-videos/scripts/record.py')
    record = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(record)
    workspace = args.workspace.resolve()
    scene.prepare(workspace)
    prompt = Path(__file__).with_name(PROMPT_FILE).read_text()
    binary = str(args.binary.resolve())
    version = subprocess.check_output([binary, '--version'], text=True).strip()
    private = [] if args.stand_in else scene.private_markers()
    if not args.stand_in and not shutil.which('claude'):
        raise SystemExit('Claude Code (claude) is not on PATH.')
    settings = Path(tempfile.mkdtemp(prefix='rnv-'))
    try:
        config = settings/'config.yaml'
        config.write_text('theme: ocean-dark\nlsp:\n  enable: false\n')
        if not args.stand_in:
            scene.claude_home(settings, workspace)
        runtime = settings/'runtime'
        env = record.capture_driver.isolated_env(runtime)
        for key in [k for k in env if k.startswith(('CLAUDE', 'ANTHROPIC'))]:
            del env[key]
        env.update(scene.child_env(settings, binary))
        # The capture client derives its environment from this process.
        previous = dict(os.environ)
        os.environ.clear()
        os.environ.update(env)
        fonts = args.font_dir
        opts = record.parser().parse_args([
            '--binary', binary, '--cwd', str(workspace), '--config', str(config),
            '--state-dir', str(runtime), '--arg=--persistent',
            '--font', str(fonts/'JetBrainsMonoNerdFont-Medium.ttf'),
            '--bold-font', str(fonts/'JetBrainsMonoNerdFontMono-Bold.ttf'),
            '--italic-font', str(fonts/'JetBrainsMonoNerdFont-MediumItalic.ttf'),
            '--bold-italic-font', str(fonts/'JetBrainsMonoNerdFontMono-BoldItalic.ttf'),
            '--steps', str(Path(__file__).with_name(PROMPT_FILE)), '--output', str(args.output),
            '--max-duration', '600', '--opening-hold', '1', '--closing-hold', '2',
            '--label', version + ('; STAND-IN rehearsal' if args.stand_in else '; live Claude Code')
            + '; ocean-dark, gruvbox, matrix; Navigator video; 200 columns x 50 rows'])
        host = subprocess.Popen([binary, '-c', str(config), '--serve'], cwd=workspace, env=env,
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        def scene_controller(c, play):
            def do(op, **kw): play({'op': op, **kw})
            def key(s, wait=.2): do('key', text=s, wait=wait)
            def type_(s, interval=.06, wait=.2): do('type', text=s, interval=interval, wait=wait)
            def command(s, wait=.3, interval=.04): do('command', text=s, wait=wait, interval=interval)
            def rows(): return c.text().splitlines()
            def left(): return [r[LEFT] for r in rows()[1:48]]
            def guard():
                screen = c.text().lower()
                if any(word.lower() in screen for word in private):
                    raise RuntimeError('Account details appeared on screen; recording stopped')
            def check(name, required=(), wait=.1):
                guard()
                do('checkpoint', name=name, required=list(required), wait=wait)
                print('CHECKPOINT', name, flush=True)
                slug = re.sub('[^a-z0-9]+', '-', name.lower()).strip('-')
                c.render_image().save(args.output.with_name(f'{args.output.stem}-{slug}.png'))
            def until(ready, timeout=120, step=.3):
                end = time.monotonic() + timeout
                while not ready():
                    guard()
                    if time.monotonic() > end:
                        raise RuntimeError('readiness timeout')
                    do('wait', wait=step)
            def theme(act, filter_text):
                # The picker previews a theme once the filter matches it, so the
                # act begins as the picker opens and the colours change just after.
                key(' ot', .4)
                check(act, ['theme'], wait=.3)
                type_(filter_text, interval=.09, wait=.6)
                key('\r', .4)

            try:
                # Act 1 (ocean-dark): start Claude Code and hand it a task.
                check('Act 1', ['Runyte'], wait=1.8)
                key('\x17v', .5)
                key('\x17h', .3)
                key(' tn', .8)
                if args.stand_in:
                    type_('echo stand-in for Claude Code', interval=.03, wait=.1)
                else:
                    type_('claude', interval=.08, wait=.1)
                key('\r', .1)
                check('Claude startup begins', wait=0)
                if args.stand_in:
                    do('wait', wait=1)
                else:
                    def claude_ready():
                        text = '\n'.join(left())
                        if CLAUDE_TRUST in text:
                            key('\r', .5)
                            return False
                        return any(marker in text for marker in CLAUDE_READY)
                    until(claude_ready, 90)
                    do('wait', wait=1)
                key('\x1c', .2)
                command('terminal-rename claude', interval=0, wait=.2)
                key('i', .2)
                check('Claude ready', wait=.3)
                if args.stand_in:
                    # What Claude Code's Ctrl-g does: open $VISUAL on its prompt file.
                    # Named like Claude Code's own prompt file, whose long name affects layout.
                    name = '../claude-prompt-0b9c1e44-7a52-4f0e-9d3b-5c8e2a61f7d0.md'
                    type_(f': > {name}; $VISUAL {name}\r', interval=0, wait=.1)
                else:
                    key('\x07', .1)
                until(lambda: '[file]' in rows()[0] and '.md' in rows()[0][:100], 30)
                do('wait', wait=.3)
                check('Prompt editor open', wait=.2)
                key('i', .15)
                do('paste', text=prompt, wait=.4)
                key('\x1b', .2)
                key('gg', .3)
                check('Prompt pasted', ['Store::complete'], wait=.8)
                key('?', .5)
                check('Prompt rendered', ['[rendered'], wait=2.2)
                # Close the rendered view rather than toggling back: a leftover
                # [rendered claude-prompt-<id>.md] row is wide enough to push the
                # Navigator's NAME column off screen.
                key(' bc', .5)
                check('Prompt source again', ['Store::complete'], wait=.2)
                command('wbc', wait=.6)
                check('Prompt returned to Claude', wait=.3)
                if args.stand_in:
                    # Stand-in for Claude's work: edit later, then reply in one line.
                    type_("(sleep 20; sed -i 's/^}$/\\n    pub fn complete(\\&mut self, title: \\&str) {}\\n}/' src/store.rs;"
                          " echo 'Added Store::complete and its test in src/store.rs.') &\r", interval=0, wait=.3)
                else:
                    key('\r', .3)
                check('Task submitted', wait=1.5)
                if not args.stand_in and not any(CLAUDE_BUSY in r for r in left()):
                    raise RuntimeError('Claude finished before it could be hidden; record another take')
                key('\x1c', .2)
                theme('Act 2', 'gruv')
                # Act 2 (gruvbox): hide Claude behind README.md, then work in the right pane.
                key(' n', .5)
                type_('readme', interval=.1, wait=.4)
                key('\r', .5)
                check('Claude hidden', ['README.md'], wait=.6)
                key('\x17l', .3)
                key(' e', .8)
                check('Explorer', ['[explorer]', 'notes.md', 'scratch.txt'], wait=.6)
                key('/notes\r', .3)
                key('gh', .1)
                key('i', .1)
                type_('docs/', interval=.08, wait=.1)
                key('\x1b', .3)
                key('o', .1)
                type_('CHANGELOG.md', interval=.06, wait=.1)
                key('\x1b', .3)
                key('/scratch\r', .3)
                key('x', .2)
                key('c', .1)
                key('\x1b', .5)
                check('Explorer edited', ['docs/notes.md', 'CHANGELOG.md'], wait=.3)
                command('w', wait=.4)
                check('Filesystem plan', ['Filesystem plan', 'move notes.md', 'delete scratch.txt'], wait=2.2)
                key('\r', .6)
                if not (workspace/'docs/notes.md').is_file() or (workspace/'scratch.txt').exists():
                    raise RuntimeError('filesystem plan was not applied')
                check('Plan applied', wait=.6)
                key('\tt', .8)
                key('\x1c', .2)
                command('terminal-rename tests', interval=0, wait=.2)
                key('i', .2)
                type_('cargo test\r', interval=.06, wait=.2)
                until(lambda: any('test result' in r[RIGHT] for r in rows()), 60)
                check('Tests ran', ['test result'], wait=1.5)
                key('\x1c', .2)
                theme('Act 3', 'matr')
                # Act 3 (matrix): switch with the Navigator; notice when Claude is done.
                key(' n', .6)
                check('Navigator', ['Navigator', 'claude', 'tests', '[explorer]', 'README.md'], wait=1.4)
                type_('main', interval=.1, wait=.4)
                key('\r', .5)
                key('\x17h', .4)
                check('Claude wait begins', wait=0)
                def claude_done():
                    # Filter to Claude's row so the preview shows its live screen.
                    key(' n', .5)
                    type_('claude', interval=0, wait=.6)
                    done = any('[terminal]' in r and 'unread' in r for r in rows())
                    if done and not args.stand_in:
                        done = ('fn complete' in (workspace/'src/store.rs').read_text()
                                and not any(CLAUDE_BUSY in r for r in rows()))
                    key('\x1b', .3)
                    return done
                until(claude_done, 300, 1.5)
                check('Claude finished', wait=0)
                key(' n', .6)
                check('Claude unread', ['claude', 'unread'], wait=2.2)
                type_('claude', interval=.08, wait=.4)
                key('\r', .6)
                # Terminal Insert -> terminal Normal -> review, where gf follows paths.
                key('\x1c', .2)
                key('\x1c', .4)
                check('Claude answer', ['src/store.rs', '[review]'], wait=1.2)
                visible = rows()
                hits = [(y, r.rindex('src/store.rs', 1, 99)) for y, r in enumerate(visible[1:48], 1)
                        if 'src/store.rs' in r[LEFT] and '|' not in r[LEFT] and '│ >' not in r[LEFT]]
                if not hits:
                    raise RuntimeError('the reply does not show src/store.rs')
                y, x = hits[-1]
                # Select exactly the path, so sentence punctuation is not part of it.
                do('mouse', x=x + 1, y=y + 1, wait=.1)
                do('mouse', x=x + 1, y=y + 1, release=True, wait=.2)
                key('v' + str(len('src/store.rs') - 1) + 'l', .5)
                key('gf', .6)
                key('\x1b', .3)
                check('Opened changed file', ['store.rs', 'fn complete'], wait=2)
                key(' n', .6)
                check('Final Navigator', ['Navigator'], wait=2.5)
            except BaseException:
                args.output.with_suffix('.failure.txt').write_text(c.text())
                c.render_image().save(args.output.with_suffix('.failure.png'))
                raise

        try:
            recipe = {'setup': [
                {'op': 'expect', 'text': 'Runyte'},
                {'op': 'command', 'text': 'open src/main.rs', 'interval': 0, 'wait': .3},
                {'op': 'command', 'text': 'open README.md', 'interval': 0, 'wait': .3},
                {'op': 'command', 'text': 'git-refresh', 'interval': 0, 'wait': .5},
                {'op': 'command', 'text': 'about', 'interval': 0, 'wait': .3},
            ], 'actions': [{'op': 'wait', 'wait': 0}]}
            result = record.record(opts, recipe, playback=scene_controller)
            print(json.dumps(result), flush=True)
        finally:
            subprocess.run([binary, '-c', str(config), '--session-stop', str(workspace), '--force'],
                           env=env, capture_output=True, timeout=15)
            try:
                host.wait(timeout=10)
            except subprocess.TimeoutExpired:
                host.terminate()
                try:
                    host.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    host.kill()
                    host.wait()
            os.environ.clear()
            os.environ.update(previous)
    finally:
        # Claude Code may still write its session file while it exits; the
        # copied login must not outlive the take.
        for _ in range(20):
            shutil.rmtree(settings, ignore_errors=True)
            if not settings.exists():
                break
            time.sleep(.5)
        else:
            raise RuntimeError(f'could not remove temporary settings: {settings}')


if __name__ == '__main__':
    main()
