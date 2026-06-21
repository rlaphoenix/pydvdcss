# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.0] - 2026-06-21

This version is all about improving the UX and overhauling the tooling. Project management
has moved from Poetry to uv with a Hatchling build backend, the supported Python versions
are now 3.10 through 3.14, and all dependencies have been updated. The Sphinx documentation
has been retired in favour of the README. The Windows wheels now bundle libdvdcss, so it no
longer needs to be installed separately there.

### Added

- Implemented `libdvdcss.dvdcss_readv()` as `DvdCss.readv()` for vectored reads into
  multiple buffers in a single call. Create buffers with `create_string_buffer(b"", 2048)`
  (each a non-zero multiple of a sector) and pass them as arguments; on success each is
  filled with consecutive sectors, readable from its `raw` property. Pass
  `flag=ReadFlag.READ_DECRYPT` to descramble VOB data as it is read.
- A `py.typed` marker (PEP 561) so downstream type checkers use the inline type hints
  shipped with the package.
- `DvdCss`, the `SeekFlag` and `ReadFlag` enums, `DvdCssStreamCb`, and all exception
  classes are now importable directly from the `pydvdcss` package root, e.g.
  `from pydvdcss import DvdCss, SeekFlag, ReadError`.
- The Windows wheels now **bundle** a precompiled `libdvdcss-2.dll` (© VideoLAN,
  GPL-2.0-or-later, sourced and SHA-256-verified from allienx/libdvdcss-dll), so
  `pip install pydvdcss` works out of the box on Windows. The pure wheel and source
  distribution remain unbundled and rely on a system-installed libdvdcss. See
  THIRD-PARTY-NOTICES.md for attribution and the GPL source offer.

### Fixed

- The local library search now also finds a `.dylib` (macOS) next to the package, and
  loads the actual matched file. Previously it only checked `.dll`/`.so` and then passed
  the suffix-less path to `CDLL()`. It now also looks inside the package directory itself
  (for the bundled DLL) before falling back to a system-installed library.
- Various CI and linting tooling mistakes and made it more efficient.
- `DvdCss.error` now returns None or string values instead of a useless integer value,
  as the `dvdcss_error` binding was wrongly declared with an `int` return type.
- `DvdCss.error` now decodes the libdvdcss error string with `errors="replace"`, so a
  malformed (non-UTF-8) error message no longer raises `UnicodeDecodeError` and masks the
  underlying failure.
- The `pf_read` callback of `DvdCssStreamCb` now uses a `c_void_p` (writable address) buffer
  instead of `c_char_p`. ctypes hands a callback a `c_char_p` argument as immutable bytes, so the
  callback could not write the read data into the buffer. This was a blocker for `open_stream()`.
- `DvdCss.open_stream()` now passes the `dvdcss_stream_cb` struct by reference. The
  `dvdcss_open_stream` C function takes a `dvdcss_stream_cb *`, but the struct was passed
  by value, so the callbacks were never reachable by libdvdcss. The docstring's note about
  this never working has been replaced with the actual requirement: `p_stream` must be non-zero.

### Changed

- `DvdCss.open_stream()` now validates `p_stream`, raising a `TypeError` if it isn't an
  int and a `ValueError` if it is `0`, which libdvdcss rejects.
- The type aliases module `pydvdcss.types` was renamed to `pydvdcss._types` to mark it
  internal and to avoid shadowing the standard library `types` module.
- Switched project management and the build backend from Poetry to uv with Hatchling.
- Now supports Python 3.10 through 3.14 (previously 3.8 through 3.11).
- Updated all dependencies, and switched development tooling (CI/CD, pre-commit) to uv.
- Various doc-strings were improved and made more clear in various ways.
- Most PyDvdCss-inherited exceptions now try to call `DvdCss.error()` for you to
  include potentially useful error information when the errors happen. Though, Errors
  from the library are not always available.
- The base exception `PyDvdCssException` was renamed to `PyDvdCssError`.
- The exception `LibDvdCssNotFound` was renamed to `LibraryNotFoundError`.
- `DvdCss.close()` now only returns True if a device was actually closed when called.
- `DvdCss.error()` is now a property, via `@property` decorator.
- `DvdCss.error` will now return None if no DVD device or directory was opened yet.
- `DvdCss.error` may now return None if there is no error string to return, or if
  the error string is falsey (basically empty).
- `DvdCss.error` now does whitespace stripping on both the left and right instead
  of just the right.
