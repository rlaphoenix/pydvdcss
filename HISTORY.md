# Release History

## master

N/A

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
