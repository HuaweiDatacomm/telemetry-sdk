#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能：message信息相关操作，主要是解码与编码
修改记录：2022-11-28 hwx1045592 创建
"""

from proto_py import huawei_telemetry_pb2
import codecs


# 解析message数据
def decode_message(message: str):
    try:
        # messagebyte = b'\n\003PE1\022\021_dyn_grpc_c6_8247\032.huawei-devm:devm/huawei-driver:driver/fans/fanj\020huawei_devm.Devm \002(\302\217\246\236\31200\332\221\246\236\3120:G\nE\010\326\221\246\236\3120Z<\232\0019*7\n5\n\00213\020\201\200\264\010\032\014CR8MM82FBXC1 \001(\0248\001@\001H\001P\002Z\020  [1]20%  [2]20%@\332\221\246\236\3120H\350\007R\002OKZ\016NetEngine 8000`\000\202\001\013V800R021C12\212\001\02124-A5-2C-86-3F-C0'
        messageBytes = bytes(message, encoding='utf8')
        # 转换生成的字节串中包含\\，下面方法可以去除，返回一个元组，第一个是数据，第二个是类型
        messageTuple = codecs.escape_decode(messageBytes, "hex-escape")
        return huawei_telemetry_pb2.Telemetry.FromString(messageTuple[0])
    except Exception as e:
        errorMsg = f"dialin error, exception: {e}"
        return errorMsg
