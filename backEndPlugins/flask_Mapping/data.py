from fileMapping import File, configConvertTodict
from fileMapping.helperFunctions_expansion.helperFunctions import deep_update
from fileMapping import appRegister

from flask import Flask, Response

from . import config


class CustomResponse(Response):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 移除 Server 头
        del self.headers['Server']


config = deep_update(configConvertTodict(config), File.public["config"].get("flask", {}))
# 生成一个config对象，并将File.public["config"]合并到config中

template_folder = config["template_folder"]
static_folder = config["static_folder"]


app = Flask(config["flaskAppName"], template_folder=template_folder, static_folder=static_folder)
app.response_class = CustomResponse

appRegister(app, "flaskApp")

