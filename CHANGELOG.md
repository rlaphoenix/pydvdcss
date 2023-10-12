# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.0] - 2023-10-12

## Added

- Added function `open_stream()` that calls the `dvdcss_open_stream` function of the libdvdcss library.
- Defined `dvdcss_stream_cb`, `pf_seek`, `pf_read`, `pf_readv`, and `dvdcss_open_stream`.

## Changed

- Various structural and organisational changes to the repository, CI/CD, and more.
- Updated dependencies as far as I could while keeping support for actively supported versions of Python.
- Moved all documentation dependencies from dev to main group as optionals installed through the `docs` extra.

## Removed

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
