from typing import Literal

from pydvdcss.structs import CrackingMode, ReadFlag, SeekFlag, VerbosityLevel

VerbosityLevel_T = VerbosityLevel | Literal[-1, 0, 1, 2]
CrackingMode_T = CrackingMode | Literal["unset", "title", "disc", "key"]
SeekFlag_T = SeekFlag | Literal[0, 1, 2]
ReadFlag_T = ReadFlag | Literal[0, 1]

__all__ = ("VerbosityLevel_T", "CrackingMode_T", "SeekFlag_T", "ReadFlag_T")
