from __future__ import annotations

from ctypes import (
    CDLL,
    c_char_p,
    c_int,
    c_void_p,
    create_string_buffer,
)
from ctypes.util import find_library
from pathlib import Path
from typing import Any

from typing_extensions import deprecated

from pydvdcss import constants, exceptions, types
from pydvdcss.structs import (
    DvdCssStreamCb,
    ReadFlag,
    SeekFlag,
)
from pydvdcss.utilities import message_with_error


class DvdCss:
    """
    Unofficial Python wrapper for VideoLAN's libdvdcss:
    https://www.videolan.org/developers/libdvdcss.html

    libdvdcss is part of the VideoLAN portfolio, which among other projects produces
    VLC, a full video client/server streaming solution. VLC can also be used as a
    standalone program to play video streams from a hard disk or a DVD.

    libdvdcss is copyright of VideoLAN and licensed under GNU General Public License.

    Some environment variables can be used to change the behavior of libdvdcss:

    Environment Variables:
      DVDCSS_VERBOSE: Sets the verbosity level.
        - 0 outputs no messages at all.
        - 1 outputs error messages to stderr.
        - 2 outputs error messages and debug messages to stderr.
      DVDCSS_METHOD: Sets the authentication & decryption method to descramble discs.
        - key is the default method. libdvdcss will use a set of calculated player keys
          to try and get the disc key. This can fail if the drive does not recognize any
          of the player keys.
        - disc is a fallback method when key has failed. Instead of using player keys,
          libdvdcss will crack the disc key using a brute force algorithm. This process
          is CPU intensive and requires 64 MB of memory to store temporary data.
        - title is the fallback when all other methods have failed. It does not rely on
          a key exchange with the DVD drive, but rather uses a crypto attack to guess
          the title key. In rare cases this may fail because there is not enough
          encrypted data on the disc to perform a statistical attack, but on the other
          hand it is the only way to decrypt a DVD stored on a hard disc, or a DVD with
          the wrong region on an RPC2 drive.
      DVDCSS_RAW_DEVICE: Specify the raw device to use. Exact usage will depend on
        your operating system, the Linux utility to set up raw devices is raw(8) for
        instance. Please note that on most operating systems, using a raw device
        requires highly aligned buffers: Linux requires a 2048 bytes alignment (which
        is the size of a DVD sector).
      DVDCSS_CACHE: Specify a directory in which to cache title key values. This will
        speed up descrambling of DVDs which are in the cache. The DVDCSS_CACHE directory
        is created if it does not exist, and a subdirectory is created named after the
        DVD's title or manufacturing date. If DVDCSS_CACHE is not set or is empty,
        libdvdcss will use the default value which is "${HOME}/.dvdcss/" under Unix and
        "C:/Documents and Settings/$USER/Application Data/dvdcss/" under Win32. The
        special value "off" disables caching.
    """

    def __init__(self) -> None:
        self.handle: int | None = None
        self._library = self._load_library()

    def __enter__(self) -> DvdCss:
        return self

    def __exit__(self, *_: Any, **__: Any) -> None:
        self.close()

    def open(self, target: str) -> int:
        """
        Open a DVD device or directory.

        libdvdcss checks whether ioctls can be performed on the disc, and when possible,
        the disc key is retrieved.

        If the disc key could be retrieved it will be used to derive title keys when
        seeking without needing to brute or crack. Your player and disc region will
        need to match to be able to obtain the disc key.

        Parameters:
            target: A block device string, e.g. "E:", "/dev/sr0", an ISO image file,
                or a VOB/IFO structure directory.

        Raises:
            OpenFailureError: Failure opening the disc or during post-initialization.
            AlreadyInUseError: If you try to open a 2nd disc without first closing.

        Returns a handle to be used for all subsequent libdvdcss calls.
        """
        if self.handle is not None:
            raise exceptions.AlreadyInUseError(
                "A DVD is already opened, you cannot open another."
            )

        self.handle = self._library.dvdcss_open(target.encode())
        if self.handle == 0:
            self.handle = None
            raise exceptions.OpenFailureError(
                message_with_error(f"Failed to open '{target}'", self.error)
            )

        return self.handle

    def open_stream(self, p_stream: int, p_stream_cb: DvdCssStreamCb) -> int:
        """
        Open a DVD device using custom read and seek functions.

        Essentially instead of having libdvdcss read from a target device,
        you provide it functions that does the reading and seeking yourself.

        Note: I have yet to actually get this to work. I don't know if I'm
        doing something wrong in terms of ctypes definitions or something
        else, but the definitions seem correct. Perhaps p_stream is used in
        a way that I don't yet understand.

        Parameters:
            p_stream: A private handle used by p_stream_cb.
            p_stream_cb: A struct containing seek and read functions.

        Raises:
            OpenFailureError: Failure opening the disc or during post-initialization.
            AlreadyInUseError: If you try to open a 2nd disc without first closing.

        Returns a handle to be used for all subsequent libdvdcss calls.
        If an error occurred, NULL is returned.
        """
        if self.handle is not None:
            raise exceptions.AlreadyInUseError(
                "A DVD is already opened, you cannot open another."
            )

        self.handle = self._library.dvdcss_open_stream(p_stream, p_stream_cb)
        if self.handle == 0:
            self.handle = None
            raise exceptions.OpenFailureError(
                message_with_error(f"Failed to open '{p_stream_cb}'", self.error)
            )

        return self.handle

    def seek(self, sector: int, flag: types.SeekFlag_T = SeekFlag.Unset) -> int:
        """
        Seeks to a position in the DVD device or directory.

        The flag is used to indicate when and how the library should calculate the CSS
        title keys. The keys used to decrypt the VOB data. When and how differs based
        on where you are seeking, when you seek to it, in what order, with what flag,
        and what cracking mode is chosen.

        - Use SeekFlag.SEEK_MPEG when seeking throughout VOB data sectors.
        - Use SeekFlag.SEEK_KEY flag the first time you enter a Title.
        - Otherwise, use SeekFlag.Unset.

        Generally the title key is always calculated when using SEEK_KEY as you seek
        into a title or VOB data sector. However, It may or may not be calculated when
        using SEEK_MPEG as it depends on the VOB, the title, and when/where you may
        have seeked to before-hand. You can use SEEK_KEY when seeking to every sector,
        but it will be wasteful on speed.

        The title key is never calculated when using no flag. You can always use it
        when you know your disc is entirely CSS-free/unprotected. Otherwise, only
        use it when described above, or you may miss calculating a title key.

        Parameters:
            sector: Position in logical blocks (2048*n) to seek to.
            flag: Seeking Flag, used as described above.

        Raises:
            NoDeviceError: No DVD device or directory is open yet.
            SeekError: Failure seeking to the specific logical block.

        Returns the new position in logical blocks (sectors).
        """
        if self.handle is None:
            raise exceptions.NoDeviceError(
                "No DVD device or directory is open yet, use open() first."
            )

        if not isinstance(sector, int):
            raise TypeError(f"Expected sector to be an int, not {sector!r}")

        if isinstance(flag, int):
            flag = SeekFlag(flag)
        elif not isinstance(flag, SeekFlag):
            raise TypeError(
                f"Expected flag to be an int or SeekFlag enum, not {flag!r}"
            )

        new_position = self._library.dvdcss_seek(self.handle, sector, flag.value)
        if new_position < 0:
            raise exceptions.SeekError(
                message_with_error(f"Failed to seek to Sector {sector}", self.error)
            )

        return new_position

    def read(self, sectors: int, flag: types.ReadFlag_T = ReadFlag.Unset) -> bytes:
        """
        Read from the DVD device or directory and decrypt data if requested.

        The flag is used to indicate when the library should decrypt VOB data with it's
        CSS title key.

        - Use ReadFlag.DECRYPT when seeking throughout VOB data sectors.
        - Otherwise, use ReadFlag.Unset.

        You must seek to the start of each title and/or through VOB data sectors to
        get the title keys necessary to descramble/decrypt CSS. This will NOT error
        if you read a scrambled VOB sector with no title key to descramble with.
        Generally, you should seek through the disc first to get the keys, then seek
        back to the start and then begin reading.

        Parameters:
            sectors: Number of logical blocks (2048*n) to read.
            flag: Reading Flag, used as described above.

        Raises:
            NoDeviceError: No DVD device or directory is open yet.
            ReadError: Failure reading sectors, or returned data is less than expected.

        Returns the read logical blocks, or raises an IOError if a reading error occurs.
        """
        if self.handle is None:
            raise exceptions.NoDeviceError(
                "No DVD device or directory is open yet, use open() first."
            )

        if not isinstance(sectors, int):
            raise TypeError(f"Expected sectors to be an int, not {sectors!r}")

        if isinstance(flag, int):
            flag = ReadFlag(flag)
        elif not isinstance(flag, ReadFlag):
            raise TypeError(
                f"Expected flag to be an int or ReadFlag enum, not {flag!r}"
            )

        # TODO: Theoretically it could read less than the expected bytes into the buffer
        #       and then we have NOP bytes as if nothing went wrong.
        #       `buffer size-read_sectors` will not work since the buffer will always
        #       be the correct length, regardless how much dvdcss_read() actually reads.
        #       We are putting faith into dvdcss_read() to always read sectors in full
        #       or dont return a sector at all, but does it work like this?
        buffer = create_string_buffer(b"", sectors * constants.SECTOR_SIZE)

        read_sectors = self._library.dvdcss_read(
            self.handle, buffer, sectors, flag.value
        )
        if read_sectors < 0:
            raise exceptions.ReadError(
                message_with_error(
                    f"Failed reading {sectors * constants.SECTOR_SIZE} bytes",
                    self.error,
                )
            )

        data = buffer.raw[: read_sectors * constants.SECTOR_SIZE]
        expected_size = sectors * constants.SECTOR_SIZE
        read_size = len(data)
        if read_size != expected_size:
            raise exceptions.ReadError(
                f"Read {read_size} bytes, expected {expected_size}"
            )

        return data

    # def readv(self, p_iovec, i_blocks, i_flags):
    #   TODO: Implement readv, not sure how this would be used or implemented.
    #         It's possible the need for readv via python is simply unnecessary.

    def close(self) -> bool:
        """
        Close the DVD by freeing the dvdcss memory and handle of the block device.
        It also clears the local data buffer.

        This should always be run once you are finished with the opened disc, even
        if you don't intend to open another disc in the same instance.

        Raises:
            CloseError: Failure closing the disc.

        Returns True if a device was closed, otherwise no device was open.
        """
        if self.handle is None:
            return False
        else:
            ret = self._library.dvdcss_close(self.handle)
            if ret == 0:
                self.handle = None
                return True
            else:
                raise exceptions.CloseError(
                    message_with_error("Failed to close the open device", self.error)
                )

    @property
    def error(self) -> str | None:
        """
        Returns the latest error that occurred in the given libdvdcss instance.

        Always returns None if a DVD device or directory is not open.
        """
        if self.handle is None:
            return None
        return self._library.dvdcss_error(self.handle).strip() or None

    @property
    def is_scrambled(self) -> bool:
        """
        Returns True if the DVD device or directory is scrambled.

        Always returns False if a DVD device or directory is not open.
        """
        if self.handle is None:
            return False
        return self._library.dvdcss_is_scrambled(self.handle) == 1

    @staticmethod
    def _load_library() -> CDLL:
        """Load libdvdcss DLL/SO library via ctypes CDLL if available."""
        lib_name = None
        for possible_name in constants.LIBRARY_NAMES:
            lib_name = find_library(possible_name)
            if lib_name:
                break
            local_path = Path(__file__).parent.parent / possible_name
            if (
                local_path.with_suffix(".dll").exists()
                or local_path.with_suffix(".so").exists()
            ):
                lib_name = str(local_path)
                break

        if not lib_name:
            raise exceptions.LibraryNotFoundError(
                "Unable to locate the libdvdcss library. "
                "PyDvdCss cannot install this for you.\n\n" + constants.INSTALL_HELP
            )

        lib = CDLL(lib_name)
        lib.dvdcss_open.argtypes = [c_char_p]
        lib.dvdcss_open.restype = c_void_p
        lib.dvdcss_open_stream.argtypes = [c_void_p, DvdCssStreamCb]
        lib.dvdcss_open_stream.restype = c_void_p
        lib.dvdcss_close.argtypes = [c_void_p]
        lib.dvdcss_close.restype = c_int
        lib.dvdcss_seek.argtypes = [c_void_p, c_int, c_int]
        lib.dvdcss_seek.restype = c_int
        lib.dvdcss_read.argtypes = [c_void_p, c_char_p, c_int, c_int]
        lib.dvdcss_read.restype = c_int
        lib.dvdcss_error.argtypes = [c_void_p]
        lib.dvdcss_error.restype = c_int
        lib.dvdcss_is_scrambled.argtypes = [c_void_p]
        lib.dvdcss_is_scrambled.restype = c_int

        return lib

    @deprecated("Use :func:`close` instead.")
    def dispose(self) -> None:
        """(deprecated) Use :func:`close` instead."""
        self.close()
