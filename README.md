<span align="center">

![Banner](banner.png?raw=true)

</span>

---

<p>&nbsp;</p><p>&nbsp;</p>

<p align="center"><strong>pydvdcss</strong> is a python wrapper for VideoLAN's <a href="https://www.videolan.org/developers/libdvdcss.html">libdvdcss</a></p>

<p>&nbsp;</p><p>&nbsp;</p>

    from pydvdcss import PyDvdCss

    # ...

    # choose device
    dev = "/dev/sr0"

    # create instance
    dvdcss = PyDvdCss()

    # use `with` to auto dispose once you leave the tree
    # of course you can also just do `dvdcss = PyDvdCss()`
    with PyDvdCss() as dvdcss:

      # open device
      dvdcss.open(dev)

      # check if dvd is scrambled
      if dvdcss.is_scrambled():
        print("The DVD is scrambled!")
      
      # read volume id from sector 16
      dvdcss.seek(16)       # seek to sector 16
      dvdcss.read(1)        # read only one sector
      data = dvdcss.buffer  # access the latest read data
      volume_label = data[40:72].strip().decode()
      print(f"{dev}: {volume_label}")
      # >> eg. `'/dev/sr0: THE_IT_CROWD_DISC_1'`
    
    # make sure you dispose when your done if you didn't
    # use `with`, otherwise stuff will get stuck in memory.
    # usage of `with` on pydvdcss automatically handles disposing.
    # dvdcss.dispose()

<p>&nbsp;</p><p>&nbsp;</p>

---

<p>&nbsp;</p><p>&nbsp;</p>

`libdvdcss` is a simple library designed for accessing DVDs like a block device without having to bother about the decryption. `pydvdcss` exposes this library as a class taking care of the rest.

<p>&nbsp;</p><p>&nbsp;</p>

<span align="center">

[![Pull requests welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](http://makeapullrequest.com)
[![GPLv3 license](https://img.shields.io/badge/license-GPLv3-blue)](https://github.com/rlaPHOENiX/pydvdcss/blob/master/LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/pydvdcss)](https://pypi.python.org/pypi/pydvdcss)
[![Python versions](https://img.shields.io/pypi/pyversions/pydvdcss)](https://pypi.python.org/pypi/pydvdcss)
[![PyPI status](https://img.shields.io/pypi/status/pydvdcss)](https://pypi.python.org/pypi/pydvdcss)
[![Contributors](https://img.shields.io/github/contributors/rlaPHOENiX/pydvdcss)](https://github.com/rlaPHOENiX/pydvdcss/graphs/contributors)
[![GitHub issues](https://img.shields.io/github/issues/rlaPHOENiX/pydvdcss)](https://github.com/rlaPHOENiX/pydvdcss/issues)
![Python version tests](https://github.com/rlaPHOENiX/pydvdcss/workflows/Version%20tests/badge.svg?branch=master)

[![Support me on ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/W7W01KX2G)

</span>

<p>&nbsp;</p><p>&nbsp;</p>

## Features

**Portability**

Anything that can run the supported python versions shown above is supported.

**Simplicity**

A DVD player can be built around the `libdvdcss` API using no more than 4 or 5 library calls.

**Freedom**

`libdvdcss` and this wrapper `pydvdcss` are released under the General Public License, ensuring it will stay free, and used only for free software products.

**Just better**

Unlike most similar projects, `libdvdcss` does not require the region of your drive to be set.

<p>&nbsp;</p><p>&nbsp;</p>

# Installation

    python -m pip install --user pydvdcss

or

    git clone https://github.com/rlaPHOENiX/pydvdcss.git
    cd pydvdcss
    python -m pip install --user .

*Note: with the second method you will need to handle updating yourself by re-cloning and installing it again.*

<p>&nbsp;</p><p>&nbsp;</p>

# To-do

- [X] Implement dvdcss_open
- [X] Implement dvdcss_close
- [X] Implement dvdcss_seek
- [X] Implement dvdcss_read
- [X] Implement dvdcss_error
- [X] Implement dvdcss_is_scrambled
- [X] Implement `__enter__` and `__exit__` for proper disposing
- [ ] Implement dvdcss_readv
- [ ] Add handlers for failed find_library or cdll calls
- [ ] Add function to set DVDCSS_VERBOSE
- [ ] Add function to set DVDCSS_METHOD

<p>&nbsp;</p><p>&nbsp;</p>

---

<p>&nbsp;</p><p>&nbsp;</p>

<span align="center">

## [PHOENiX](https://github.com/rlaPHOENiX)

## [LICENSE (GPLv3)](https://github.com/rlaPHOENiX/pydvdcss/blob/master/LICENSE)

## [CONTRIBUTORS](https://github.com/rlaPHOENiX/pydvdcss/graphs/contributors)

</span>