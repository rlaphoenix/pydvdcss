# Release History

## master

- N/A

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