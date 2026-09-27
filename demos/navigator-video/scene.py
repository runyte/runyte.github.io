# SPDX-License-Identifier: MPL-2.0
"""Fixture and isolated Claude Code settings for the Navigator video."""
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess

CARGO_TOML = '[package]\nname = "api"\nversion = "0.1.0"\nedition = "2021"\n\n[dependencies]\n'
README = '# api\n\nA small task service, ready to grow.\n\nRun the tests with `cargo test`.\n'
DESIGN = '# Design\n\nTasks are kept in memory and sorted by priority.\n'
NOTES = '# Notes\n\n- Persist tasks between runs.\n- Add due dates.\n'
SCRATCH = 'tmp: try a BTreeMap keyed by priority\n'
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


def git(workspace, *args):
    subprocess.run(['git', '-c', 'user.name=Demo', '-c', 'user.email=demo@example.com', *args],
                   cwd=workspace, check=True)


def prepare(workspace):
    """Create and commit the demo Cargo project in an empty directory."""
    workspace = Path(workspace)
    if workspace.exists() and any(workspace.iterdir()):
        raise SystemExit('Use an empty temporary workspace.')
    for directory in ('src', 'docs'):
        (workspace/directory).mkdir(parents=True)
    files = {'Cargo.toml': CARGO_TOML, 'README.md': README, 'docs/design.md': DESIGN,
             'notes.md': NOTES, 'scratch.txt': SCRATCH, 'src/store.rs': STORE,
             'src/main.rs': MAIN, '.gitignore': '/target\n.runyte/\n'}
    for name, text in files.items():
        (workspace/name).write_text(text)
    # Build first so the recorded test run is quick.
    subprocess.run(['cargo', 'generate-lockfile', '--offline', '-q'], cwd=workspace, check=True)
    subprocess.run(['cargo', 'test', '-q', '--no-run'], cwd=workspace, check=True,
                   stderr=subprocess.DEVNULL)
    git(workspace, 'init', '-q', '-b', 'main')
    git(workspace, 'add', '-A')
    git(workspace, 'commit', '-qm', 'Start the task service')


def claude_home(settings, workspace):
    """A private Claude Code config dir: copied login, onboarding done, folder trusted."""
    source = Path(os.environ.get('CLAUDE_CONFIG_DIR', Path.home()/'.claude'))
    credentials = source/'.credentials.json'
    if not credentials.is_file():
        raise SystemExit('This scene needs a Claude Code login (.credentials.json).')
    home = Path(settings)/'claude'
    home.mkdir(mode=0o700, exist_ok=True)
    shutil.copyfile(credentials, home/'.credentials.json')
    (home/'.credentials.json').chmod(0o600)
    version = subprocess.check_output(['claude', '--version'], text=True).split()[0]
    state = {
        'hasCompletedOnboarding': True,
        'lastOnboardingVersion': version,
        'theme': 'dark',
        # The LSP plugin dialog would otherwise interrupt the take after Claude's edit.
        'lspRecommendationDisabled': True,
        'projects': {str(Path(workspace).resolve()): {'hasTrustDialogAccepted': True}},
    }
    # Carry over only which notices were already seen, so none reappears on screen.
    try:
        own = json.loads((Path.home()/'.claude.json').read_text())
    except (OSError, ValueError):
        own = {}
    for name, value in own.items():
        if name.startswith(('hasShown', 'hasSeen')) and isinstance(value, bool):
            state[name] = value
        elif name == 'lastReleaseNotesSeen' and isinstance(value, str):
            state[name] = value
    (home/'.claude.json').write_text(json.dumps(state))
    # Edits and `cargo test` are approved in advance; any other command would ask.
    (home/'settings.json').write_text(json.dumps({'permissions': {
        'defaultMode': 'acceptEdits', 'allow': ['Bash(cargo test:*)']}}))
    return home


def private_markers():
    """Account name and email words that must never appear on screen.

    They are read from the local Claude Code state and kept in memory only.
    """
    source = Path(os.environ.get('CLAUDE_CONFIG_DIR', Path.home()))
    state = source/'.claude.json'
    if not state.is_file():
        state = Path.home()/'.claude.json'
    try:
        account = json.loads(state.read_text()).get('oauthAccount', {})
    except (OSError, ValueError):
        return []
    words = set()
    for field in ('displayName', 'fullName', 'emailAddress'):
        value = account.get(field) or ''
        words.update(part for part in value.replace('@', ' ').split() if len(part) >= 4)
        if '@' in value:
            words.add(value)
    return sorted(words)


def child_env(settings, binary):
    """Environment shared by the host and client, and so by every terminal.

    Terminals get a private home whose .bashrc only sets a plain prompt, so no
    user name, host name or personal shell setup reaches the video. Cargo and
    rustup keep using the real toolchain.
    """
    home = Path(settings)/'home'
    home.mkdir(exist_ok=True)
    (home/'.bashrc').write_text("PS1='$ '\nunset PROMPT_COMMAND\n")
    real = Path.home()
    editor = shlex.quote(str(binary)) + ' --wait'
    return {'HOME': str(home), 'SHELL': '/bin/bash',
            'CARGO_HOME': os.environ.get('CARGO_HOME', str(real/'.cargo')),
            'RUSTUP_HOME': os.environ.get('RUSTUP_HOME', str(real/'.rustup')),
            'CLAUDE_CONFIG_DIR': str(Path(settings)/'claude'), 'DISABLE_AUTOUPDATER': '1',
            'EDITOR': editor, 'VISUAL': editor, 'HISTFILE': '/dev/null'}
