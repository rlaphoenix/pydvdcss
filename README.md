![Banner](https://raw.githubusercontent.com/homemediadb/pydvdcss/master/banner.png)

[![License](https://img.shields.io/:license-GPL%203.0-blue.svg)](https://github.com/homemediadb/pydvdcss/blob/master/LICENSE)
[![Python version](https://img.shields.io/pypi/pyversions/pydvdcss)](https://pypi.python.org/pypi/pydvdcss)
[![Release version](https://img.shields.io/pypi/v/pydvdcss)](https://pypi.python.org/pypi/pydvdcss)
[![Manager: uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Onyx-Nostalgia/uv/refs/heads/fix/logo-badge/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Linter: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Build status](https://github.com/homemediadb/pydvdcss/actions/workflows/ci.yml/badge.svg)](https://github.com/homemediadb/pydvdcss/actions/workflows/ci.yml)

**pydvdcss** is a Python wrapper for VideoLAN's [libdvdcss].

[libdvdcss] is a simple library designed for accessing DVDs like a block device without having to bother about the
decryption.

  [libdvdcss]: <https://www.videolan.org/developers/libdvdcss.html>

## Features

- **Portability** — Supported platforms include GNU/Linux, FreeBSD, NetBSD, OpenBSD, Haiku, macOS, Solaris, QNX,
  OS/2, and Windows NT 4.0 SP4 (with IE 5.0) or later.
- **Simplicity** — A DVD player can be built around the libdvdcss API using no more than 4 or 5 library calls.
- **Freedom** — libdvdcss is released under the GPL, ensuring it stays free and is used only for free software.
- **Adaptability** — Unlike most similar projects, libdvdcss does not require the region of your drive to be set, and
  will try its best to read from the disc even in the case of a region mismatch.

## Installation

```shell
pip install pydvdcss
```

pydvdcss is a wrapper, so it needs the native **libdvdcss** library too:

- **Windows**: nothing to do — the Windows wheels **bundle** `libdvdcss-2.dll`, so
  `pip install pydvdcss` is all you need. (If you install the source distribution instead,
  drop a `libdvdcss-2.dll` next to your script, in the current working directory, or in
  `C:/Windows/System32`; pre-built DLLs: <https://github.com/allienx/libdvdcss-dll>.)
- **Linux**: install it from your distribution's repositories (e.g. `libdvdcss2`).
- **macOS**: `brew install libdvdcss`.

pydvdcss looks for the library bundled inside the package first, then falls back to a
system-installed copy.

### Bundled libdvdcss

The Windows wheels include a precompiled `libdvdcss-2.dll` (© VideoLAN, GPL-2.0-or-later)
taken unmodified from <https://github.com/allienx/libdvdcss-dll> and verified by SHA-256 at
build time. The pure wheel and source distribution do not bundle it. See
[THIRD-PARTY-NOTICES.md](https://github.com/homemediadb/pydvdcss/blob/master/THIRD-PARTY-NOTICES.md)
for attribution, license, and the GPL written offer for source.

## Usage

```python
from pydvdcss import DvdCss

with DvdCss() as dvd:
    dvd.open("D:")               # a device ("D:", "/dev/sr0"), an ISO file, or a VIDEO_TS directory
    print(dvd.is_scrambled)      # True if the disc is CSS-protected

    dvd.seek(16)                 # seek to the Primary Volume Descriptor
    data = dvd.read(1)           # read 1 logical block (2048 bytes), returned as bytes
    print(data[40:72])           # e.g. b'SPONGEBOB_SQUAREPANTS_D1\x00\x00...'
```

To descramble CSS-protected VOB data, seek to the start of each title with `SeekFlag.SEEK_KEY` to obtain its title
key, then read the sectors with `ReadFlag.READ_DECRYPT`. See the docstrings on `DvdCss` and its methods for the full
API, including `seek()`, `read()`, `readv()`, and `open_stream()`.

## Development

This project is managed using [uv](https://docs.astral.sh/uv), an extremely fast Python package and project manager.
Install the latest version of uv before continuing. Development currently requires Python 3.10+.

### Set up

Starting from Zero? Not sure where to begin? Here's steps on setting up this Python project using uv. Note that
uv installation instructions should be followed from the uv Docs: https://docs.astral.sh/uv/getting-started/installation

1. Clone the Repository:
    ```shell
    git clone https://github.com/homemediadb/pydvdcss
    cd pydvdcss
    ```
2. Install the Project with uv:
    ```shell
    uv sync --all-groups
    ```
    This creates a Virtual environment at `.venv` and then installs all project dependencies into the Virtual
    environment. Your System Python environment is not affected at all.
3. Now activate the Virtual environment:
    ```shell
    .venv\Scripts\activate
    ```
    (or `source .venv/bin/activate` on macOS and Linux)

    Note:
    - You can alternatively just prefix `uv run` to any command you wish to run under the Virtual environment.
    - I recommend entering the Virtual environment and all further instructions will have assumed you did.
    - JetBrains PyCharm and Visual Studio Code both detect the `.venv` Virtual environment automatically.
    - For more information, see: https://docs.astral.sh/uv/concepts/projects/
4. Install Pre-commit tooling to ensure safe and quality commits:
    ```shell
    uv tool install pre-commit --with pre-commit-uv --force-reinstall
    pre-commit install
    ```

Now feel free to work on the project however you like, all code will be checked before committing.

### Building Source and Wheel distributions

    uv build

You can optionally specify `--sdist` or `--wheel` to build that distribution only.
Built files can be found in the `/dist` directory.

## License

This project is licensed under the terms of the [GNU General Public License, Version 3.0](https://github.com/homemediadb/pydvdcss/blob/master/LICENSE).

* * *

© rlaphoenix 2020-2026
