#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能：生产数据类，该类主要用于从路由器采集数据，包括dialin(Subscribe)和dialout(DataPublish)
修改记录：2022-11-17 hwx1045592 创建
"""
import threading

import grpc

from proto_py import huawei_grpc_dialin_pb2_grpc, huawei_grpc_dialin_pb2, huawei_grpc_dialout_pb2_grpc

class Subscribe(threading.Thread):
    """Subscribe dialin rpc method."""
    def __init__(self, t_name, dialin_server, sub_args_dict):
        threading.Thread.__init__(self, name=t_name, daemon=True)
        # 订阅成功状态
        self.status = False
        self.dialin_server = dialin_server
        self.sub_args_dict = sub_args_dict

    # 查看订阅状态
    def getStauts(self):
        # 订阅成功状态
        return self.status

    def run(self):
        try:
            metadata, subreq = Subscribe.generate_subArgs_and_metadata(self.sub_args_dict)
            # 新建grpc客户端，建立grpc连接
            server = self.dialin_server
            channel = grpc.insecure_channel(server)
            stub = huawei_grpc_dialin_pb2_grpc.gRPCConfigOperStub(channel)
            # 开始订阅
            sub_resps = stub.Subscribe(subreq, metadata=metadata)
            for sub_resp in sub_resps:
                data_is_valid = Subscribe.check_sub_reply_is_data(sub_resp)  # 检查是否为数据
                if data_is_valid is False:
                    self.status = True
                else:
                    print(sub_resp)
                break
            exit()
        except Exception as e:
            print("dialin error, exception {0}".format(e))

    # 检查 dialin reply 是否为正常数据
    @staticmethod
    def check_sub_reply_is_data(sub_resp):
        resp_code = sub_resp.response_code
        if (resp_code == ""):
            return True
        if (resp_code == "200"):
            return False
        if (resp_code != "200" and resp_code != ""):
            return False
        if (sub_resp.message == "ok"):
            return False

    # 生成订阅和grpc连接参数
    @staticmethod
    def generate_subArgs_and_metadata(sub_args_dict):
        metadata, paths, request_id, sample_interval = sub_args_dict['metadata'], sub_args_dict['paths'], \
                                                       sub_args_dict['request_id'], sub_args_dict['sample_interval']
        sub_req = huawei_grpc_dialin_pb2.SubsArgs()
        for path in paths:
            sub_path = huawei_grpc_dialin_pb2.Path(path=path['path'], depth=path['depth'])
            sub_req.path.append(sub_path)
        sub_req.encoding = 0  # 固定值0:gpb编码
        sub_req.request_id = request_id
        sub_req.sample_interval = sample_interval
        return metadata, sub_req