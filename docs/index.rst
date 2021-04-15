pydvdcss
==================================================

Release v\ |version|. (:ref:`Installation <installation>`)

.. image:: https://pepy.tech/badge/pydvdcss
    :target: https://pepy.tech/project/pydvdcss

.. image:: https://img.shields.io/pypi/l/pydvdcss.svg
    :target: https://pypi.org/project/pydvdcss/

.. image:: https://img.shields.io/pypi/wheel/pydvdcss.svg
    :target: https://pypi.org/project/pydvdcss/

.. image:: https://img.shields.io/pypi/pyversions/pydvdcss.svg
    :target: https://pypi.org/project/pydvdcss/

**pydvdcss** is a python wrapper for VideoLAN's libdvdcss.

-------------------

**Short example**::

   >>> dvd = DvdCss()
   >>> dvd.open("D:")
   -1333389968
   >>> dvd.is_scrambled()
   True
   >>> dvd.seek(16)
   16
   >>> dvd.read(1)
   1
   >>> dvd.buffer
   b'\x01CD001\x01\x00PC,...'
   >>> dvd.buffer[40:72]
   b'SPONGEBOB_SQUAREPANTS_D1\x00\x00...'
   >>> dvd.close()
   True
   >>> dvd.dispose()
   True

libdvdcss (via pydvdcss) is a simple library designed for accessing DVDs like a
block device without having to bother about the decryption.

Features of libdvdcss
---------------------

* Portability — Currently supported platforms are GNU/Linux, FreeBSD, NetBSD, OpenBSD, Haiku, Mac OS X, Solaris, QNX,
  OS/2, and Windows NT 4.0 SP4 (with IE 5.0) or later.
* Simplicity — A DVD player can be built around the libdvdcss API using no more than 4 or 5 library calls.
* Freedom — libdvdcss is released under the General Public License, ensuring it will stay free, and used only for free
  software products.
* Adaptability — Unlike most similar projects, libdvdcss does not require the region of your drive to be set and will
  try its best to read from the disc even in the case of a region mismatch.

Pages
-----

.. toctree::
   :maxdepth: 2

   installation
   api
   todo
