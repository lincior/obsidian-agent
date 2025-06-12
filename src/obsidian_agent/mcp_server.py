"""MCP server for Obsidian vaults."""

from __future__ import annotations

import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP


def get_obsidian_root() -> Path:
    """Get the root directory of Obsidian vaults from env variable.

    Raises
    ------
        ValueError: unset environment variable.
        ValueError: not a directory.

    Returns
    -------
        Path: path to the Obsidian root directory.

    """
    root = os.getenv("OBSIDIAN_ROOT")
    if not root:
        error_message = "OBSIDIAN_ROOT environment variable is not set."
        raise ValueError(error_message)
    path = Path(root)
    if not path.is_dir():
        error_message = f"OBSIDIAN_ROOT '{root}' is not a directory."
        raise ValueError(error_message)
    return path


mcp = FastMCP("Obsidian")


@mcp.tool()
def list_vaults() -> list[str]:
    """List all available vaults in Obsidian.

    Returns
    -------
        list[str]: list of vault names.

    """
    obsidian_root = get_obsidian_root()
    return [p.stem for p in obsidian_root.glob("*")]


@mcp.tool()
def list_vault_notes(vault: str) -> list[str]:
    """List all notes in a given vault.

    Args:
    ----
        vault (str): vault name.

    Returns:
    -------
        str: list of filenames in the vault.

    """
    obsidian_root = get_obsidian_root()
    return [p.name for p in (obsidian_root / vault).glob("*")]


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
    obsidian_root = get_obsidian_root()
    note_path = obsidian_root / vault / note
    if not note_path.is_file():
        error_message = f"Note '{note}' not found in vault '{vault}'."
        raise FileNotFoundError(error_message)
    return note_path.read_text(encoding="utf-8")
