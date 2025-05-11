"""
为实现前后端分离

"""

import os

import flask
from fileMapping import File, pathConversion, getAppRegister



file_path = os.path.dirname(__file__)
config = {
    "rootPath": file_path,
    "flask": {
        "template_folder": os.path.join(file_path, "resources/templates"),
        "static_folder": os.path.join(file_path, "resources/static"),
        "host": "0.0.0.0",
        "port": 83
    },
    "config": {
        "dataFolder": os.path.join(file_path, "file_DATA"),
    }
}

plugins = [
    "backEndPlugins",
    "..\\publicPlugins"
]

f = File([pathConversion(__file__, i) for i in plugins], printLog=True, config=config)
if __name__ == '__main__':
    f.runAll()


    appRun = getAppRegister("AppRun")
    appRun(debug=True)

