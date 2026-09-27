#!/usr/bin/env python3
"""Record session management with two isolated persistent Runyte hosts."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time

from record_features import key, command, type_, hold, check, TASKS

PROJECTS = {
    'API': ('terafox', 'src/tasks.py', TASKS),
    'Website': ('ember-dark', 'style.css', '''/* A quiet home for the release. */
:root {
    --background: #282a2f;
    --foreground: #b9b9be;
    --accent: #c96870;
}

body {
    background: var(--background);
    color: var(--foreground);
    font-family: monospace;
    line-height: 1.6;
}

a {
    color: var(--accent);
}
'''),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skills-root', required=True, type=Path)
    parser.add_argument('--binary', required=True, type=Path)
    parser.add_argument('--font-dir', required=True, type=Path)
    parser.add_argument('--output-dir', required=True, type=Path)
    parser.add_argument('--source-ref', help='Verified source revision of the supplied binary')
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    spec = importlib.util.spec_from_file_location('record', args.skills_root/'runyte-demo-videos/scripts/record.py')
    recorder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(recorder)
    binary = str(args.binary.resolve())
    version = subprocess.check_output([binary, '--version'], text=True).strip()
    digest = hashlib.sha256(Path(binary).read_bytes()).hexdigest()
    with tempfile.TemporaryDirectory(prefix='runyte-sessions-') as directory, \
            tempfile.TemporaryDirectory(prefix='rss-') as settings_directory:
        root = Path(directory)
        runtime = Path(settings_directory)/'rt'
        config = Path(settings_directory)/'config.yaml'
        config.write_text('theme: terafox\nlsp:\n  enable: false\n')
        env = recorder.capture_driver.isolated_env(runtime)
        env.update({'SHELL':'/bin/sh', 'ENV':'/dev/null', 'PS1':'$ ', 'HISTFILE':'/dev/null',
                    'GIT_CONFIG_GLOBAL':'/dev/null', 'GIT_CONFIG_NOSYSTEM':'1'})
        previous = dict(os.environ)
        os.environ.clear()
        os.environ.update(env)
        hosts = []
        try:
            for name, (theme, filename, text) in PROJECTS.items():
                workspace = root/name.lower()
                workspace.mkdir()
                target = workspace/filename
                target.parent.mkdir(exist_ok=True)
                target.write_text(text)
                (workspace/'README.md').write_text(
                    f'# {name}\n\nA small project, ready to grow.\n\n'
                    f'## This session\n\n- Theme: {theme}\n- Working file: {filename}\n'
                    '\n## Next steps\n\n1. Review the changes.\n2. Keep the examples short.\n3. Ship the release.\n')
                (workspace/'.gitignore').write_text('.runyte/\n')
                git = ['git','-c','user.name=Demo','-c','user.email=demo@example.com',
                       '-c','commit.gpgsign=false','-c','core.hooksPath=/dev/null']
                for operation in (['init','-q','-b','main'],['add','.'],['commit','-qm','Prepare session demo']):
                    subprocess.run(git+operation,cwd=workspace,env=env,check=True)
                host = subprocess.Popen([binary,'-c',str(config),'--serve'],cwd=workspace,env=env,
                                        stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
                hosts.append((workspace,host))
                deadline = time.monotonic()+15
                while True:
                    listing = subprocess.run([binary,'-c',str(config),'--session-list'],env=env,capture_output=True,text=True)
                    ready = any(str(workspace) in row and 'running' in row for row in listing.stdout.splitlines())
                    renamed = subprocess.run([binary,'-c',str(config),'--session-rename',str(workspace),name],
                                             env=env,capture_output=True,text=True)
                    if ready and renamed.returncode == 0: break
                    if host.poll() is not None or time.monotonic()>deadline:
                        raise RuntimeError('Session host did not become ready: '+renamed.stderr + (host.stderr.read().decode() if host.poll() is not None else ''))
                    time.sleep(.1)
            setup = []
            # Prepare real session state through the same client used for the take.
            for name, (theme, filename, _) in PROJECTS.items():
                setup += [command('session-attach ../'+name.lower(),1), command('theme '+theme),
                          command('open README.md'),key('?'),key('\x17v'),command('open '+filename)]
            setup += [command('session-attach ../api',1), check('API ready','pending_tasks','terafox')]
            actions = [
                key('  ',1),check('Session manager','Sessions','API','Website'),hold(1.5),
                key('\t',1),check('Session actions','Rename','Open'),hold(1),key('\x1b'),
                type_('Website',.8),key('\r',1),check('Website in ember-dark','ember-dark','style.css'),hold(1.5),
                key('\x1b[1;2D',1),check('Shift Left returns to API','terafox','pending_tasks'),hold(1.5),
                key('\x1b[1;2C',1),check('Shift Right returns to Website','ember-dark','style.css'),hold(1.5),
                key('  ',1),check('Both sessions stay open','Sessions','API','Website'),hold(1),
            ]
            recipe = {'setup':setup,'actions':actions}
            recipe_path = args.output_dir/'session-management.recipe.json'
            recipe_path.write_text(json.dumps(recipe,indent=2)+'\n')
            fonts = args.font_dir
            options = recorder.parser().parse_args([
                '--binary',binary,'--cwd',str(root/'api'),'--config',str(config),
                '--state-dir',str(runtime),'--arg=--persistent','--theme','terafox',
                '--font',str(fonts/'JetBrainsMonoNerdFont-Medium.ttf'),
                '--bold-font',str(fonts/'JetBrainsMonoNerdFontMono-Bold.ttf'),
                '--italic-font',str(fonts/'JetBrainsMonoNerdFont-MediumItalic.ttf'),
                '--bold-italic-font',str(fonts/'JetBrainsMonoNerdFontMono-BoldItalic.ttf'),
                '--steps',str(recipe_path),'--output',str(args.output_dir/'session-management.mp4'),
                '--label',f'{version}; source {args.source_ref or "unverified"}; binary sha256 {digest}; session management; terafox and ember-dark',
            ])
            def playback(capture, play):
                try:
                    for action in actions:
                        play(action)
                        if action['op']=='checkpoint':
                            if str(Path.home()) in capture.text(): raise RuntimeError('Personal path in capture')
                            expected = {'Website in ember-dark':'282a2f', 'Shift Left returns to API':'152528',
                                        'Shift Right returns to Website':'282a2f'}.get(action['name'])
                            if expected and capture.screen.buffer[35][150].bg != expected:
                                raise RuntimeError('Session did not retain its expected theme')
                            slug=action['name'].lower().replace(' ','-')
                            capture.render_image().save(args.output_dir/f'session-management-{slug}.png')
                except BaseException:
                    capture.render_image().save(args.output_dir/'failure.png')
                    (args.output_dir/'failure.txt').write_text(capture.text())
                    raise
            print(json.dumps(recorder.record(options,recipe,playback=playback)),flush=True)
            (args.output_dir/'session-management.provenance.json').write_text(json.dumps({
                'version':version,'source_revision':args.source_ref,'binary_sha256':digest,'theme':'terafox / ember-dark',
                'geometry':'200x50','font':'JetBrainsMono Nerd Font Medium',
            },indent=2)+'\n')
        finally:
            # Never stop sessions outside this scene's exact workspace paths.
            for workspace,host in hosts:
                try:
                    subprocess.run([binary,'-c',str(config),'--session-stop',str(workspace),'--force'],
                                   env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=15)
                except subprocess.TimeoutExpired:
                    host.terminate()
                try: host.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    host.terminate()
                    try: host.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        host.kill(); host.wait()
            os.environ.clear()
            os.environ.update(previous)


if __name__=='__main__': main()
