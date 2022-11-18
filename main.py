import time
from typing import Union

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from producer import Subscribe

app = FastAPI()

# 传递参数数据模型
class Parameter(BaseModel):
    username: str
    password: str
    address: str
    path: str | None = 'huawei-debug:debug/cpu-infos/cpu-info'
    depth: int | None = 1
    sample_interval: int | None = 1000
    request_id: int | None = 3

# 动态订阅
@app.post("/subscribe")
def dialin_subscribe(parameter: Parameter):
    # print(paras)
    sub_args_dict = dict(parameter)
    sub_args_dict['metadata'] = tuple([('username', parameter.username), ('password', parameter.password)])
    sub_args_dict['paths'] = [{'path': parameter.path, 'depth': parameter.depth}]

    print(sub_args_dict)
    subscribe_thread = Subscribe('subscribe', parameter.address, sub_args_dict)
    subscribe_thread.start()
    time.sleep(5)
    status = subscribe_thread.getStauts()
    d = {'info': 'success', 'code': 200}
    if status is False:
        d['info'] = 'fail'
    return d

def main(paras):
    # print(33)
    print(paras, type(paras), dict(paras))




if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    exit()
    parameter = 9
    main(parameter)
