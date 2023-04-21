# -*- coding: utf-8 -*-
# @Author: Noaghzil
# @Date:   2023-04-21 08:06:16
# @Last Modified by:   Noaghzil
# @Last Modified time: 2023-04-21 08:06:16
from fastapi import FastAPI, Request
from fastapi.middleware.base import BaseHTTPMiddleware

app = FastAPI()

# 定义中间件类
class HeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 获取 header 中的参数，这里假设参数名为 "my-header"
        my_header = request.headers.get("my-header")
        # 将参数放入指定的入参中，这里假设参数名为 "header_param"
        request.scope["header_param"] = my_header

        # 调用下一个中间件或路由处理函数
        response = await call_next(request)

        return response

# 定义路由处理函数
@app.get("/")
async def index(header_param: str):
    # 使用经过中间件处理的参数
    return {"header_param": header_param}

# 将中间件添加到应用中
app.middleware("http")(HeaderMiddleware)
