import time

import uvicorn
from fastapi import FastAPI

from producer import Subscribe
from message import *
from utilities import *
from DataModels import *
app = FastAPI()

# 公共返回数据模型
out = Output()

# 解析message数据接口
@app.post("/decode")
def decode_message(parameter: MessageBody):
    res = decode_message(parameter.message)
    out.message = res
    if 'exception' in res:
        out.code = 500
        out.info = 'decode message error.'
    return out


# 动态订阅
@app.post("/subscribe")
def dialin_subscribe(parameter: SubsPara):
    # 组装数据
    sub_args_dict = dict(parameter)
    sub_args_dict['metadata'] = tuple([('username', parameter.username), ('password', parameter.password)])
    sub_args_dict['paths'] = [{'path': parameter.path, 'depth': parameter.depth}]

    subscribe_thread = Subscribe('subscribe', parameter.address, sub_args_dict)
    subscribe_thread.start()
    time.sleep(5)
    status = subscribe_thread.getStauts()
    if status is False:
        out.code = 500
        out.info = 'subscribe failed.'
    return out

def main(paras):
    # print(33)
    print(paras, type(paras), dict(paras))




if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    exit()
    parameter = 9
    main(parameter)
