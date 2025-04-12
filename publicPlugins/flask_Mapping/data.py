import itertools
import os
import jinja2
from werkzeug.middleware.shared_data import SharedDataMiddleware

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

template_folder = config["template_folder"]  # if isinstance(config["template_folder"], (list, tuple)) else [config["template_folder"]]
static_folder = config["static_folder"]  # if isinstance(config["static_folder"], (list, tuple)) else [config["static_folder"]]
flaskAppName = config["flaskAppName"]

app = Flask(flaskAppName, template_folder=template_folder, static_folder=static_folder)
app.response_class = CustomResponse
# if isinstance(template_folder, list):
#     # 实现的路径 template_folder
#     app.jinja_loader = jinja2.ChoiceLoader([jinja2.FileSystemLoader(i)for i in template_folder])


appRegister(app, "flaskApp")

