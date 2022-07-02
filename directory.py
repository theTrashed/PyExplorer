import os
import sys
import subprocess


def sort_dir_list(dir_conts, r=False):
    dir_conts = {k: v for k, v in sorted(dir_conts.items(), key=lambda item:
                                         item[0].lower(), reverse=r)}
    dir_conts = {k: v for k, v in sorted(dir_conts.items(), key=lambda item:
                                         item[1])}

    return dir_conts


def get_dir_cont(new_dir_path='~', sort=True, ascending=False):
    os.chdir(os.path.expanduser(new_dir_path))

    dir_cont = {}
    # Check if the directory is the root directory or not
    if (os.path.dirname(os.curdir) != os.curdir):
        dir_cont['..'] = 'dir'
    dirs = os.listdir()
    for d in dirs:
        if os.path.isdir(d):
            dir_cont[d] = 'dir'
        else:
            dir_cont[d] = 'file'

    if (sort):
        return sort_dir_list(dir_cont, ascending)
    else:
        return dir_cont


def open_file(file_path):
    if sys.platform.startswith('darwin'):
        subprocess.call(['open', os.path.join(os.curdir, file_path)])
    elif sys.platform.startswith('win32'):
        subprocess.call(['cmd', '/c' , 'start', os.path.join(os.curdir, file_path)])
    elif sys.platform.startswith('linux'):
        subprocess.call(['xdg-open', os.path.join(os.curdir, file_path)])
    else:
        print('No support for unknown OS')
