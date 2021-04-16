import os
import platform
from ctypes import CFUNCTYPE, c_void_p, c_int, c_char_p, CDLL, create_string_buffer
from ctypes.util import find_library
from pathlib import Path
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


class DvdCss:
    """
    Python wrapper for VideoLAN's libdvdcss.
    https://www.videolan.org/developers/libdvdcss.html

    libdvdcss is part of the VideoLAN project, which among other things produces
    VLC, a full video client/server streaming solution. VLC can  also be used as
    a standalone program to play video streams from a hard disk or a DVD.

    The Environment Variables `DVDCSS_METHOD` and `DVDCSS_VERBOSE` are handled
    by :func:`set_cracking_mode` and :func:`set_verbosity` respectively. See
    those functions for more information.

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

    def __init__(self):
        self.handle = None  # libdvdcss device handle

        self._library = self._load_library()
        if not self._library:
            _installation()

        self._open = CFUNCTYPE(c_void_p, c_char_p)(("dvdcss_open", self._library))
        self._close = CFUNCTYPE(c_int, c_void_p)(("dvdcss_close", self._library))
        self._seek = CFUNCTYPE(c_int, c_void_p, c_int, c_int)(("dvdcss_seek", self._library))
        self._read = CFUNCTYPE(c_int, c_void_p, c_char_p, c_int, c_int)(("dvdcss_read", self._library))
        self._error = CFUNCTYPE(c_int, c_void_p)(("dvdcss_error", self._library))
        self._is_scrambled = CFUNCTYPE(c_int, c_void_p)(("dvdcss_is_scrambled", self._library))

    def __enter__(self):
        return self

    def __exit__(self, *_, **kwargs):
        self.dispose()

    @staticmethod
    def _load_library() -> Optional[CDLL]:
        """Load dvdcss DLL library via ctypes CDLL if available."""
        dlls = ["dvdcss", "dvdcss2", "libdvdcss", "libdvdcss2", "libdvdcss-2"]
        dll = None
        for dll_name in dlls:
            dll = find_library(dll_name)
            if dll:
                break
            local_path = (Path(__file__).parent.parent / dll_name).with_suffix(".dll")
            if local_path.exists():
                dll = str(local_path)
                break
        if not dll:
            return None
        return CDLL(dll)

    def dispose(self):
        """
        Closes any open disc and frees all data stored in this instance.
        It also unsets the libdvdcss verbosity and cracking mode.

        This should be run when you intend to re-use the object for a new
        disc and want to start fresh.

        If you simply want to open a new disc with the same settings and
        environment, run :func:`close` instead.
        """
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

        Parameters:
            psz_target: A block device string, e.g. "E:", "/dev/sr0", an ISO image file,
                or a VOB/IFO structure directory.

        Returns a handle to be used for all subsequent libdvdcss calls.
        If an error occurred, NULL is returned.
        """
        if self.handle is not None:
            raise ValueError("DvdCss.open: A DVD is already open in this instance.")
        self.handle = self._open(psz_target.encode())
        if self.handle == 0:
            self.handle = None
            return -1
        return self.handle

    def close(self) -> bool:
        """
        Close the DVD by freeing the dvdcss memory and handle of the block device.
        It also clears the local data buffer.

        This should always be run once you are finished with the opened disc, even
        if you don't intend to open another disc in the same instance.
        """
        if self.handle is not None:
            ret = self._close(self.handle)
            if ret != 0:
                raise ValueError("DvdCss.close: Failed to close device handle: %s" % self.error())
        self.handle = None
        return True

    def seek(self, i_blocks: int, i_flags: int = NO_FLAGS) -> int:
        """
        Seeks to the requested position of the disc, in logical blocks.

        Parameters:
            i_blocks: Position in logical blocks (2048*n) to seek to.
            i_flags: NO_FLAGS by default, or you can specify SEEK_MPEG or SEEK_KEY flags.

        Returns the new position in blocks, or a negative value if an error
        occurred.

        - Use SEEK_MPEG flag when seeking throughout VOB data sectors. It isn't needed
          on the first sector.
        - Use SEEK_KEY flag the first time you enter a TITLE. You *can* always call it
          in VOB data sectors, however it will be unnecessary and cause slowdowns.

        """
        return self._seek(self.handle, i_blocks, i_flags)

    def read(self, i_blocks: int, i_flags: int = NO_FLAGS) -> bytes:
        """
        Read from the disc and decrypt data if requested.

        Parameters:
            i_blocks: Number of logical blocks (2048*n) to read.
            i_flags: NO_FLAGS by default, or you can specify the READ_DECRYPT flag.

        Returns the read logical blocks, or raises an IOError if a reading error occurs.
        """
        buffer = create_string_buffer(b'', i_blocks * self.SECTOR_SIZE)
        read = self._read(self.handle, buffer, i_blocks, i_flags)
        if read < 0:
            raise IOError("DvdCss.read: An error occurred while reading: %s" % self.error())
        return buffer.raw[:read * self.SECTOR_SIZE]

    # def readv(self, p_iovec, i_blocks, i_flags):
    #   TODO: Implement readv, not sure how this would be used or implemented.
    #         It's possible the need for readv via python is simply unnecessary.

    def error(self) -> str:
        """Returns the latest error that occurred in the given libdvdcss instance."""
        return self._error(self.handle).rstrip()

    def is_scrambled(self) -> bool:
        """Check if the disc is scrambled."""
        return self._is_scrambled(self.handle) == 1

    @staticmethod
    def set_verbosity(verbosity: int = 0) -> int:
        """
        Set libdvdcss verbosity (DVDCSS_VERBOSE environment variable).

        - -1: Unset the DVDCSS_VERBOSE environment variable.
        -  0: No error messages, no debug messages (this is the default).
        -  1: Only error messages.
        -  2: Error and debug messages.

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

        - unset: Unset the DVDCSS_METHOD environment variable.
        - title: By default the decrypted title key is guessed from the encrypted
          sectors of the stream. Thus it should work with a file as well as
          the DVD device. But decrypting a title key may take too much time
          or even fail. With the title method, the key is only checked at
          the beginning of each title, so it will not work if the key
          changes in the middle of a title.
        - disc: The disc key is cracked first. Afterwards all title keys can be
          decrypted instantly, which allows checking them often.
        - key: The same as the "disc" method if you do not have a file with player
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
