#!/usr/bin/env python3
# -----------------------------------------------------
# -*- coding: utf-8 -*-
# @time : 19-5-13
# @Author  : jaykky
# @Software: ZJ_AI
# -----------------------------------------------------
from lxml.etree import Element, SubElement, ElementTree, tostring
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
import os

class XmlContext:
    def __init__(self):
        # Note : size = (height, width, depth)!!
        self.labels = []
        self.boxes  = []
        self.sizes  = []
        self.path   = ''

#  use guide:
#  path = '/home/hyl/data/2019-04-29_a2_10000.xml'
#  xml = XmlReader()
#  xml.open(path)
#  print(xml.get_size(), xml.get_labels(), xml.get_boxes())
#
class XmlReader:
    def __init__(self):
        pass

    def open(self, path):
        self._init()
        self._open_xml(path)
        return self.xml_context

    def _init(self):
        # self._labels = []
        # self._boxes = []
        # self._size = []
        self.xml_context = XmlContext

    def get_context(self):
        return self.xml_context

    # def get_labels(self):
    #     # assert len(self._labels) != 0, 'Please first run open function or this file have no label!'
    #     return self._labels
    #
    # def get_boxes(self):
    #     # assert len(self._boxes) != 0, 'Please first run open function or this file have no boxes!'
    #     return self._boxes
    #
    # def get_size(self):
    #     assert len(self._size) == 3, 'Please first run open function or this file have no sizes!'
    #     return self._size

    def _open_xml(self, path):
        tree = ET.parse(path)
        root = tree.getroot()
        self.xml_context.path   = path
        self.xml_context.labels = self._find_labels(root)
        self.xml_context.boxes  = self._find_boxes(root)
        self.xml_context.sizes  = self._find_size(root)

    def _find_labels(self, root):
        labels = []
        element_objs = root.findall('object')
        for element_obj in element_objs:
            name = element_obj.find('name').text
            labels.append(name)
        return labels

    def _find_boxes(self, root):
        boxes = []
        element_objs = root.findall('object')
        for element_obj in element_objs:
            bbox = element_obj.find('bndbox')
            xmin = int(float(bbox.find('xmin').text))
            ymin = int(float(bbox.find('ymin').text))
            xmax = int(float(bbox.find('xmax').text))
            ymax = int(float(bbox.find('ymax').text))
            boxes.append([xmin, ymin, xmax, ymax])
        return boxes

    def _find_size(self, root):
        element_objs = root.findall('size')
        width = int(float(element_objs[0].find('width').text))
        height = int(float(element_objs[0].find('height').text))
        depth = int(float(element_objs[0].find('depth').text))
        return [height, width, depth]



# use guide :
# path = '/home/hyl/data/2019-04-29_a2_10000.xml'
# boxes = [[1,2,3,4], [1,3,5,7]]
# labels = [class1, class2]
# size  = [1280, 720, 3]  [width, height, depth]
# saver = XmlSaver()
# saver.push(path[:-4] + '_1.xml', xml.get_size(), xml.get_labels(), xml.get_boxes())
# saver.save()

class XmlSaver:
    def __init__(self):
        self._init()

    def _init(self):
        self._root = None

    def _build_voc_structure(self):
        root = Element('annotation')
        tree = ElementTree(root)
        return root

    def save(self, xml_context):
        # Note : size = (height, width, depth)!!
        self.xml_context = xml_context

        # start to build xml tree
        self._root = self._build_voc_structure()
        self._load_default_attribute(self._root)
        self._load_path_attribute(self._root)
        self._load_size_attribute(self._root)
        self._load_obj_attribute(self._root)

        self._save()


    def _save(self):
        assert self._can_save, 'Please first push something into Saver!'
        self._save_into_xml()
        self.clean()

    def clean(self):
        self._init()

    def _save_into_xml(self):
        xml = tostring(self._root, pretty_print=True)
        dom = parseString(xml)
        with open(self.xml_context.path, 'w+') as f:
            dom.writexml(f, addindent='', newl='', encoding='utf-8')


    def _can_save(self):
        return (self.xml_context.labels is not None and self.xml_context.boxes is not None
                and self.xml_context.path is not None and self.xml_context.sizes is not None)

    def _load_default_attribute(self, root): #构建voc默认属性
        node_folder = SubElement(root, 'folder')
        node_folder.text = 'JPEGImages'
        node_segmented = SubElement(root, 'segmented')
        node_segmented.text = '0'

    def _load_path_attribute(self, root): #构建路径属性
        node_filename = SubElement(root, 'filename')
        node_filename.text = os.path.split(self.xml_context.path)[1][:-4]+'.jpg'
        node_path = SubElement(root, 'path')
        node_path.text = os.path.abspath(os.path.join(self.xml_context.path,'..','..','JPEGImages',
                                                      os.path.split(self.xml_context.path)[1][:-4]+'.jpg'))

    def _load_size_attribute(self, root): #构建图像尺寸属性
        node_size = SubElement(root, 'size')
        node_width=SubElement(node_size,'width')
        node_width.text=str(self.xml_context.sizes[1])
        node_height = SubElement(node_size, 'height')
        node_height.text=str(self.xml_context.sizes[0])
        node_depth = SubElement(node_size, 'depth')
        node_depth.text = str(self.xml_context.sizes[2])

    def _load_obj_attribute(self, root):  #构建图像物体属性
        for i,label in enumerate(self.xml_context.labels):
            node_object = SubElement(root, 'object')
            node_name = SubElement(node_object, 'name')
            node_name.text = label
            node_pose = SubElement(node_object, 'pose')
            node_pose.text = 'Unspecified'
            node_truncated = SubElement(node_object, 'truncated')
            node_truncated.text = '0'
            node_difficult = SubElement(node_object, 'difficult')
            node_difficult.text = '0'
            self.xml_context.boxes[i]=self._check_border(self.xml_context.boxes[i])

            node_bndbox = SubElement(node_object, 'bndbox')
            node_xmin = SubElement(node_bndbox, 'xmin')
            node_xmin.text = str(int(self.xml_context.boxes[i][0]))

            node_ymin = SubElement(node_bndbox, 'ymin')
            node_ymin.text = str(int(self.xml_context.boxes[i][1]))

            node_xmax = SubElement(node_bndbox, 'xmax')
            node_xmax.text = str(int(self.xml_context.boxes[i][2]))

            node_ymax = SubElement(node_bndbox, 'ymax')
            node_ymax.text = str(int(self.xml_context.boxes[i][3]))

    def _check_border(self, bbox): #边缘检测
        if bbox[0] <= 0.0:
            bbox[0] = 1

        if bbox[1] <= 0.0:
            bbox[1] = 1

        if bbox[2] >= self.xml_context.sizes[1]:
            bbox[2] = self.xml_context.sizes[1] - 1

        if bbox[3] >= self.xml_context.sizes[0]:
            bbox[3] = self.xml_context.sizes[0] - 1
        return bbox
