#!/usr/bin/python3
"""
Fabric script to create and distribute an archive to web servers
"""

import os
import time
from fabric.api import env, local, put, run

# Define the web servers
env.hosts = ['54.234.56.234', '54.236.17.212']


def do_pack():
    """
    Generate a .tgz archive from the web_static folder.

    Returns:
        str: The path of the created archive, or None if creation fails.
    """
    try:
        # Create the versions directory if it doesn't exist
        local("mkdir -p versions")

        # Create the archive with a timestamp
        timestamp = time.strftime("%Y%m%d%H%M%S")
        archive_path = f"versions/web_static_{timestamp}.tgz"
        local(f"tar -cvzf {archive_path} web_static/")

        return archive_path
    except Exception as e:
        print(f"Error while packing: {e}")
        return None


def do_deploy(archive_path):
    """
    Distribute an archive to the web servers.

    Args:
        archive_path (str): The path to the archive file.

    Returns:
        bool: True if deployment was successful, False otherwise.
    """
    if not os.path.isfile(archive_path):
        print("Archive path does not exist")
        return False

    try:
        # Extract filename and folder name from archive_path
        file_name = os.path.basename(archive_path)
        folder_name = f"/data/web_static/releases/{file_name.split('.')[0]}"

        # Upload the archive to the /tmp/ directory on the web server
        put(archive_path, f"/tmp/{file_name}")

        # Create the release directory
        run(f"mkdir -p {folder_name}")

        # Extract the archive into the release directory
        run(f"tar -xzf /tmp/{file_name} -C {folder_name}")

        # Remove the archive from the /tmp/ directory
        run(f"rm /tmp/{file_name}")

        # Move contents of web_static to the release directory's root
        run(f"mv {folder_name}/web_static/* {folder_name}/")

        # Remove the now-empty web_static directory
        run(f"rm -rf {folder_name}/web_static")

        # Remove the old symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run(f"ln -s {folder_name} /data/web_static/current")

        print("Deployment done!")
        return True
    except Exception as e:
        print(f"Deployment failed: {e}")
        return False


def deploy():
    """
    Create and distribute an archive to web servers.

    Returns:
        bool: True if the deployment process was successful, False otherwise.
    """
    try:
        # Create an archive
        archive_path = do_pack()
        if archive_path is None:
            return False

        # Deploy the archive to the servers
        return do_deploy(archive_path)
    except Exception as e:
        print(f"Deploy failed: {e}")
        return False
