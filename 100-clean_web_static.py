#!/usr/bin/python3
"""
Deletes stale archives
"""
from os.path import isdir, exists, basename, join, sep, splitext
from os import mkdir, listdir, unlink
from datetime import datetime
from fabric.api import env, local, put, run, runs_once
env.hosts = ['3.84.239.19', '18.210.33.168']


@runs_once
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
    if archive_path:
        return do_deploy(archive_path=archive_path)
    else:
        return False

def do_clean(number=0):
    """
    Deletes stale archives 
    """
    arcs = listdir("versions/")
    arcs.sort(reverse=True)
    number = int(number)
    if not number:
        number += 1
    if number < len(arcs):
        arcs = arcs[number:]
    else:
        arcs = []
    for arc in arcs:
        unlink(join("versions", arc))
        