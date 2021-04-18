class PyDvdCssException(Exception):
    """Base exception for the pydvdcss project."""


class LibDvdCssNotFound(PyDvdCssException):
    """The library libdvdcss (dll or so) was unable to be found."""
