---
title: Installation
description: Install Rust, Cargo, and Runyte on Linux or macOS.
---

# Installation

Runyte currently supports **Linux and macOS**. It requires Rust 1.88 or newer
and a C compiler for its bundled Tree-sitter grammars.

## 1. Install Rust and Cargo

[Cargo](https://doc.rust-lang.org/stable/cargo/) is Rust's package manager and
build tool. It downloads packages from crates.io and builds their executable
programs. The recommended way to get Cargo is to install Rust with
[rustup](https://rust-lang.org/tools/install/), the official Rust toolchain
installer and version manager.

On Linux or macOS, run:

```sh
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

Follow the on-screen instructions, then restart your terminal. Confirm that
both tools are available:

```sh
rustc --version
cargo --version
```

You also need a C compiler. On macOS, the Xcode Command Line Tools provide one
(`xcode-select --install`). On Linux, install your distribution's C development
tools if `cc --version` is not already available.

## 2. Install Runyte

Cargo builds Runyte from its published package and installs the `runyte`
executable:

```sh
cargo install runyte --locked
```

The `--locked` flag uses the dependency versions tested with the release.

## 3. Start Runyte

```sh
runyte             # open the built-in introduction
runyte .           # explore and edit the current directory
runyte README.md   # open a file
```

Once inside, run `:tutorial` for a guided introduction or press `Space ?` for
contextual help.
