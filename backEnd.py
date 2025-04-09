"""
为实现前后端分离

"""

import os

import flask
from fileMapping import File, pathConversion, getAppRegister



config = {
    "rootPath": os.path.dirname(__file__),
    "flask": {
        "template_folder": os.path.join(os.path.dirname(__file__), "resources/templates"),
        "static_folder": os.path.join(os.path.dirname(__file__), "resources/static"),
        "port": 83
    },
    "config": {
        "dataFolder": os.path.join(os.path.dirname(__file__), "file_data"),
    }
}


f = File(pathConversion(__file__, "backEndPlugins"), printLog=True, config=config)
if __name__ == '__main__':
    f.runAll()


    appRun = getAppRegister("AppRun")
    appRun()