- `DvdCss.is_scrambled()` is now a property, via `@property` decorator.
- `DvdCss.is_scrambled` will now return False if no DVD device or directory was opened yet.
- `DvdCss.open()` changed parameter names from `psz_target` to `target`.
- `DvdCss.open()` now also accepts any `os.PathLike` object (e.g. a `pathlib.Path`) for
  `target`, not just a `str`.
- `DvdCss.open()` now normalises a bare Windows drive root given with a trailing slash
  (e.g. `"G:/"`) to `"G:"`, which libdvdcss otherwise rejects. Only the drive-root form
  is touched; real file, ISO, and directory paths are left untouched.
- `DvdCss.seek()` changed parameter names from `i_blocks` to `sector` and `i_flags` to
  `flag`.
- `DvdCss.read()` changed parameter names from `i_blocks` to `sectors` and `i_flags` to
  `flag`.
- `DvdCss.seek()` now uses a `SeekFlag` enum for the `flag` parameter instead of an
  integer value. However, you can still use an int if you prefer.
- `DvdCss.read()` now uses a `ReadFlag` enum for the `flag` parameter instead of an
  integer value. However, you can still use an int if you prefer.
- `DvdCss.open()` and `DvdCss.open_stream()` now raises an `AlreadyInUseError` exception
  instead of a `ValueError` when you try to open a 2nd disc in the same class instance.
- `DvdCss.open()` and `DvdCss.open_stream()` now raises an `OpenFailureError` exception
  instead of returning -1 on failure to open and initialize the device or directory.
- `DvdCss.seek()` and `DvdCss.read()` now raises a `NoDeviceError` exception when called
  if no DVD device or directory was opened yet.
- `DvdCss.seek()` now raises a `SeekError` exception instead of returning negative
  numbers on seek failures.
- `DvdCss.read()` now raises a `ReadError` exception instead of an `IOError` on failure
  to read one or more sectors.
- `DvdCss.close()` now raises a `CloseError` exception instead of a `ValueError` on
  failure to close an open device or directory.
- The list of possible library names were put into constants as `LIBRARY_NAMES`.

### Removed

- The `DvdCss.dispose()` method. Use `DvdCss.close()` instead. It only differed from
  `close()` by also resetting the `DVDCSS_VERBOSE` and `DVDCSS_METHOD` environment
  variables, which is undesirable as those are process-global, not per-instance.
- The Sphinx documentation system and Read the Docs configuration. The relevant information
  (installation, features, and a usage example) now lives in the README.
- The DeepSource configuration.
- The `SECTOR_SIZE`, `BLOCK_BUFFER`, `NO_FLAGS`, `READ_DECRYPT`, `SEEK_MPEG`,
  `SEEK_KEY`, `flags_m`, and `flags_s` class variables were removed. The variables to
  do with flags/read/seek were refactored as SeekFlag and ReadFlag.

## [1.4.0] - 2023-10-12

### Added

- Added function `open_stream()` that calls the `dvdcss_open_stream` function of the libdvdcss library.
- Defined `dvdcss_stream_cb`, `pf_seek`, `pf_read`, `pf_readv`, and `dvdcss_open_stream`.

### Changed

- Various structural and organisational changes to the repository, CI/CD, and more.
- Updated dependencies as far as I could while keeping support for actively supported versions of Python.
- Moved all documentation dependencies from dev to main group as optionals installed through the `docs` extra.

### Removed

- Dropped support for Python 3.5, 3.6, and 3.7. This is to have support for the latest dependency versions.
- Removed all uses of poetry-dynamic-versioning as it's simply unnecessary.

## [1.3.2] - 2021-04-18

### Added

- Added custom base exception `PyDvdCssException` which will be used for all custom pydvdcss exceptions.

### Changed

- A custom exception `LibDvdCssNotFound` is now raised when a shared library `.so`/`.dll` was not found.
- Define library prototypes directly instead of opening CFUNCTYPE functions. This reduces the amount of objects and
  memory used up by each DvdCss() object.

### Fixed

- Also check for local libdvdcss shared library `.so` files relative to the project.

## [1.3.1] - 2021-04-17

### Fixed

- Fix no library found check, the local libdvdcss shared library `.so`/`.dll` search set the dll path to the temporary
  search path whether it existed or not, therefore if none of them ever existed it would still have finished with a
  path set to the `dll` variable, making the rest of the code think it found a library.

## [1.3.0] - 2021-04-16

### Added

- Sphinx documentation to /docs and automated builds with ReadTheDocs at https://pydvdcss.readthedocs.io
- Added dunamai dependency for use in the Documentation.
- Added poetry-dynamic-versioning dependency for automating the package version listed in pyproject.
- The libdvdcss shared library `.so`/`.dll` files are now also searched locally relative to the project.

