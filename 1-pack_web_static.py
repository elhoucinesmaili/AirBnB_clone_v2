#!/usr/bin/python3
"""
Fabric script to generate a .tgz archive
Usage: fab -f 1-pack_web_static.py do_pack
"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Creates a .tgz archive of the web_static folder.
    The archive will be stored in the 'versions' directory.
    """
    # Generate the timestamped archive name
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = f"web_static_{timestamp}.tgz"

    # Ensure the versions directory exists
    if local("mkdir -p versions").failed:
        return None

    # Create the archive
    result = local(f"tar -cvzf versions/{archive_name} web_static")
    if result.failed:
        return None

    return archive_name
