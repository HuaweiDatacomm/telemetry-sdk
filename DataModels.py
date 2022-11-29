#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能：数据模型，用于过滤输入
修改记录：2022-11-28 hwx1045592 创建
"""

from pydantic import BaseModel


# 动态订阅传递参数
class SubsPara(BaseModel):
    username: str
    password: str
    address: str
    path: str | None = 'huawei-debug:debug/cpu-infos/cpu-info'
    depth: int | None = 1
    sample_interval: int | None = 1000
    request_id: int | None = 3

# 解析数据Message模型
class MessageBody(BaseModel):
    message: str
    sensor_path: str | None = 'huawei-debug'

# 返回数据模型
class Output(BaseModel):
    code: int = 200
    info: str = 'success'
    message: str | None = None