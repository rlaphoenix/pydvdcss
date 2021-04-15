# Release History

## 1.2.0

**Fixes**

- Some typos have been fixed here and there.
- The `type` argument for `DvdCss.__exit__` has been removed as it was shadowing the builtin `type`.
- set_verbosity now returns an int rather than a str value, or potentially a `None` value. It will always return either an int or -1 to represent None, which is more akin to the param input.
- close now clears buffer and buffer length and checks if there's a handle before attempting to close it.
- open now checks if a disc is already opened and if so, does not allow you to open until you close or dispose.
- Removed the Python Implementation PyPy trove classifier. This project doesn't use PyPy.
- Updated HISTORY to include changes for 1.1.0, which I forgot to do.

**Improvements**

- Python 3.5 support by removing all uses of f-strings.
- Add to DeepSource; Badge added to README.
- README re-worked, all HTML tags removed or replaced with Markdown. Positioning of information moved around for better readability.
- Ko-fi references, badges, and links removed. I don't accept any donations from Ko-fi anymore.
- Python 3.9 build tests added to GitHub Actions. Renamed the action from "Version tests" to "Build" for a shorter badge.
- DvdCss now imported into `__init__.py` allowing faster and shorter import paths for the user. E.g. `from pydvdcss import DvdCss` instead of `from pydvdcss.dvdcss import DvdCss`.
- Type-hinting has been added where applicable to both params and returns.
- Some doc-strings have been shortened or generally improved for readability; Some new ones have also been added.
- Library DLL loading code is now moved to its own function _load_library().
- Installation function has been renamed to _installation() to signify that it's intended to be used internally only.
- Use Python-Poetry instead of Setuptools. This is for it's easier configuration via pyproject and it's better CLI UX.

## 1.1.0

**Fixes**

- Small typo on libdvdcss install instructions.

**Improvements**

- Move PyDvdCss class from __init__.py to its own file, dvdcss.py so that it isn't executed during installation.
- Rename PyDvdCss class to DvdCss, as the class isn't pydvdcss, the package is.
- Clean up the libdvdcss dll/so installation instructions and be less specific on required versions on Windows instructions.

## 1.0.7

**Improvements**

- Add handler for failed ctypes cdll call

## 1.0.6

**Improvements**

- Add functions to set DVDCSS_VERBOSE and DVDCSS_METHOD environment variables.
- Reset DVDCSS_VERBOSE and DVDCSS_METHOD on dispose.

## 1.0.5

**Bugfixes**

- When using `open()` make sure there's no handle in use, if there is, dispose it first. This ensures handle isnt stuck in memory purgatory.

## 1.0.4

**Improvements**

- Add libdvdcss installation instructions for Windows, Mac, and Linux

## 1.0.3

**Improvements**

- Add extra checks for ctypes find_library call in case one isn't found

**Bugfixes**

- Add handler for failed ctypes find_library call

## 1.0.2

**Improvements**

- Implement `dispose()` function to deal with disposing
- Have `__exit__` call `dispose()` so that `with` calls dispose properly
- Clear the buffer in `dispose()`

## 1.0.1

**Bugfixes**

- Fix ctypes.util import
- Fix a small type error in the README's Quick Usage

## 1.0.0

- Initial release
