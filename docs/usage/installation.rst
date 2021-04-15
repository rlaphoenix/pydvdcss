Installation
============

This part of the documentation covers the installation of pydvdcss.
The first step to using any software package is getting it properly installed.

The simplest and most recommended method of installation would be :ref:`From PIP/PyPI`.

From PIP/PyPI
---------------------------------

.. code-block:: shell

    $ python -m pip install --user pydvdcss

From Source Code
---------------------------

.. code-block:: shell

    $ git clone https://github.com/rlaphoenix/pydvdcss
    $ cd pydvdcss
    $ python -m pip install --user .

Note however that there are some caveats when installing from Source Code:

- Source Code may have changes that are not yet tested or stable, and may have regressions.
- Only install from Source-code if you have a reason, e.g. to test changes.
- Requires `Poetry <https://python-poetry.org/docs/#installation>`_ as it's used as the build system backend.