### Changed

- Exceptions raised when loading the library is now bubbled up instead of absorbed and ignored.
- Create buffer with a default of an empty byte-string in `read()` so if libdvdcss reads nothing, we get `b''` instead
  of `b'\x00' * size`.
- Raise an IOError if libdvdcss read less than 0 bytes (an error result).
- `read()` now returns the read bytes instead of how many bytes were read.

### Removed

- Removed leftover print() statement used during debugging.

### Fixed

- Discard handle if libdvdcss returns a handle of `0`, returns `-1`.
- Fix ctype used for the handle, change from `c_long` to `c_void_p`.
- Remove `buffer` and the `buffer_len` check, always use a new buffer when reading. This is to avoid potentially taking
  the previous buffer contents and overwriting it with < buffer size, resulting in the end bytes keeping the old data
  instead of x00, or just no bytes at all there, or just the wrong entire buffer of data.

## [1.2.0] - 2021-04-15

### Added

- Added support for Python 3.5.
- Added import shortcut for DvdCss class to the package `__init__`, allowing `from pydvdcss import DvdCss`.
- Added Type-hinting for parameters and returns, doc-strings were improved.

### Changed

- Migrated from setuptools to Python Poetry.
- `set_verbosity()` now returns an integer value; -1 when Unsetting the cracking mode.
- `open()` now raises a ValueError if you try opening a DVD device/target when one is already open.

### Fixed

- Fixed memory leak by clearing the buffer in `close()`.
- Fixed runtime error by ensuring the libdvdcss handle exists before attempting to close in `close()`.

## [1.1.0] - 2020-10-10

### Changed

- Renamed PyDvdCss class to DvdCss and moved it from `__init__.py` to `dvdcss.py`, so that it isn't executed during
  installation.

## [1.0.7] - 2020-06-17

### Added

- Add error handling when loading the libdvdcss shared library.

## [1.0.6] - 2020-06-16

### Added

- Added methods to set `DVDCSS_VERBOSE` and `DVDCSS_METHOD` environment variables.
- Reset `DVDCSS_VERBOSE` and `DVDCSS_METHOD` on dispose.

## [1.0.5] - 2020-06-16

### Fixed

- Disposed of open handle when trying to open a new one when one is already opened.

## [1.0.4] - 2020-06-16

### Added

- Multiple library/filenames to try and find when loading the libdvdcss shared library/dll.
- Error handling if the library could not be found.
- Installation instructions/tips for Windows, Mac, and Linux.

## [1.0.3] - 2020-06-16

- Effectively skipped and is a lesser duplicate of [1.0.4].

### Added

- Added extra checks

## [1.0.2] - 2020-06-15

### Added

- Added `dispose()` method to clear libdvdcss handles and memory.

### Fixed

- Close open libdvdcss handles and memory on exit of a `with ...:` statement (or anything that runs `__exit__`).

## [1.0.1] - 2020-06-15

### Fixed

- Fix ctypes.util import.
- Fix a small type error in the README's Quick Usage.

## [1.0.0] - 2020-06-15

Initial release.

[1.5.0]: https://github.com/homemediadb/pydvdcss/releases/tag/v1.5.0
[1.4.0]: https://github.com/homemediadb/pydvdcss/releases/tag/v1.4.0
[1.3.2]: https://github.com/homemediadb/pydvdcss/releases/tag/v1.3.2
[1.3.1]: https://github.com/homemediadb/pydvdcss/releases/tag/v1.3.1
[1.3.0]: https://github.com/homemediadb/pydvdcss/releases/tag/v1.3.0
[1.2.0]: https://github.com/homemediadb/pydvdcss/releases/tag/v1.2.0
[1.1.0]: https://github.com/homemediadb/pydvdcss/releases/tag/v1.1.0
[1.0.7]: https://github.com/homemediadb/pydvdcss/releases/tag/v1.0.7
[1.0.6]: https://github.com/homemediadb/pydvdcss/releases/tag/v1.0.6
[1.0.5]: https://github.com/homemediadb/pydvdcss/releases/tag/v1.0.5
[1.0.4]: https://github.com/homemediadb/pydvdcss/releases/tag/v1.0.4
[1.0.3]: https://github.com/homemediadb/pydvdcss/releases/tag/v1.0.3
[1.0.2]: https://github.com/homemediadb/pydvdcss/releases/tag/v1.0.2
[1.0.1]: https://github.com/homemediadb/pydvdcss/releases/tag/v1.0.1
[1.0.0]: https://github.com/homemediadb/pydvdcss/releases/tag/v1.0.0
