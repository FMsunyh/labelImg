#!/usr/bin/python3

"""
Copyright 2018-2019  Firmin.Sun (fmsunyh@gmail.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
# -----------------------------------------------------
# @Time    : 9/26/2019 5:20 PM
# @Author  : Firmin.Sun (fmsunyh@gmail.com)
# @Software: ZJ_AI
# -----------------------------------------------------
# -*- coding: utf-8 -*-
import os

#!/usr/bin/env python3
# -----------------------------------------------------
# -*- coding: utf-8 -*-
# @time : 19-5-16
# @Author  : jaykky
# @Software: ZJ_AI
# -----------------------------------------------------
import sys
import os
import base64
import json
import requests
import argparse
import datetime
from PIL import Image
from config import cfg

# input workspace
root_path = os.path.abspath(os.path.join(__file__, '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from utils.voc_generation import load_dataset
from utils.xml_utils import XmlSaver, XmlContext

def load_dataSet(dir, batch_size = 1):
    return load_dataset(dir, batch_size)

def host_interface(host='0.0.0.0', port='36888'):
    api_str = 'http://{}:{}/task'.format(host,port)
    return api_str

def load_image_size_pil(path):
    # result : (width, height)
    # use time : 0.0068
    im = Image.open(path)
    return im.size

#=============== tool util ===================#
def image2base64(image_path):
    with open(image_path, 'rb') as f:
        data = f.read()
        byte_encode = base64.b64encode(data)
        # str_encode = str(byte_encode, 'utf-8')
        str_encode = str(byte_encode).encode('utf-8')
    return str_encode

def get_json_data(json_file):
    with open(json_file) as f:
        data = json.load(f)
    return data

def get_post_info(image_file):
    data = {}
    data['data'] = {}

    encode = image2base64(image_file)
    data['data']['base64_code'] = encode
    return data

def post(url, data):
    if url == '':
        return None

    res = requests.post(url, json=data)
    return res.text

def get_now_date():
    date = datetime.datetime.now().strftime('%Y%m%d')
    return str(date)

def prelabel_image(host, port, image_dir):
    host = host_interface(host, port)

    post_code  = get_post_info(image_dir)

    callback_boxes = post(host, post_code)

    return callback_boxes

def callback2boxes(callback):
    detect_result = list(json.loads(callback)['data'])
    boxes, labels = [], []
    for  r in detect_result:
        r = r.split(',')
        labels.append(r[0])
        boxes.append([int(float(r[2])), int(float(r[3])), int(float(r[4])), int(float(r[5]))])
    return boxes, labels

def success(callback):
    return json.loads(callback)['status'] == 100000


def read_setting(path):
    # read data from setting,cfg

    cfg.merge_from_file(path)

    host = cfg.OBDT_01.IP
    port = cfg.OBDT_01.PORT
    return host, str(port)

def do_fun(path,defaultConfigFile):
    #1 open image

    # base 64code

    # request server

    # get result

    # save result

    # init tools
    package_dir = path
    host, port = read_setting(defaultConfigFile)

    dataSet = load_dataSet(package_dir)
    xml_saver = XmlSaver()
    xml_context = XmlContext

    # start calculate graph
    count = 0
    while dataSet.has_next():
        output = dataSet.next()
        jpg, _ = output[0]

        count = count+1
        if not os.path.exists(jpg):
            print('{} is not exist!'.format(jpg))

        callback = prelabel_image(host, port, jpg)
        # print(callback)

        # extract neccessary result from callback
        if not success(callback):
            print('{} cant prelabel success!'.format(jpg))
            continue

        xml_context.boxes, xml_context.labels = callback2boxes(callback)
        # print('detect result : {}, {}'.format(xml_context.boxes, xml_context.labels))

        # save boxes
        xml_path = dataSet.get_xml_by_jpg(jpg)
        xml_context.path = xml_path
        if not os.path.exists(os.path.abspath(os.path.join(xml_path, '..'))):
            os.mkdir(os.path.abspath(os.path.join(xml_path, '..')))

        width, height = load_image_size_pil(jpg)
        image_size = [height, width, 3]
        xml_context.sizes = image_size

        xml_saver.save(xml_context)
        print('[{}/{}]{} have saved success!'.format(count,dataSet.size(), xml_path))

def do_makebbox(input_path, defaultConfigFile,):
    do_fun(input_path, defaultConfigFile)

    print('proccess successfully.')


