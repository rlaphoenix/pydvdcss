import ctypes
import ctypes.util
import os
import platform
from typing import Optional


def _installation():
    """Raise dvdcss DLL library installation instructions."""
    err = "PyDvdCss: Unable to locate libdvdcss library, please install it.\n"
    if platform.system() == "Windows":
        err += "\n".join([
            "On Windows, the installation process is a bit annoying, so I calculated it all for you:",
            "Find or compile the latest libdvdcss DLL for Windows, then place the file in:",
            "`C:/Windows/%s`" % ("SysWOW64" if platform.machine().endswith("64") else "System32"),
            "Done!"
        ])
    elif platform.system() == "Darwin":
        err += "\n".join([
            "On Mac, the installation process is easiest when using `brew`.",
            "If you don't have brew installed, follow the instructions at `https://brew.sh`",
            "Once installed, open terminal and type: `brew install libdvdcss`",
            "Done!"
        ])
    elif platform.system() == "Linux":
        err += "\n".join([
            "On Linux, the installation process is very simple.",
            "Just check your Package Distribution for `libdvdcss`.",
            "If it's not found, check it's User Repository or compile it yourself.",
            "If you compile it yourself, make sure it's somewhere in PATH for pydvdcss to find it.",
            "pydvdcss uses ctypes.util.find_library to search for the library.",
            "It uses `/sbin/ldconfig`, `gcc`, `objdump` and `ld` to try find the library.",
            "Good luck!"
        ])
    raise EnvironmentError(err)


def _load_library() -> Optional[ctypes.CDLL]:
    """Load dvdcss DLL library via ctypes CDLL if available."""
    dlls = ["dvdcss", "dvdcss2", "libdvdcss", "libdvdcss2", "libdvdcss-2"]
    dll = None
    for dll_name in dlls:
        dll = ctypes.util.find_library(dll_name)
        if dll:
            break
    if not dll:
        return None
    try:
        return ctypes.CDLL(dll)
    except OSError:
        return None


