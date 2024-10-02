import os
import shutil


def copy_static_to_public(source, dest):
    ld = []
    if os.path.exists(source):
        ld = os.listdir(source)

    if os.path.exists(dest):
        shutil.rmtree(dest)
        os.mkdir(dest)
    else:
        os.mkdir(dest)

    if (item := ".DS_Store") in ld:
        ld.remove(item)

    for item in ld:
        s = os.path.join(source, item)
        d = os.path.join(dest, item)
        if os.path.isfile(s):
            shutil.copy(s, d)
        else:
            copy_static_to_public(s, d)
