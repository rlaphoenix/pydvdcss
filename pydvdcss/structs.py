from ctypes import CFUNCTYPE, Structure, c_char_p, c_int, c_uint64, c_void_p
from enum import Enum


class VerbosityLevel(Enum):
    Unset = -1
    """Unset the DVDCSS_VERBOSE environment variable."""
    Nothing = 0
    """Outputs no messages at all."""
    Error = 1
    """Outputs error messages to stderr."""
    Debug = 2
    """Outputs error messages and debug messages to stderr."""


class CrackingMode(Enum):
    Unset = "unset"
    """Unset the DVDCSS_METHOD environment variable."""
    Title = "title"
    """By default the decrypted title key is guessed from the encrypted
    sectors of the stream. Thus it should work with a file as well as
    the DVD device. But decrypting a title key may take too much time
    or even fail. With the title method, the key is only checked at
    the beginning of each title, so it will not work if the key
    changes in the middle of a title."""
    Disc = "disc"
    """The disc key is cracked first. Afterwards all title keys can be
    decrypted instantly, which allows checking them often."""
    Key = "key"
    """The same as the "disc" method if you do not have a file with player
    keys at compile time. If you do, disc key decryption will be faster.
    This is the default method also employed by libdvdcss."""


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


__all__ = ("VerbosityLevel", "CrackingMode", "SeekFlag", "ReadFlag", "DvdCssStreamCb")
