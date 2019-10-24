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
# @Time    : 10/12/2019 3:43 PM
# @Author  : Firmin.Sun (fmsunyh@gmail.com)
# @Software: ZJ_AI
# -----------------------------------------------------
# -*- coding: utf-8 -*-
from yacs.config import CfgNode as CN
import os.path as osp

_C = CN(new_allowed=True)

_C.OBDT_01 = CN()
_C.OBDT_01.IP = '192.168.1.179'
_C.OBDT_01.PORT = 26888

_C.OBDT_CLS = CN()
_C.OBDT_CLS.IP = '192.168.1.179'
_C.OBDT_CLS.PORT = 16888

_C.PATH = osp.join(osp.dirname(__file__),"..", 'data','config.yaml')

cfg = _C
