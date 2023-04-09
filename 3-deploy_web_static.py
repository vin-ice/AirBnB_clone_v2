#!/usr/bin/python3
"""
Creates and distributes an archive to webservers
"""
from datetime import datetime
from fabric.api import env, local, put, run, runs_once
from os.path import isdir, exists, basename, join
from os import mkdir, sep
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
    dest = join(path, f_name.split(".")[0])
    try:
        put(archive_path, "{}".format(join(sep, "tmp", f_name)))
        run("mkdir -p {}".format(path))
        run("tar -xzf {} -C {}".format(join(sep, "tmp", f_name), dest))
        run("rm -rf {}".format(f_name))
        run("mv {}/web_static/* {}".format(dest, dest))
        run("rm -rf {}/web_static".format(dest))
        run("rm -rf {}".format(join(sep, "data", "web_static", "current")))
        run("ln -s {} {}".format(dest, join(sep,
                                            "data", "web_static", "current")))
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
