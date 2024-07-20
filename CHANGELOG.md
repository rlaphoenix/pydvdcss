# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

This version is all about improving the UX and upgrading it's tooling. Support for
Python 3.8 has been dropped, but 3.12 is now supported. Unfortunately this means
dropping support for Windows 7/8/8.1 as well. This was more or less necessary to keep
up with the latest versions of other dependencies as well as crucial bug fixes.

### Added

- Implemented `libdvdcss.dvdcss_readv()` to `DvdCss.readv()`. Simply create buffers
  using `create_string_buffer(b"", 2048)` and pass them as arguments. Read data will
  go into the original buffers made. You can read the bytes from the `raw` property
  of each string buffer.

### Fixed

- Various CI and linting tooling mistakes and made it more efficient.

### Changed

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
- `DvdCss.read()` now raises a `SeekError` exception instead of a negative integer when
  it fails to seek.
- `DvdCss.read()` now raises a `ReadError` exception instead of an `IOError` on failure
  to read one or more sectors.
- `DvdCss.close()` now raises a `CloseError` exception instead of a `ValueError` on
  failure to close an open device or directory.
- `DvdCss.dispose()` is now deprecated and an alias of `DvdCss.close()` and no longer
  unsets the verbosity level or cracking mode environment variables. This is because
  it cant actually work (see Removed section), and even if it did it is set in your
  environment, not per-instance. Its not logical to reset it when it will affect every
  other instance running.
- The list of possible library names were put into constants as `LIBRARY_NAMES`.

### Removed

- The `SECTOR_SIZE`, `BLOCK_BUFFER`, `NO_FLAGS`, `READ_DECRYPT`, `SEEK_MPEG`,
  `SEEK_KEY`, `flags_m`, and `flags_s` class variables were removed. The variables to
  do with flags/read/seek were refactored as SeekFlag and ReadFlag.
- The `DvdCss.set_verbosity()` and `DvdCss.set_cracking_mode()` methods as it is not
  actually possible to set the environment variable from Python in such a way for the
  library to see the changes. I've tried manipulating os.environ, setx, py-setenv, and
  pycrosskit. Nothing set it persistently for the current terminal/shell in such a way
  without needing the terminal/shell to reload, making this method pointless.

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

[1.4.0]: https://github.com/rlaphoenix/pydvdcss/releases/tag/v1.4.0
[1.3.2]: https://github.com/rlaphoenix/pydvdcss/releases/tag/v1.3.2
[1.3.1]: https://github.com/rlaphoenix/pydvdcss/releases/tag/v1.3.1
[1.3.0]: https://github.com/rlaphoenix/pydvdcss/releases/tag/v1.3.0
[1.2.0]: https://github.com/rlaphoenix/pydvdcss/releases/tag/v1.2.0
[1.1.0]: https://github.com/rlaphoenix/pydvdcss/releases/tag/v1.1.0
[1.0.7]: https://github.com/rlaphoenix/pydvdcss/releases/tag/v1.0.7
[1.0.6]: https://github.com/rlaphoenix/pydvdcss/releases/tag/v1.0.6
[1.0.5]: https://github.com/rlaphoenix/pydvdcss/releases/tag/v1.0.5
[1.0.4]: https://github.com/rlaphoenix/pydvdcss/releases/tag/v1.0.4
[1.0.3]: https://github.com/rlaphoenix/pydvdcss/releases/tag/v1.0.3
[1.0.2]: https://github.com/rlaphoenix/pydvdcss/releases/tag/v1.0.2
[1.0.1]: https://github.com/rlaphoenix/pydvdcss/releases/tag/v1.0.1
[1.0.0]: https://github.com/rlaphoenix/pydvdcss/releases/tag/v1.0.0
