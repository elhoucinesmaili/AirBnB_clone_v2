#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers
Usage:
    fab -f 2-do_deploy_web_static.py do_deploy:archive_path=<path_to_archive> -i <ssh_key> -u <username>
"""

from fabric.api import env, put, run
import os

# Define the web servers
env.hosts = ['54.234.56.234', '54.236.17.212']


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.
    
    Args:
        archive_path (str): The path to the archive to distribute.

    Returns:
        bool: True if all operations were successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Extract the archive name and directory name
        archive_name = os.path.basename(archive_path)
        no_ext = archive_name.split(".")[0]
        release_path = f"/data/web_static/releases/{no_ext}"

        # Upload the archive to /tmp/ directory on the web server
        put(archive_path, f"/tmp/{archive_name}")

        # Create the directory to uncompress the archive
        run(f"mkdir -p {release_path}")

        # Uncompress the archive into the release directory
        run(f"tar -xzf /tmp/{archive_name} -C {release_path}")

        # Remove the archive from the web server
        run(f"rm /tmp/{archive_name}")

        # Move the contents from web_static to the parent directory
        run(f"mv {release_path}/web_static/* {release_path}/")

        # Remove the now-empty web_static directory
        run(f"rm -rf {release_path}/web_static")

        # Remove the old symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link to the new release
        run(f"ln -s {release_path} /data/web_static/current")

        print("New version deployed!")
        return True
    except Exception as e:
        print(f"Deployment failed: {e}")
        return False
