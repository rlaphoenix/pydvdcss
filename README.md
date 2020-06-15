# pydvdcss

Python wrapper for VideoLAN's libdvdcss.

<p align="center">
<a href="https://python.org"><img src="https://img.shields.io/badge/python-3.6%2B-informational?style=flat-square" /></a>
<a href="https://github.com/rlaPHOENiX/pydvdcss/blob/master/LICENSE"><img alt="license" src="https://img.shields.io/github/license/rlaPHOENiX/pydvdcss?style=flat-square" /></a>
<a href="https://github.com/rlaPHOENiX/pydvdcss/issues"><img alt="issues" src="https://img.shields.io/github/issues/rlaPHOENiX/pydvdcss?style=flat-square" /></a>
<a href="http://makeapullrequest.com"><img alt="pr's welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square" /></a>
<br>
<a href="https://ko-fi.com/W7W01KX2G"><img alt="support me" src="https://www.ko-fi.com/img/githubbutton_sm.svg" /></a>
</p>

## To-do

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

## Quick Installation

    python -m pip install --user pydvdcss

## Quick Usage

    from pydvdcss import PyDvdCss

    # ...

    # choose device
    dev = "/dev/sr0"

    # with handles disposing once you leave the call
    with PyDvdCss as dvdcss:

      # open device
      dvdcss.open(dev)

      # check if dvd is scrambled
      if dvdcss.is_scrambled():
        print("The DVD is scrambled!")
      
      # read volume id from sector 16
      dvdcss.seek(16)  # seek to sector 16
      dvdcss.read(1)   # read only one sector
      volume_label = dvdcss.buffer[40:72].strip().decode()
      print(f"{dev}: {volume_label}")
