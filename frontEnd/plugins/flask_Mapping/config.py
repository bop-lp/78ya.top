# 这个文件是Flask插件的配置文件，用于配置插件的一些参数


host = "127.0.0.1"
# 0.0.0.0 表示允许任何IP访问，如果只允许局域网访问，可以改成192.168.0.0/16之类的
port = 82

flaskAppName = "flask"
aliasRouting = True

template_folder = "templates"
static_folder = "static"

"""
如果aliasRouting为True,  当注册路由时有2个相同的函数名情况, 会自动给第二个函数添加一个别名, 例如: 
@xxx.wrapper("/index")
def index(): ...

@xxx.wrapper("/index2")
def index(): ...  # index -> index2

index2 会自动注册为/index2的别名, 这样可以避免函数名重复的问题.
"""

