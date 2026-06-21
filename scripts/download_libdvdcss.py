"""Download a prebuilt Windows ``libdvdcss-2.dll`` for bundling into the wheel.

VideoLAN only publishes libdvdcss *source*, so the Windows binaries are taken,
unmodified, from the third-party (GPL-2.0) project
https://github.com/allienx/libdvdcss-dll. Every download is verified against a
pinned SHA-256. The CD workflow uses this to build the platform-specific Windows
wheels; see the "Bundled libdvdcss" section of the README.
"""

from __future__ import annotations

import argparse
import hashlib
import urllib.request
from pathlib import Path

REPO = "allienx/libdvdcss-dll"
RAW = f"https://raw.githubusercontent.com/{REPO}/main"
DLL_NAME = "libdvdcss-2.dll"
LICENSE_NAME = "LICENSE.libdvdcss"

ARCH_SUBDIR = {"x86_64": "64-bit", "i386": "32-bit"}

# Pinned SHA-256 of the upstream DLLs. Refuse to bundle anything not listed here.
KNOWN_HASHES = {
    ("1.5.0", "x86_64"): (
        "fb6944bc154ddeae570b98fa1d458ea7a8a940c25aca1854ccb28dee6b4e5119"
    ),
    ("1.5.0", "i386"): (
        "669c34173ddb8d5a71f72ad7e9c0accb647fb50a10be732be4382cd4647e6cda"
    ),
}


def _fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "pydvdcss-build"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return bytes(response.read())


def download(version: str, arch: str, dest: Path) -> None:
    expected = KNOWN_HASHES.get((version, arch))
    if expected is None:
        raise SystemExit(
            f"No pinned SHA-256 for libdvdcss {version} {arch}; refusing to bundle an "
            f"unverified binary. Add its hash to KNOWN_HASHES first."
        )

    dll = _fetch(f"{RAW}/{version}/{ARCH_SUBDIR[arch]}/{DLL_NAME}")
    actual = hashlib.sha256(dll).hexdigest()
    if actual != expected:
        raise SystemExit(
            f"SHA-256 mismatch for libdvdcss {version} {arch}:\n"
            f"  expected {expected}\n  got      {actual}"
        )

    dest.mkdir(parents=True, exist_ok=True)
    (dest / DLL_NAME).write_bytes(dll)
    # Ship libdvdcss's GPL-2.0 licence text next to the binary it covers.
    (dest / LICENSE_NAME).write_bytes(_fetch(f"{RAW}/LICENSE"))
    print(f"Downloaded {DLL_NAME} ({version}, {arch}) -> {dest} [sha256 ok]")


def clean(dest: Path) -> None:
    for name in (DLL_NAME, LICENSE_NAME):
        path = dest / name
        if path.exists():
            path.unlink()
            print(f"Removed {path}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Bundle a prebuilt libdvdcss DLL.")
    parser.add_argument("-a", "--arch", choices=sorted(ARCH_SUBDIR), default="x86_64")
    parser.add_argument("-V", "--version", default="1.5.0")
    parser.add_argument("-d", "--dest", type=Path, default=Path("pydvdcss"))
    parser.add_argument(
        "-c",
        "--clean",
        action="store_true",
        help="Remove any bundled library before downloading.",
    )
    parser.add_argument(
        "--clean-only",
        action="store_true",
        help="Only remove the bundled library, do not download.",
    )
    args = parser.parse_args(argv)

    if args.clean or args.clean_only:
        clean(args.dest)
    if not args.clean_only:
        download(args.version, args.arch, args.dest)


if __name__ == "__main__":
    main()
