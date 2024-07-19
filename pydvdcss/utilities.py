from __future__ import annotations

from typing import Any


def message_with_error(message: str | None, error: Any | None) -> str:
    """
    Merge a message with an error as a string, if there's an error available.

    Parameters:
        message: String to use as the primary message.
        error: Variable to use as an error message/code.

    Returns a string with message and error seperated with `: ` if error is not blank.
    """
    return ": ".join(part for part in (message, str(error or "")) if part)
