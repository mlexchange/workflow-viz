import logging
import os
import re
from logging import StreamHandler

from dotenv import load_dotenv

load_dotenv()

TILED_WHITELIST = os.getenv("TILED_WHITELIST", "").strip()
# Split by space or comma followed by any number of whitespaces
TILED_WHITELIST = re.split(r"[,\s]+\s*", TILED_WHITELIST)
TILED_WHITELIST = [
    whitelist_term for whitelist_term in TILED_WHITELIST if whitelist_term.strip()
]

logger = logging.getLogger("tiled.adapters.whitelist")
logger.addHandler(StreamHandler())
logger.setLevel("INFO")

if not TILED_WHITELIST:
    logger.info("    WHITELIST: Whitelist empty, not applying whitelist walker.")
else:
    logger.info(
        "    WHITELIST: Only processing files and directorys where the path contains:"
    )
    for whitelist_term in TILED_WHITELIST:
        logger.info("        %s" % whitelist_term)


async def walk(
    catalog,
    path,
    files,
    directories,
    settings,
):
    """
    Skip all files and directories that contain a term from the blacklist.
    """
    # Whitelist is empty, do not apply anything
    if not TILED_WHITELIST:
        return files, directories

    unhandled_files = []
    for file in files:
        if file.is_file() and any(
            whitelist_term in file.name for whitelist_term in TILED_WHITELIST
        ):
            unhandled_files.append(file)
        else:
            logger.info("    WHITELIST: Nothing will handle file '%s'", file)
    unhandled_directories = []
    for directory in directories:
        if directory.is_dir() and any(
            whitelist_term in directory.name for whitelist_term in TILED_WHITELIST
        ):
            unhandled_directories.append(directory)
        else:
            logger.info("    WHITELIST: Nothing will handle directory '%s'", directory)
    return unhandled_files, unhandled_directories
