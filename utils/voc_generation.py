#!/usr/bin/env python3
# -----------------------------------------------------
# -*- coding: utf-8 -*-
# @time : 19-5-5
# @Author  : jaykky
# @Software: ZJ_AI
# -----------------------------------------------------
import os
import logging
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def load_dataset(dir, batch_size):
    dataset = Voc_generation(dir, batch_size)
    return dataset


def is_voc_dataset(dir):
    if not os.path.exists(os.path.join(dir, 'JPEGImages')):
        return False

    elif not os.path.exists(os.path.join(dir, 'Annotations')):
        os.makedirs(os.path.join(dir, 'Annotations'))

    return True


class Voc_generation(object):
    def __init__(self, parent_dir, batch_size=1, circle=False):
        self.parent_dir = parent_dir
        self.batch_size = batch_size
        self.circle = circle
        self._has_next = True
        self._epoch    = 0

        assert is_voc_dataset(self.parent_dir), 'Please confirm {} file is voc package'.format(self.parent_dir)

        self._file_index = 0
        self._file_path = self.get_files_from_dir(self.parent_dir)

    def size(self):
        return len(self._file_path)

    def has_next(self):
        return self._has_next

    def get_epoch(self):
        return self._epoch

    def get_files_from_dir(self, dir, ext='.jpg'):
        jpg_dir = os.path.join(dir, 'JPEGImages')
        result_list = []
        for root, _, files in os.walk(jpg_dir):
            result_list.extend([os.path.join(root, fn) for fn in files
                                if os.path.splitext(fn)[1]==ext])
        logging.info('{} get {} {} files'.format(dir, len(result_list), ext))
        return result_list

    def get_xml_by_jpg(self, jpg):
        jpg_name = os.path.splitext(os.path.split(jpg)[1])[0]
        parent_dir, parent_name = os.path.split(os.path.dirname(jpg))
        xml_path = os.path.join(parent_dir, 'Annotations', jpg_name + '.xml')
        return xml_path

    def next(self):
        if self._file_index == 0:
            self._epoch +=1
            self._file_path = sorted(self._file_path)

        group = []
        for i in range(self.batch_size):

            # load jpg and xml
            jpg_fn = self._file_path[self._file_index]
            xml_fn = self.get_xml_by_jpg(jpg_fn)
            group.append([jpg_fn, xml_fn])

            # update next file index
            self._file_index = (self._file_index + 1) % self.size()

            # if not circle , break out
            if not self.circle and self._file_index == 0:
                self._has_next = False
                break

        return group

# load_dataset('/home/hyl/data/train_data_2019-05-06_worksite',batch_size=1)