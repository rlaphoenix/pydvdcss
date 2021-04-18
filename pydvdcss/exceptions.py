class PyDvdCssException(Exception):
    """Base exception for the pydvdcss project."""
    def __init__(self, *args):
        super(PyDvdCssException).__init__(self, *args)


class LibDvdCssNotFound(PyDvdCssException):
    """The library libdvdcss (dll or so) was unable to be found."""
