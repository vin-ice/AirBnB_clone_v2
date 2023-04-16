#!/usr/bin/python3
"""
Generates a .tgz archive from web_static
"""
from datetime import datetime
from fabric.api import local
from os.path import isdir
from os.path import join


def do_pack():
    """
    Generates a .tgz archive file from web_static
    """
    dest = "versions"
    f_name = "web_static_{}.tgz".format(datetime.now()
                                        .strftime("%Y%m%d%H%M%S"))

    if not isdir(dest):
        local("mkdir {}".format(dest))

    path = join(dest, f_name)
    res = local("tar -cvzf {} web_static".format(path))

    if res.failed:
        return None
    else:
        return path
