#!/usr/bin/python3
"""
Distributes an archive to web servers
"""
from os.path import exists, splitext
from fabric.api import put, run, env
from os.path import basename
from os.path import join
from os import sep

env.hosts = ['3.84.239.19', '18.210.33.168']


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
