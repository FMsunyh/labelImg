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
# @Time    : 10/24/2019 9:27 AM
# @Author  : Firmin.Sun (fmsunyh@gmail.com)
# @Software: ZJ_AI
# -----------------------------------------------------
# -*- coding: utf-8 -*-
import sys
import os
import base64
import json
import requests
import argparse
import datetime
from PIL import Image
from config import cfg
from prettytable import PrettyTable
# input workspace
root_path = os.path.abspath(os.path.join(__file__, '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from utils.voc_generation import load_dataset
from utils.xml_utils import XmlSaver, XmlContext

def load_dataSet(dir, batch_size = 1):
    return load_dataset(dir, batch_size)

def host_interface(host='0.0.0.0', port='16889'):
    api_str = 'http://{}:{}/commdity_recognition/recognition'.format(host,port)
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
    # data['data']['base64_code'] = encode
    data['data']['base64_code'] = "data:image/jpg;base64,"+ str(encode).encode('utf-8')
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

    host = cfg.SEARCH_ID.IP
    port = cfg.SEARCH_ID.PORT
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
    ids = {}
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

        if xml_context.labels[0] in ids:
            ids[xml_context.labels[0]] = ids[xml_context.labels[0]] + 1
        else:
            ids[xml_context.labels[0]] = 1

        print('[{}/{}]'.format(count,dataSet.size()))

        if count >10:
            break

    result = sorted(ids.items(), key=lambda d: d[1],reverse = True)


    table = PrettyTable(["ID", "SCORE"])
    table.align["ID"] = "l"
    table.padding_width = 1
    for tup in result:
        table.add_row([tup[0], tup[1]])

    print(table)

def do_searchid(input_path, defaultConfigFile):
    do_fun(input_path, defaultConfigFile)

    print('proccess successfully.')