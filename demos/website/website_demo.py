#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""Record a real Runyte prompt-editor, Codex, explorer and Rust diagnostics demo."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import tempfile
import time


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--skills-root', type=Path, required=True)
    p.add_argument('--binary', type=Path, required=True)
    p.add_argument('--font-dir', type=Path, required=True)
    p.add_argument('--workspace', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    spec = importlib.util.spec_from_file_location('record', args.skills_root / 'runyte-demo-videos/scripts/record.py')
    record = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(record)
    workspace = args.workspace.resolve()
    if workspace.exists() and any(workspace.iterdir()):
        raise SystemExit('Use an empty temporary workspace.')
    workspace.mkdir(parents=True, exist_ok=True)
    (workspace/'Cargo.toml').write_text('[package]\nname = "focus-planner"\nversion = "0.1.0"\nedition = "2024"\n\n[[bin]]\nname = "focus"\npath = "focus.rs"\n')
    (workspace/'.gitignore').write_text('/target/\n/.runyte/\n')
    subprocess.run(['git', 'init', '-q', str(workspace)], check=True)
    prompt = Path(__file__).with_name('prompt.md').read_text()
    binary = str(args.binary.resolve())
    version = subprocess.check_output([binary, '--version'], text=True).strip()
    with tempfile.TemporaryDirectory(prefix='rd-') as settings:
        settings = Path(settings)
        config = settings/'config.yaml'
        config.write_text('theme: ocean-dark\nlsp:\n  enable: true\neditor:\n  soft_wrap: false\n  word_completion: false\n')
        # Isolate Codex UI state and prompt filenames; use the existing login without printing it.
        codex_home = settings/'codex'
        codex_home.mkdir(mode=0o700)
        source_home = Path(os.environ.get('CODEX_HOME', str(Path.home()/'.codex')))
        auth = source_home/'auth.json'
        if not auth.is_file():
            raise SystemExit('This scene needs a Codex file-based login (auth.json).')
        shutil.copyfile(auth, codex_home/'auth.json')
        (codex_home/'auth.json').chmod(0o600)
        (codex_home/'config.toml').write_text('model = "gpt-6-astra"\nmodel_reasoning_effort = "low"\n')
        runtime = settings/'runtime'
        env = record.capture_driver.isolated_env(runtime)
        env.update(EDITOR=shlex.quote(binary)+' --wait', VISUAL=shlex.quote(binary)+' --wait', CODEX_HOME=str(codex_home), PS1='demo $ ')
        # Capture's environment derives from this process; host and client must agree.
        previous = {k: os.environ.get(k) for k in ('EDITOR', 'VISUAL', 'CODEX_HOME', 'PS1')}
        os.environ.update({k:env[k] for k in previous})
        fonts = args.font_dir
        opts = record.parser().parse_args([
            '--binary',binary,'--cwd',str(workspace),'--config',str(config),
            '--state-dir',str(runtime),'--arg=--persistent',
            '--font',str(fonts/'JetBrainsMonoNerdFont-Medium.ttf'),
            '--bold-font',str(fonts/'JetBrainsMonoNerdFontMono-Bold.ttf'),
            '--italic-font',str(fonts/'JetBrainsMonoNerdFont-MediumItalic.ttf'),
            '--bold-italic-font',str(fonts/'JetBrainsMonoNerdFontMono-BoldItalic.ttf'),
            '--steps',str(Path(__file__).with_name('prompt.md')),'--output',str(args.output),
            '--max-duration','600','--opening-hold','1','--closing-hold','2',
            '--label',version+'; ocean-dark; live Codex focus planner; 200 columns x 50 rows'])
        host = subprocess.Popen([binary,'-c',str(config),'--serve'],cwd=workspace,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        def scene(c, play):
            def do(op, **kw): play({'op':op, **kw})
            def key(s, wait=.2): do('key',text=s,wait=wait)
            def command(s, wait=.2, interval=.035): do('command',text=s,wait=wait,interval=interval)
            def rows(): return c.text().splitlines()
            def right(): return [s[101:199].strip() for s in rows()[1:47]]
            def check(name, required=(), wait=.1):
                do('checkpoint',name=name,required=list(required),wait=wait)
                print('CHECKPOINT',name,flush=True)
                c.render_image().save(args.output.with_name(args.output.stem+'-'+re.sub('[^a-z0-9]+','-',name.lower())+'.png'))
            def until(fn, timeout=90):
                end=time.monotonic()+timeout
                while not fn():
                    if time.monotonic()>end:
                        raise RuntimeError('readiness timeout')
                    do('wait',wait=.2)
            try:
                check('About opening', [version.replace('runyte', 'Runyte', 1)])
                key('\x17v',.5)
                command('terminal bash --noprofile --norc',wait=.5,interval=.018)
                do('type',text='codex --no-alt-screen -s read-only -a never',interval=.025,wait=.15)
                key('\r',.2)
                check('Codex startup begins',wait=0)
                do('wait',wait=2)
                for _ in range(60):
                    if any('trust the contents' in s for s in right()):
                        key('\r',1)
                    if any('OpenAI Codex' in s for s in right()) and any('Ask Codex' in s for s in right()):
                        do('wait',wait=1)
                        if not any('trust the contents' in s for s in right()):break
                    do('wait',wait=.5)
                else:raise RuntimeError('Codex did not reach its ready prompt')
                key('\x0c',.3)
                for _ in range(15):
                    if not any('usage limit' in s or 'Session renamed' in s or 'Ctrl+L is disabled' in s for s in right()):break
                    do('wait',wait=.5)
                    key('\x0c',.2)
                key('\x1c',.15)
                command('terminal-rename Codex',interval=0)
                key('i',.2)
                check('Codex ready',['OpenAI Codex'],wait=.3)
                key('\x07',.3)
                until(lambda:'[file]' in rows()[0] and '.md' in rows()[0])
                key('%',.1)
                key('c',.1)
                do('type',text=prompt,interval=.012,wait=.2)
                key('\x1b',.25)
                key('gg',.2)
                check('Prompt composed',['focus planner'],wait=.3)
                key('?',.8)
                check('Wide table rendered',wait=.1)
                key(' ps',1.2)
                check('Table soft wrapping',['Scheduling constraint'],wait=.4)
                key('?',.25)
                command('wbc',wait=.6,interval=.07)
                check('Prompt returned to Codex',wait=.1)
                key('\r',.2)
                check('Codex response wait begins',wait=0)
                def answer_complete():
                    rr=right()
                    starts=[i for i,s in enumerate(rr) if re.match(r'• (?:use |#\[|struct |type |fn |const )',s)]
                    inputs=[i for i,s in enumerate(rr) if 'Ask Codex' in s]
                    if not starts or not inputs or inputs[-1]<=starts[0]:return False
                    code='\n'.join(rr[starts[0]:inputs[-1]]).rstrip()
                    return ('fn main()' in code and code.endswith('}') and code.count('{')==code.count('}') and not any('esc to interrupt' in s for s in rr))
                until(answer_complete,180)
                do('wait',wait=.4)
                check('Codex answered',['fn main()'],wait=1)
                key('\x1c',.15)
                # gw captures the immutable review directly from live Normal mode.
                targets=[(y,s.index('focus',101)) for y,s in enumerate(rows()[1:47],1) if 'fn focus(' in s[101:]]
                if not targets:raise RuntimeError('focus function is not visible')
                y,x=targets[0]
                key('gw',.75)
                check('Jump labels',['jump to word'],wait=.2)
                first,second,third=[c.screen.buffer[y][x+i] for i in range(3)]
                label=first.data+(second.data if second.fg!=third.fg else '')
                if not re.fullmatch('[a-z]{1,2}',label):raise RuntimeError('invalid jump label')
                for char in label:key(char,.35)
                key('ve',.45)
                key('y',.2)
                key('\x17h',.25)
                key(' E',.5)
                check('File manager opened',['[explorer]'],wait=.1)
                key('o',.15)
                key('\x1b',.15)
                key('p',.4)
                key('A',.1)
                do('type',text='.rs',interval=.09,wait=.15)
                key('\x1b',.15)
                command('w',wait=.45)
                check('Create file from copied word',['create focus.rs'],wait=.4)
                key('\r',.4)
                if not (workspace/'focus.rs').is_file():raise RuntimeError('copied word did not create focus.rs')
                key('\r',.35)
                key('\x17l',.2)
                # Select the actual answer block, excluding the Codex bullet and input prompt.
                visible=rows()
                starts=[(y,s.index('•',101)+2) for y,s in enumerate(visible[1:47],1) if re.match(r'• (?:use |#\[|struct |type |fn |const )',s[101:199].strip())]
                if len(starts)!=1:raise RuntimeError('complete answer start is not visible')
                sy,sx=starts[0]
                ends=[y for y,s in enumerate(visible[sy+1:47],sy+1) if s[101:199].strip()=='}']
                if not ends:raise RuntimeError('answer ending is missing')
                ey=ends[-1]
                do('mouse',x=sx+1,y=sy+1,wait=.1)
                do('mouse',x=sx+1,y=sy+1,release=True,wait=.1)
                key('v'+str(ey-sy)+'j$',.6)
                check('Select complete answer',wait=.2)
                key('y',.15)
                key(';',.15)
                key('\x17h',.2)
                key('p',.7)
                command('w',wait=.3)
                source=(workspace/'focus.rs').read_text()
                if 'fn focus(' not in source or 'fn main()' not in source or 'Ask Codex' in source:raise RuntimeError('answer copy verification failed')
                args.output.with_suffix('.answer.rs').write_text(source)
                # Compile only; never execute generated code for the recording.
                result=subprocess.run(['cargo','check','--offline'],cwd=workspace,env=env,capture_output=True,text=True,timeout=60)
                if result.returncode:raise RuntimeError('generated source did not compile: '+result.stderr)
                check('Rust answer pasted',['rust-analyzer'],wait=.5)
                command('format',wait=.5)
                key('/15\r',.35)
                key('c',.1)
                do('type',text='"15"',interval=.13,wait=.2)
                key('\x1b',.2)
                command('w',wait=.3)
                check('Diagnostics wait begins',wait=0)
                until(lambda: '1E' in rows()[48],60)
                check('Rust type error ready',wait=.3)
                key(' ld',.5)
                check('Rust diagnostics',['mismatched types'],wait=.4)
            except BaseException:
                args.output.with_suffix('.failure.txt').write_text(c.text())
                c.render_image().save(args.output.with_suffix('.failure.png'))
                raise
        try:
            recipe={'setup':[{'op':'expect','text':'Run language servers'},{'op':'key','text':'\x1b[B\r','wait':.4},{'op':'command','text':'session-rename '+str(workspace)+' Focus planner','interval':0,'wait':.2},{'op':'command','text':'about','interval':0,'wait':.2}], 'actions':[{'op':'wait','wait':0}]}
            result=record.record(opts,recipe,playback=scene)
            print(json.dumps(result),flush=True)
        finally:
            subprocess.run([binary,'-c',str(config),'--session-stop',str(workspace),'--force'],env=env,capture_output=True,timeout=15)
            try:host.wait(timeout=10)
            except subprocess.TimeoutExpired:
                host.terminate()
                try:host.wait(timeout=5)
                except subprocess.TimeoutExpired:host.kill();host.wait()
            for key,value in previous.items():
                if value is None:os.environ.pop(key,None)
                else:os.environ[key]=value

if __name__=='__main__':main()
