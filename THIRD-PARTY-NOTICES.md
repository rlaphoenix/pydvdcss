# Third-Party Notices

## libdvdcss

The platform-specific (Windows) wheels of **pydvdcss** bundle a precompiled copy
of **libdvdcss** (`libdvdcss-2.dll`). The pure wheel and the source distribution
do **not** bundle it; on those, libdvdcss must be installed on the system.

- Copyright © VideoLAN and its authors.
- Licensed under the **GNU General Public License, version 2 or (at your option)
  any later version** (GPL-2.0-or-later). The full license text is shipped next to
  the bundled library as `LICENSE.libdvdcss`.
- Project / source:
  - <https://www.videolan.org/developers/libdvdcss.html>
  - <https://code.videolan.org/videolan/libdvdcss>
  - Source releases: <https://download.videolan.org/pub/libdvdcss/>
- The bundled Windows binaries are taken, **unmodified**, from the third-party
  build project <https://github.com/allienx/libdvdcss-dll> (also GPL-2.0), and are
  verified by SHA-256 at build time (see `scripts/download_libdvdcss.py`).

### Written offer for source (GPL)

The bundled `libdvdcss-2.dll` is built from the corresponding source of libdvdcss
at the bundled version, available at
<https://download.videolan.org/pub/libdvdcss/>. For at least three years from the
date of distribution, you may also request the complete corresponding source by
opening an issue at <https://github.com/homemediadb/pydvdcss/issues>.

pydvdcss itself is licensed GPL-3.0-only (see `LICENSE`); GPL-2.0-or-later is
compatible with it.
