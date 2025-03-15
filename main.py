import os

import flask
from fileMapping import File, pathConversion, getAppRegister


config = {
    "flask": {
        "template_folder": os.path.join(os.path.dirname(__file__), "resources/templates"),
        "static_folder": os.path.join(os.path.dirname(__file__), "resources/static"),
    }
}

f = File(pathConversion(__file__, "plugins"), printLog=True, config=config)
if __name__ == '__main__':
    f.runAll()

    #
    appRun = getAppRegister("AppRun")
    appRun()


