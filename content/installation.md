---
seoTitle: "Install Runyte on Linux, macOS, and Windows"
title: Installation
description: Install the terminal or desktop edition of Runyte. Use the installer, download a release or disk image, or install through Cargo.
---

# Install Runyte

{{< edition-tabs >}}
{{< edition id="terminal" title="Terminal edition" >}}
## Linux and macOS

Install or update to the latest release:

```sh
curl -fsSL https://raw.githubusercontent.com/runyte/runyte/main/install.sh | sh
```

- Supports x86-64 and ARM64. Verifies the download's SHA-256 checksum.
- Installs to `~/.local/bin/runyte` without sudo. Add that directory to `PATH`.
- Linux needs glibc 2.35 or newer. Alpine/musl is unsupported.
- macOS binaries are unsigned and not notarized.

[Review the installer](https://github.com/runyte/runyte/blob/main/install.sh) ·
[Options and requirements](/docs/user-guide/#install-and-update-with-curl)

## Windows

Download the x86-64 ZIP from [GitHub Releases](https://github.com/runyte/runyte/releases).
Verify its hash against `SHA256SUMS`, extract it, and add its directory to `PATH`.

- Requires Windows 11 24H2 or later and Windows Terminal.
- The executable is unsigned.
- Install the x64 Visual C++ Redistributable if `VCRUNTIME140.dll` is missing.

[Windows setup and differences](/docs/user-guide/#windows-support)

## Cargo

Requires Rust 1.88 or newer and a C compiler.

```sh
cargo install runyte --locked
```

On Windows, install Visual Studio Build Tools with the C++ toolchain and Windows SDK.
{{< /edition >}}
{{< edition id="desktop" title="Desktop edition" >}}
## Linux and macOS {#desktop-script}

Install or update to the latest release:

```sh
curl -fsSL https://raw.githubusercontent.com/runyte/runyte/main/install.sh | sh -s -- --desktop
```

Then open it in its own native window:

```sh
runyte --window
```

- Linux needs glibc 2.39 or newer, a graphical desktop, and a working Vulkan driver.
- macOS needs version 11 or later. Runs on Apple silicon and Intel.
- On macOS the script installs `Runyte.app` in `~/Applications`.
- The desktop edition also runs in a terminal. Run `runyte` without `--window`.
- There is no Windows desktop edition.

[Review the installer](https://github.com/runyte/runyte/blob/main/install.sh) ·
[Options and requirements](https://github.com/runyte/runyte/blob/main/INSTALLATION.md#desktop-edition)

## macOS disk image {#desktop-macos}

Download `Runyte-X.Y.Z.dmg` from [GitHub Releases](https://github.com/runyte/runyte/releases).
Open it and drag Runyte onto Applications. Launch it from Finder, Launchpad, or Spotlight.

The app is signed and notarized, so macOS asks only its usual first-launch confirmation.

## Linux archive {#desktop-linux}

Download the `runyte-desktop` archive for your CPU from
[GitHub Releases](https://github.com/runyte/runyte/releases).
Extract it into a permanent directory, then run these commands from that directory:

```sh
./runyte --window --editor
python3 contrib/packaging/package.py linux --binary ./runyte
```

The last command registers the launcher and icons for your desktop account.
Add the directory to `PATH`, or link its `runyte` and `runed` into `~/.local/bin`.
{{< /edition >}}
{{< /edition-tabs >}}

## First run

| Command | Start with |
| --- | --- |
| `runyte` | The current directory |
| `runyte --window` | The current directory, in its own native window (desktop edition) |
| `runyte README.md` | A file |
| `runyte +120:8 src/app.rs` | A line and column |
| `runyte -a` | A persistent session |

Inside Runyte, use `:tutorial` to learn interactively. Press `Space ?` for help.

## Set your editor

On Linux and macOS, add these to your shell configuration:

```sh
alias ru=runyte
export EDITOR='runyte --wait'
export VISUAL='runyte --wait'
```

Git, Claude Code, and Codex can then open files or prompts in Runyte.
See the [shell setup guide](/docs/user-guide/#change-the-shell-directory-on-exit)
for Windows setup and changing directory on exit.

## Optional tools

| For | Install |
| --- | --- |
| Git features | `git` |
| Language services | Your language server; allow it with `:lsp-trust` |
| Linux clipboard | `wl-clipboard`, `xclip`, or `xsel` |

The macOS and Windows clipboard integrations use system tools or APIs.

[All release downloads](https://github.com/runyte/runyte/releases) ·
[Full manual](/docs/user-guide/)
