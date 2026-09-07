---
title: Installation
description: Download Runyte for Linux or macOS, or build it with Cargo.
---

# Get Runyte

## Download 0.2.0

{{< compact-table label="Runyte 0.2.0 downloads" >}}
| Platform | Download |
| --- | --- |
| **macOS · Apple Silicon** | [ARM64 archive](https://github.com/runyte/runyte/releases/download/v0.2.0/runyte-v0.2.0-aarch64-apple-darwin.tar.xz) |
| **macOS · Intel** | [x86-64 archive](https://github.com/runyte/runyte/releases/download/v0.2.0/runyte-v0.2.0-x86_64-apple-darwin.tar.xz) |
| **Linux · Intel / AMD** | [x86-64 archive](https://github.com/runyte/runyte/releases/download/v0.2.0/runyte-v0.2.0-x86_64-unknown-linux-gnu.tar.xz) |
| **Linux · ARM** | [ARM64 archive](https://github.com/runyte/runyte/releases/download/v0.2.0/runyte-v0.2.0-aarch64-unknown-linux-gnu.tar.xz) |
{{< /compact-table >}}

Verify against [SHA256SUMS](https://github.com/runyte/runyte/releases/download/v0.2.0/SHA256SUMS),
extract, and put `runyte` on your `PATH`. macOS binaries are unsigned and not notarized.

[All releases](https://github.com/runyte/runyte/releases)

## Or build with Cargo

Requires [Rust 1.88+ and Cargo](https://rust-lang.org/tools/install/) and a C compiler.

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
{{< /compact-table >}}
