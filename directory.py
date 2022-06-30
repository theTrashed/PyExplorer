import os


def sort_dir_list(dir_conts, r=False):
    dir_conts = {k: v for k, v in sorted(dir_conts.items(), key=lambda item:
                                         item[0].lower(), reverse=r)}
    dir_conts = {k: v for k, v in sorted(dir_conts.items(), key=lambda item:
                                         item[1])}

    return dir_conts


def get_dir_cont(new_dir_path, sort=True, ascending=False):
    os.chdir(os.path.expanduser(new_dir_path))

    dir_cont = {}
    dirs = os.listdir()
    for d in dirs:
        if os.path.isdir(d):
            dir_cont[d] = 'dir'
        else:
            dir_cont[d] = 'file'

    if sort:
        return sort_dir_list(dir_cont, ascending)
    else:
        return dir_cont
