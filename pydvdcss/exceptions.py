class PyDvdCssError(Exception):
    """Base exception for the pydvdcss project."""


class LibraryNotFoundError(PyDvdCssError):
    """The libdvdcss library file (.dll or .so) could not be found."""


class NoDeviceError(PyDvdCssError):
    """No DVD device or directory is opened yet, but is required for this action."""


class AlreadyInUseError(PyDvdCssError):
    """A DVD device or directory is already open, close it first."""


class OpenFailureError(PyDvdCssError):
    """Failed to open the requested DVD device or directory."""


class CloseError(PyDvdCssError):
    """Failed to close the open DVD device or directory."""


class SeekError(PyDvdCssError):
    """Failed to seek to a specific position on the DVD device or directory."""


class ReadError(PyDvdCssError):
    """Failed to read at a specific position on the DVD device or directory."""
