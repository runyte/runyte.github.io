#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""Capture the Navigator listing files, an explorer, terminals and About."""
import argparse
import importlib.util
import os
from pathlib import Path
import subprocess

CARGO_TOML = '[package]\nname = "api"\nversion = "0.1.0"\nedition = "2021"\n\n[dependencies]\n'
README = '# api\n\nA small task service, ready to grow.\n\nRun the tests with `cargo test`.\n'
DESIGN = '# Design\n\nTasks are kept in memory and sorted by priority.\n'
STORE = '''use crate::Task;

pub struct Store {
    tasks: Vec<Task>,
}

impl Store {
    pub fn new() -> Self {
        Self { tasks: Vec::new() }
    }

    pub fn add(&mut self, task: Task) {
        self.tasks.push(task);
        self.tasks.sort_by_key(|task| std::cmp::Reverse(task.priority));
    }

    pub fn pending(&self) -> impl Iterator<Item = &Task> {
        self.tasks.iter().filter(|task| !task.complete)
    }
}
'''
MAIN = '''//! A small task service, ready to grow.

mod store;

#[derive(Debug, PartialEq)]
pub struct Task {
    pub title: String,
    pub complete: bool,
    pub priority: u8,
}

impl Task {
    pub fn new(title: &str) -> Self {
        Self { title: title.to_owned(), complete: false, priority: 0 }
    }

    pub fn finish(&mut self) {
        self.complete = true;
    }
}

fn main() {
    let mut store = store::Store::new();
    store.add(Task::new("Write the README"));
    for task in store.pending() {
        println!("{}", task.title);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn new_task_is_open() {
        assert!(!Task::new("Plan").complete);
    }

    #[test]
    fn finish_marks_complete() {
        let mut task = Task::new("Ship");
        task.finish();
        assert!(task.complete);
    }
}
'''

# Ctrl-\ returns control from a terminal child to Runyte.
LEAVE_TERMINAL = [{'op': 'key', 'text': '\x1c'}, {'op': 'wait', 'wait': 0.3}]
STEPS = [
    {'op': 'wait', 'wait': 1.5},
    {'op': 'command', 'text': 'about'},
    # An unsaved edit shows the [+] state flag.
    {'op': 'command', 'text': 'open README.md'},
    {'op': 'key', 'text': 'ge'},
    {'op': 'key', 'text': 'oTODO: document the HTTP endpoints.'},
    {'op': 'wait', 'wait': 0.2},
    {'op': 'key', 'text': '\x1b'},
    {'op': 'wait', 'wait': 0.3},
    {'op': 'command', 'text': 'open docs/design.md'},
    # Two terminals that keep running after Space t q hides them.
    {'op': 'command', 'text': 'terminal python3 -m http.server 8000 --bind 127.0.0.1 --directory docs'},
    {'op': 'expect', 'text': 'Serving HTTP'},
    *LEAVE_TERMINAL,
    {'op': 'command', 'text': 'terminal-rename docs server'},
    {'op': 'key', 'text': ' tq'},
    {'op': 'command', 'text': 'terminal bash --norc --noprofile'},
    {'op': 'wait', 'wait': 0.5},
    {'op': 'key', 'text': 'git log --oneline\r'},
    *LEAVE_TERMINAL,
    {'op': 'command', 'text': 'terminal-rename git'},
    {'op': 'key', 'text': ' tq'},
    # Visible layout: file left, explorer top right, test terminal below it.
    {'op': 'command', 'text': 'open src/main.rs'},
    {'op': 'key', 'text': 'gg'},
    {'op': 'key', 'text': '\x17v'},
    {'op': 'key', 'text': ' E'},
    {'op': 'key', 'text': '\x17s'},
    {'op': 'command', 'text': 'terminal bash --norc --noprofile'},
    {'op': 'wait', 'wait': 0.5},
    {'op': 'key', 'text': 'cargo test -q\r'},
    {'op': 'expect', 'text': 'test result', 'timeout': 60},
    {'op': 'wait', 'wait': 0.5},
    *LEAVE_TERMINAL,
    {'op': 'command', 'text': 'terminal-rename tests'},
    # Running the tests invalidates Git status; show a settled status line.
    {'op': 'command', 'text': 'git-refresh'},
    {'op': 'wait', 'wait': 2},
    {'op': 'key', 'text': ' n'},
    {'op': 'wait', 'wait': 0.8},
]
REQUIRED = ['Navigator', 'tests', 'git', 'docs server', '[explorer]', '[+]', '[about]', 'test result: ok']


def git(workspace, *args):
    subprocess.run(['git', '-c', 'user.name=Demo', '-c', 'user.email=demo@example.com', *args],
                   cwd=workspace, check=True)


def prepare(workspace):
    for directory in ('src', 'tests', 'docs'):
        (workspace/directory).mkdir(parents=True)
    (workspace/'Cargo.toml').write_text(CARGO_TOML)
    (workspace/'README.md').write_text(README)
    (workspace/'docs/design.md').write_text(DESIGN)
    (workspace/'src/store.rs').write_text(STORE)
    (workspace/'src/main.rs').write_text(MAIN)
    (workspace/'tests/store.rs').write_text('#[test]\nfn placeholder() {}\n')
    (workspace/'.gitignore').write_text('/target\n.runyte/\n')
    # Build first so the test run is quick and target/ exists before the explorer opens.
    subprocess.run(['cargo', 'generate-lockfile', '--offline', '-q'], cwd=workspace, check=True)
    subprocess.run(['cargo', 'test', '-q', '--no-run'], cwd=workspace, check=True,
                   stderr=subprocess.DEVNULL)
    git(workspace, 'init', '-q', '-b', 'main')
    git(workspace, 'add', '-A')
    git(workspace, 'commit', '-qm', 'Start the task service')
    # Uncommitted changes for the gutter and the status line.
    main = workspace/'src/main.rs'
    main.write_text(main.read_text().replace('priority: 0 }', 'priority: 1 }'))
    with (workspace/'README.md').open('a') as readme:
        readme.write('\nSee docs/design.md for the data model.\n')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--skills-root', type=Path, required=True)
    p.add_argument('--binary', type=Path, required=True)
    p.add_argument('--font-dir', type=Path, required=True)
    p.add_argument('--workspace', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--label', default='')
    args = p.parse_args()
    workspace = args.workspace.resolve()
    if workspace.exists() and any(workspace.iterdir()):
        raise SystemExit('Use an empty temporary workspace.')
    prepare(workspace)
    spec = importlib.util.spec_from_file_location(
        'capture', args.skills_root/'runyte-screenshots/scripts/capture.py')
    capture = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(capture)
    # Terminals inherit this environment: a plain prompt keeps user and host names out of the image.
    os.environ.update(PS1='$ ', HISTFILE='/dev/null')
    fonts = args.font_dir
    options = capture.parser().parse_args([
        '--binary', str(args.binary.resolve()), '--cwd', str(workspace),
        '--font', str(fonts/'JetBrainsMonoNerdFont-Medium.ttf'),
        '--bold-font', str(fonts/'JetBrainsMonoNerdFontMono-Bold.ttf'),
        '--italic-font', str(fonts/'JetBrainsMonoNerdFont-MediumItalic.ttf'),
        '--bold-italic-font', str(fonts/'JetBrainsMonoNerdFontMono-BoldItalic.ttf'),
        '--theme', 'terafox-soft', '--label', args.label, '--interactive',
    ])
    with capture.Capture(options) as session:
        for step in STEPS:
            session.action(step)
        session.action({'op': 'save', 'path': str(args.output.resolve()), 'required': REQUIRED})


if __name__ == '__main__':
    main()
