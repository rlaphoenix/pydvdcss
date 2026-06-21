from typing import Literal

from pydvdcss.structs import ReadFlag, SeekFlag

SeekFlag_T = SeekFlag | Literal[0, 1, 2]
ReadFlag_T = ReadFlag | Literal[0, 1]

__all__ = ("ReadFlag_T", "SeekFlag_T")
