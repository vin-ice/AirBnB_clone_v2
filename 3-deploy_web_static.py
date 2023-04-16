#!/usr/bin/python3
"""
Creates and distributes an archive to webservers
"""
from datetime import datetime
from fabric.api import env, local, put, run
from os.path import isdir, exists, basename, join, splitext
from os import mkdir, sep
env.hosts = ['3.84.239.19', '18.210.33.168']


def do_pack():
    """Archives static files"""
    if not isdir("versions"):
        mkdir("versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    dest = "versions/web_static_{}.tgz".format(date)
    try:
        local("tar -cvzf {} web_static".format(dest))
        return dest
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Distributes archive files from exe 1 to server
    """
    if not exists(archive_path):
        return False
    f_name = basename(archive_path)
    path = join(sep, "data", "web_static", "releases")
    dest = join(path, splitext(f_name)[0])
    tmp = join(sep, "tmp", f_name)
    cur = join(sep, "data", "web_static", "current")
    try:
        put(archive_path, "{}".format(tmp))
        run("mkdir -p {}/".format(join(dest)))
        run("tar -xzf {} -C {}/".format(tmp, dest))
        run("rm {}".format(tmp))
        run("mv {} {}/".format(join(dest, "web_static", "*"), dest))
        run("rm -rf {}".format(join(dest, "web_static")))
        run("rm -rf {}".format(cur))
        run("ln -s {}/ {}".format(dest, cur))
        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """
    Archives and deploys static files
    """
    archive_path = do_pack()
    try:
        return (do_deploy(archive_path=archive_path))
    except Exception:
        return False
