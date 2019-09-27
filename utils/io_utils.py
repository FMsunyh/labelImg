#!/usr/bin/env python3
# -----------------------------------------------------
# -*- coding: utf-8 -*-
# @time : 19-5-5
# @Author  : jaykky
# @Software: ZJ_AI
# -----------------------------------------------------
import os
import shutil


def make_dir(new_dir):
    if not os.path.exists(new_dir):
        print('{} create success!'.format(new_dir))
        os.mkdir(new_dir)

def rename_file(oldname, newname):
    try:
        if oldname !='' and newname != '':
            os.rename(oldname, newname)
            # print('old name:', oldname)
            # print('new name:', newname)
    except Exception as ex:
        print(ex)


def move_dir(src_file, dest_dir):
    make_dir(dest_dir)

    try:
        shutil.move(src_file, dest_dir)
        # print("move successfuly:'{}' to '{}'".format(src_file, dest_dir))
    except Exception as e:
        print("Can't not move '{}' to '{}'. :{}", src_file, dest_dir, e)

def move_files_to_folder(folder, file_list):
    for f in file_list:
        move_dir(f, folder)

def get_files_from_dir(dir, ext='.jpg'):
    result_list = []
    for root, _, files in os.walk(dir):
        result_list.extend([os.path.join(root, fn) for fn in files
                            if os.path.splitext(fn)[1]== ext])
    print(' get {} {} files'.format(len(result_list), ext))
    return result_list

# if __name__ == '__main__':
#