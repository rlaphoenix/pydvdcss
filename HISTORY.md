# Release History

## 1.3.2

**Fixes**

- Add .so to the local path check, not just .dll.

**Improvements**

- Raise custom exception if libdvdcss shared object file (dll/so) is not found, instead of a regular Exception.
  This allows you to catch that specific exception to handle it yourself if you so wish.
- Condense the libdvdcss installation instruction information to the basics. If the basics aren't enough, the
  user should just Google it at that point.
- Define library prototypes directly instead of opening CFUNCTYPE functions. This reduces the amount of objects
  and memory used up by each DvdCss() object, but also improves the general UX of operating with the library.

## 1.3.1

**Fixes**

- get_library: Fix possible dll check exists error. If no dlls were found, then the local dll path string would be
  what DLL ultimately becomes after the for each loop. Meaning the next `if not dll` check wouldnt be true, and would
  think that DLL was actually found.

## 1.3.0

**Fixes**

- Use githack cdn url for README banner so pages outside of github.com can correctly render the banner.
- Small typos fixed here and there. Some "typos" more like errors, have also been fixed in some docs.
- open: If handle is 0, return -1 and invalidate the handle instead of returning 0 as if it was it's actual handle.
- _load_library: If CDLL fails, let it raise an exception instead of returning None. (don't hide the error info).
- libdvdcss definitions: The handle type should be c_void_p not c_long. This fixes pydvdcss on Windows.
- read: Buffer should have a default of nothing, not \x00*size. Safety fix.
- read: Remove unnecessary buffer_len check and variable. It is no longer wanted nor necessary. Safety fix.
- read: Always create a new buffer, don't use one from previous reads. Removes self.buffer entirely. It *might* cause slowdowns (I really dont know) but it isnt safe to do that. Safety fix.
- read: If read blocks is < 0 value, assume error, raise IOError.

**Improvements**

- Create Sphinx docs in /docs and https://pydvdcss.readthedocs.io/. The doc information is also quite heavily updated pretty much all-round.
- Use dunamai and poetry-dynamic-versioning to automatically handle versions based on git tags.
- _load_library: Add checks for local DLL paths.
- read: Instead of returning count read bytes, return the actual read bytes. If you need the length of read bytes, it's now accurate and possible to len() the return.

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
