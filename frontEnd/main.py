import os

import flask
from fileMapping import File, pathConversion, getAppRegister


config = {
    "rootPath": os.path.dirname(__file__),
    "flask": {
        "template_folder": os.path.join(os.path.dirname(__file__), "resources/templates"),
        "static_folder": os.path.join(os.path.dirname(__file__), "resources/static"),
    },
    "config": {
        "dataFolder": os.path.join(os.path.dirname(__file__), ""),
    }
}


plugins = [
    "plugins",
    "..\\publicPlugins"
]

f = File([pathConversion(__file__, i) for i in plugins], printLog=True, config=config)
# f = File(pathConversion(__file__, "plugins"), printLog=True, config=config)
if __name__ == '__main__':
    f.runAll()

    # createAContainer = getAppRegister("createAContainer")
    # md = createAContainer("78ya.top")
    # MD_html = getAppRegister("MD_html")
    # html = MD_html(md)
    # print(html.generated("test.md"))

    appRun = getAppRegister("AppRun")
    appRun(debug=True)



