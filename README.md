![Banner](banner.png?raw=true)

* * *

![Python version tests](https://github.com/rlaPHOENiX/pydvdcss/workflows/Build/badge.svg?branch=master)
![Python versions](https://img.shields.io/pypi/pyversions/pydvdcss)
[![PyPI version](https://img.shields.io/pypi/v/pydvdcss)](https://pypi.python.org/pypi/pydvdcss)
[![GPLv3 license](https://img.shields.io/badge/license-GPLv3-blue)](https://github.com/rlaPHOENiX/pydvdcss/blob/master/LICENSE)
[![PyPI status](https://img.shields.io/pypi/status/pydvdcss)](https://pypi.python.org/pypi/pydvdcss)
[![GitHub issues](https://img.shields.io/github/issues/rlaPHOENiX/pydvdcss)](https://github.com/rlaPHOENiX/pydvdcss/issues)
[![DeepSource issues](https://deepsource.io/gh/rlaPHOENiX/pydvdcss.svg/?label=active+issues)](https://deepsource.io/gh/rlaPHOENiX/pydvdcss/?ref=repository-badge)
[![Contributors](https://img.shields.io/github/contributors/rlaPHOENiX/pydvdcss)](https://github.com/rlaPHOENiX/pydvdcss/graphs/contributors)

**pydvdcss** is a python wrapper for VideoLAN's [libdvdcss].

[libdvdcss] is a simple library designed for accessing DVDs like a block device without having to bother about the
decryption.

  [libdvdcss]: <https://www.videolan.org/developers/libdvdcss.html>

```py
from pydvdcss.dvdcss import DvdCss

# ...

# choose device
dev = "/dev/sr0"  # e.g. 'E:', `/dev/sr0`, or a path to an ISO file

# use `with` to auto dispose once you leave the tree
# of course you can also just do `dvdcss = DvdCss()`
with DvdCss() as dvdcss:

  # open device
  dvdcss.open(dev)

  # check if dvd is scrambled
  if dvdcss.is_scrambled():
    print("The DVD is scrambled!")

  # read volume id from the ISO 9660 Volume Descriptor Set
  dvdcss.seek(16)       # seek to sector 16, the first 15 sectors are unused by ISO 9660
  dvdcss.read(1)        # read one sector amount of data
  data = dvdcss.buffer  # access the latest read data
  volume_label = data[40:72].strip().decode()
  print("%s: %s" % (dev, volume_label))
  # >> eg. `'/dev/sr0: THE_IT_CROWD_DISC_1'`

# make sure you dispose when your done if you didn't
# use `with`, otherwise stuff will get stuck in memory.
# usage of `with` on DvdCss automatically handles disposing.
# dvdcss.dispose()
```

---

## Features

**Portability**

Anything that can run the supported python versions shown above is supported.

**Simplicity**

A DVD player can be built around the `libdvdcss` API using no more than 4 or 5 library calls.

**Freedom**

`libdvdcss` and this wrapper `pydvdcss` are released under the General Public License, ensuring it will stay free, and used only for free software products.

**Just better**

Unlike most similar projects, `libdvdcss` does not require the region of your drive to be set.

## Installation

from PyPI:

```shell
$ python -m pip install --user pydvdcss
```

or from source-code:

- Source-code may have changes that are not yet tested or stable, and may have regressions.
- Only install from Source-code if you have a reason, e.g. to test changes.
- Requires [Poetry] as it's used as the build system backend.

  [Poetry]: <https://python-poetry.org/docs/#installation>

```shell
$ git clone https://github.com/rlaPHOENiX/pydvdcss.git
$ cd pydvdcss
$ python -m pip install --user .
```

## To-do

- [x] Implement dvdcss_open
- [x] Implement dvdcss_close
- [x] Implement dvdcss_seek
- [x] Implement dvdcss_read
- [x] Implement dvdcss_error
- [x] Implement dvdcss_is_scrambled
- [x] Implement `__enter__` and `__exit__` for proper disposing
- [x] Add handlers for failed find_library calls
- [X] Add handlers for failed cdll calls
- [x] Add instructions for installing libdvdcss
- [x] Add and test support for Windows
- [x] Add and test support for Mac OS
- [x] Add and test support for Linux
- [x] Add function to set DVDCSS_VERBOSE
- [x] Add function to set DVDCSS_METHOD
- [ ] Implement dvdcss_readv, not sure how this would be used or implemented

## Functions

### DvdCss.open(psz_target=[string])

Open a DVD device or directory and return a dvdcss instance.

Initialize the libdvdcss library and open the requested DVD device or directory.
libdvdcss checks whether ioctls can be performed on the disc, and when possible,
the disc key is retrieved.

open() returns a handle to be used for all subsequent libdvdcss calls. If an
error occurred, NULL is returned.

- **psz_target**: target name, e.g. "/dev/hdc" or "E:".

### DvdCss.close()

Close the DVD and clean up the library.

Close the DVD device and free all the memory allocated by libdvdcss.
On return, the dvdcss_t handle is invalidated and may not be used again.

### DvdCss.seek(i_blocks=[int], i_flags=[int;NOFLAGS])

Seek in the disc and change the current key if requested.

This function seeks to the requested position, in logical blocks.
Returns the new position in blocks, or a negative value in case an error
happened.

Tips:

> Use SEEK_MPEG flag when seeking throughout VOB data sectors. It isn't needed
> on the first sector.

> Use SEEK_KEY flag the first time you enter a TITLE. You _can_ always call it
> in VOB data sectors, however it will be unnecessary and cause slowdowns.

- **i_blocks**: absolute block offset to seek to.
- **i_flags**: NOFLAGS by default, or you can specify SEEK_KEY or SEEK_MPEG flags.

### DvdCss.read(i_blocks=[int], i_flags=[int;NOFLAGS])

Read from the disc and decrypt data if requested.

This function reads i_blocks logical blocks from the DVD.
Returns the amount of blocks read, or a negative value in case an error happened.

Tips:

> Get the read contents from the buffer variable of DvdCss instance.

- **i_blocks**: absolute block offset to seek to.
- **i_flags**: NOFLAGS by default, or you can specify the READ_DECRYPT flag.

### DvdCss.error()

Return a string containing the latest error that occurred in the given libdvdcss
instance.

This function returns a constant string containing the latest error that occurred
in libdvdcss. It can be used to format error messages at your convenience in your
application.

Returns a null-terminated string containing the latest error message.

### DvdCss.is_scrambled()

Check if the DVD is scrambled.

Returns True if it's scrambled.

---

## [PHOENiX](https://github.com/rlaPHOENiX)

## [LICENSE (GPLv3)](https://github.com/rlaPHOENiX/pydvdcss/blob/master/LICENSE)

## [CONTRIBUTORS](https://github.com/rlaPHOENiX/pydvdcss/graphs/contributors)
