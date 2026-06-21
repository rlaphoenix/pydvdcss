"""Hatchling build hook: tag the wheel for a platform when a bundled DLL exists.

The CD workflow downloads ``pydvdcss/libdvdcss-2.dll`` and sets the
``PYDVDCSS_WHEEL_PLATFORM`` environment variable (e.g. ``win_amd64`` or
``win32``) before building, producing a platform-specific wheel. With neither the
env var nor the DLL present, a normal pure (py3-none-any) wheel is built.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        platform_tag = os.environ.get("PYDVDCSS_WHEEL_PLATFORM", "").strip()
        bundled_dll = Path(self.root) / "pydvdcss" / "libdvdcss-2.dll"
        if platform_tag and bundled_dll.exists():
            build_data["pure_python"] = False
            build_data["tag"] = f"py3-none-{platform_tag}"
