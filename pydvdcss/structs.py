from ctypes import CFUNCTYPE, Structure, c_char_p, c_int, c_uint64, c_void_p
from enum import Enum


class SeekFlag(Enum):
    Unset = 0
    SEEK_MPEG = 1
    """Seeking through VOB data sectors. Checks title key in some cases."""
    SEEK_KEY = 2
    """Seeking through title data sectors. Checks title key at seeked position."""


class ReadFlag(Enum):
    Unset = 0
    READ_DECRYPT = 1
    """Decrypt the data it reads."""


class DvdCssStreamCb(Structure):
    """
    Creates a struct to match dvdcss_stream_cb.

    Set of callbacks to access DVDs in custom ways.
    """

    _fields_ = (
        # custom seek callback - int(p_stream, i_pos)
        ("pf_seek", CFUNCTYPE(c_int, c_void_p, c_uint64)),
        # custom read callback - int(p_stream, buffer, i_read)
        ("pf_read", CFUNCTYPE(c_int, c_void_p, c_char_p, c_int)),
        # custom vectored read callback - int(p_stream, p_iovec, i_blocks)
        ("pf_readv", CFUNCTYPE(c_int, c_void_p, c_void_p, c_int)),
    )


__all__ = ("SeekFlag", "ReadFlag", "Iovec", "DvdCssStreamCb")
