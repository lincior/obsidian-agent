"""MCP server for Obsidian vaults."""

from __future__ import annotations

import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP

OBSIDIAN_ROOT = Path(os.getenv("OBSIDIAN_ROOT"))
if not OBSIDIAN_ROOT.is_dir():
    error_message = (
        "OBSIDIAN_ROOT environment variable is not set or is not a directory."
    )
    raise ValueError(error_message)

mcp = FastMCP("Obsidian")


@mcp.tool()
def list_vaults() -> list[str]:
    """List all available vaults in Obsidian.

    Returns
    -------
        list[str]: list of vault names.

    """
    return [p.stem for p in OBSIDIAN_ROOT.glob("*")]


@mcp.tool()
def list_vault_notes(vault: str) -> str:
    """List all notes in a given vault.

    Args:
    ----
        vault (str): vault name.

    Returns:
    -------
        str: list of filenames in the vault.

    """
    return [p.name for p in (OBSIDIAN_ROOT / vault).glob("*")]


@mcp.tool()
def read_note(vault: str, note: str) -> str:
    """Read a note from a vault.

    Args:
    ----
        vault (str): vault name.
        note (str): note filename.

    Raises:
    ------
        FileNotFoundError: if the note does not exist in the vault.

    Returns:
    -------
        str: content of the note.

    """
    note_path = OBSIDIAN_ROOT / vault / note
    if not note_path.is_file():
        error_message = f"Note '{note}' not found in vault '{vault}'."
        raise FileNotFoundError(error_message)
    with note_path.open(encoding="utf-8") as f:
        return f.read()
