---
seoTitle: "Install Runyte on Linux, macOS, and Windows"
title: Installation
description: Download Runyte for Linux, macOS, or Windows, or build it with Cargo.
---

# Get Runyte

## Download 0.3.2

{{< compact-table label="Runyte 0.3.2 downloads" >}}
| Platform | Download |
| --- | --- |
| **macOS · Apple Silicon** | [ARM64 archive](https://github.com/runyte/runyte/releases/download/v0.3.2/runyte-v0.3.2-aarch64-apple-darwin.tar.xz) |
| **macOS · Intel** | [x86-64 archive](https://github.com/runyte/runyte/releases/download/v0.3.2/runyte-v0.3.2-x86_64-apple-darwin.tar.xz) |
| **Linux · Intel / AMD** | [x86-64 archive](https://github.com/runyte/runyte/releases/download/v0.3.2/runyte-v0.3.2-x86_64-unknown-linux-gnu.tar.xz) |
| **Linux · ARM** | [ARM64 archive](https://github.com/runyte/runyte/releases/download/v0.3.2/runyte-v0.3.2-aarch64-unknown-linux-gnu.tar.xz) |
| **Windows · x86-64** | [ZIP archive](https://github.com/runyte/runyte/releases/download/v0.3.2/runyte-v0.3.2-x86_64-pc-windows-msvc.zip) · provisional |
{{< /compact-table >}}

Verify against [SHA256SUMS](https://github.com/runyte/runyte/releases/download/v0.3.2/SHA256SUMS),
extract, and put `runyte` on your `PATH`. macOS binaries are unsigned and not notarized.

On Windows, check the hash with `Get-FileHash -Algorithm SHA256`. The
executable is unsigned and needs the x64
[Visual C++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist)
(`VCRUNTIME140.dll`), which the ZIP does not include. Windows support is
provisional: it targets Windows 11 24H2 or later in Windows Terminal.
[Windows scope and requirements](/docs/user-guide/#windows-support)

[All releases](https://github.com/runyte/runyte/releases)

## Or build with Cargo

Requires [Rust 1.88+ and Cargo](https://rust-lang.org/tools/install/) and a C compiler.
On Windows, use Visual Studio Build Tools with the C++ toolchain and Windows SDK.

```sh
cargo install runyte --locked
```

## Start here

```sh
runyte
runyte .
runyte README.md
runyte --persistent
```

Inside Runyte: `:tutorial` for a guided tour, `Space ?` for help.

{{< compact-table label="Optional tools" >}}
| For | Requirement |
| --- | --- |
| Git workflows | `git` on your `PATH` |
| Language services | Your language server; allow it with `:lsp-trust` |
| Linux system clipboard | `wl-clipboard`, `xclip`, or `xsel` |
| macOS system clipboard | Built-in `pbcopy` / `pbpaste`; nothing to install |
| Windows system clipboard | Built in; nothing to install |
{{< /compact-table >}}
