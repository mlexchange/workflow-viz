import logging
import os
import re
from logging import StreamHandler

from dotenv import load_dotenv

load_dotenv()

TILED_BLACKLIST = os.getenv("TILED_BLACKLIST", "").strip()
# Split by space or comma followed by any number of whitespaces
TILED_BLACKLIST = re.split(r"[,\s]+\s*", TILED_BLACKLIST)

TILED_BLACKLIST = [
    blacklist_term for blacklist_term in TILED_BLACKLIST if blacklist_term.strip()
]

logger = logging.getLogger("tiled.adapters.blacklist")
logger.addHandler(StreamHandler())
logger.setLevel("INFO")

# Blacklist is empty, will not filter out anything
if not TILED_BLACKLIST:
    logger.info("    BLACKLIST: Blacklist empty, not applying whitelist walker.")
else:
    logger.info("    BLACKLIST: Omitting files and directorys with:")
    for blacklist_term in TILED_BLACKLIST:
        logger.info("        %s" % blacklist_term)


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
    # Blacklist is empty, will not filter out anything
    if not TILED_BLACKLIST:
        return files, directories

    unhandled_files = []
    for file in files:
        if file.is_file() and any(
            blacklist_term in file.name for blacklist_term in TILED_BLACKLIST
        ):
            logger.info("    BLACKLIST: Nothing will handle file '%s'", file)
        else:
            unhandled_files.append(file)
    unhandled_directories = []
    for directory in directories:
        if directory.is_dir() and any(
            blacklist_term in directory.name for blacklist_term in TILED_BLACKLIST
        ):
            logger.info("    BLACKLIST: Nothing will handle directory '%s'", directory)
        else:
            unhandled_directories.append(directory)
    return unhandled_files, unhandled_directories