class DvdCss:
    """
    Python wrapper for VideoLAN's libdvdcss.
    https://www.videolan.org/developers/libdvdcss.html

    libdvdcss is part of the VideoLAN project, which among other things produces
    VLC, a full video client/server streaming solution. VLC can  also be used as
    a standalone program to play video streams from a hard disk or a DVD.

    Environment Variables:

        DVDCSS_METHOD={title|disc|key}: method for key decryption
          title: By default the decrypted title key is guessed from the encrypted
              sectors of the stream. Thus it should work with a file as well as
              the DVD device. But decrypting a title key may take too much time
              or even fail. With the title method, the key is only checked at
              the beginning of each title, so it will not work if the key
              changes in the middle of a title.
          disc:  The disc key is cracked first. Afterwards all title keys can be
              decrypted instantly, which allows checking them often.
          key:   The same as the "disc" method if you do not have a file with player
              keys at compile time. If you do, disc key decryption will be faster.
              This is the default method also employed by libdvdcss.

        DVDCSS_VERBOSE={0|1|2}: libdvdcss verbosity
          0: no error messages, no debug messages (this is the default)
          1: only error messages
          2: error and debug messages

    libdvdcss is copyright VideoLAN
    """

    # Constants
    SECTOR_SIZE = 2048  # dvd sector size
    BLOCK_BUFFER = 128  # maximum size of buffer for read()

    # Flags
    NO_FLAGS = 0
    READ_DECRYPT = 1  # Ask read() to decrypt the data it reads.
    SEEK_MPEG = 1  # Tell seek() it's seeking in MPEG data.
    SEEK_KEY = 2  # Ask seek() to check on the sectors title key.

    # Flag int to str conversion arrays for debug and print use
    flags_m = {
        0: "NO_FLAGS",
        1: "READ_DECRYPT"
    }
    flags_s = {
        0: "NO_FLAGS",
        1: "SEEK_MPEG",
        2: "SEEK_KEY",
        3: "SEEK_KEY & SEEK_MPEG"
    }

    # Implement Functions from libdvdcss
    # import libdvdcss if possibly via ctypes CDLL
    LIB = _load_library()
    if not LIB:
        _installation()

    _open = ctypes.CFUNCTYPE(ctypes.c_long, ctypes.c_char_p)(("dvdcss_open", LIB))
    _close = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_long)(("dvdcss_close", LIB))
    _seek = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_long, ctypes.c_int, ctypes.c_int)(("dvdcss_seek", LIB))
    _read = ctypes.CFUNCTYPE(
        ctypes.c_int, ctypes.c_long, ctypes.c_char_p, ctypes.c_int, ctypes.c_int
    )(("dvdcss_read", LIB))
    _error = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_long)(("dvdcss_error", LIB))
    _is_scrambled = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_long)(("dvdcss_is_scrambled", LIB))

    def __init__(self):
        self.handle = None  # libdvdcss device handle
        self.buffer = None  # buffer for read()
        self.buffer_len = 0  # length of self.buffer since we wont be able to len check it

    def __enter__(self):
        return self

    def __exit__(self, *_, **kwargs):
        self.dispose()

    def dispose(self):
        """Close and Dispose all data stored in this instance."""
        self.buffer = None
        self.buffer_len = 0
        if self.handle:
            self.close()
        # reset verbosity and cracking mode environment variables
        self.set_verbosity(-1)
        self.set_cracking_mode("unset")

    def open(self, psz_target: str) -> int:
        """
        Open a DVD device or directory and return a dvdcss instance.

        Initialize the libdvdcss library and open the requested DVD device or directory.
        libdvdcss checks whether ioctls can be performed on the disc, and when possible,
        the disc key is retrieved.

        open() returns a handle to be used for all subsequent libdvdcss calls. If an
        error occurred, NULL is returned.
        """
        if self.handle is not None:
            raise ValueError("DvdCss.open: A DVD is already open in this instance.")
        self.handle = self._open(psz_target.encode())
        return self.handle

    def close(self) -> bool:
        """
        Close the DVD and clean up the library.

        Close the DVD device and free all the memory allocated by libdvdcss.
        On return, the dvdcss_t handle is invalidated and may not be used again.
        """
        if self.handle is not None:
            ret = self._close(self.handle)
            if ret != 0:
                raise ValueError("DvdCss.close: Failed to close device handle: %s" % self.error())
        self.handle = None
        self.buffer = None
        self.buffer_len = 0
        return True

    def seek(self, i_blocks: int, i_flags: int = NO_FLAGS) -> int:
        """
        Seek in the disc and change the current key if requested.

        This function seeks to the requested position, in logical blocks.
        Returns the new position in blocks, or a negative value in case an error
        happened.

        - Use SEEK_MPEG flag when seeking throughout VOB data sectors. It isn't needed
          on the first sector.
        - Use SEEK_KEY flag the first time you enter a TITLE. You *can* always call it
          in VOB data sectors, however it will be unnecessary and cause slowdowns.
        """
        return self._seek(self.handle, i_blocks, i_flags)

    def read(self, i_blocks: int, i_flags: int = NO_FLAGS) -> int:
        """
        Read from the disc and decrypt data if requested.

        This function reads i_blocks logical blocks from the DVD.
        Returns the amount of blocks read, or a negative value in case an error happened.

        Tips:
        - Get the read contents from the buffer variable of PyDvdCss instance.
        """
        if self.buffer_len != i_blocks:
            # the current ctypes buffer won't fit the data, resize it
            self.buffer = ctypes.create_string_buffer(i_blocks * self.SECTOR_SIZE)
            self.buffer_len = i_blocks
        return self._read(self.handle, self.buffer, i_blocks, i_flags)

    # def readv(self, p_iovec, i_blocks, i_flags):
    #   TODO: Implement readv, not sure how this would be used or implemented.
    #         It's possible the need for readv via python is simply unnecessary.

    def error(self) -> str:
        """Get the latest error that occurred in the given libdvdcss instance."""
        return self._error(self.handle).rstrip()

    def is_scrambled(self) -> bool:
        """Check if the DVD is scrambled."""
        return self._is_scrambled(self.handle) == 1

    @staticmethod
    def set_verbosity(verbosity: int = 0) -> int:
        """
        Set libdvdcss verbosity (DVDCSS_VERBOSE environment variable).

        Available options are int 0..2
          -1:  Unset/Remove/Reset the cracking mode.
           0:  no error messages, no debug messages (this is the default)
           1:  only error messages
           2:  error and debug messages

        Returns the now current value of DVDCSS_VERBOSE, expected value should be
        the same as the verbosity int provided.
        """
        if verbosity == -1:
            os.unsetenv("DVDCSS_VERBOSE")
            return -1
        os.environ["DVDCSS_VERBOSE"] = str(verbosity)
        return int(os.environ["DVDCSS_VERBOSE"])

    @staticmethod
    def set_cracking_mode(mode="key"):
        """
        Set libdvdcss cracking mode (DVDCSS_METHOD environment variable).

        Available options:
          'unset': Unset/Remove/Reset the cracking mode.
          'title': By default the decrypted title key is guessed from the encrypted
                   sectors of the stream. Thus it should work with a file as well as
                   the DVD device. But decrypting a title key may take too much time
                   or even fail. With the title method, the key is only checked at
                   the beginning of each title, so it will not work if the key
                   changes in the middle of a title.
          'disc':  The disc key is cracked first. Afterwards all title keys can be
                   decrypted instantly, which allows checking them often.
          'key':   The same as the "disc" method if you do not have a file with player
                   keys at compile time. If you do, disc key decryption will be faster.
                   This is the default method also employed by libdvdcss.

        Returns the now current value of DVDCSS_METHOD, expected value should be
        the same as the mode string provided.
        """
        if mode == -1:
            os.unsetenv("DVDCSS_METHOD")
            return None
        os.environ["DVDCSS_METHOD"] = mode
        return os.environ["DVDCSS_METHOD"]
