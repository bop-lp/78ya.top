import functools
import json

from flask import Flask, request

from fileMapping import appRegister

from . import data as flask_data


@appRegister
class FlaskApp:
    info = {"routing": [], "error": {}}

    # 这个是用来存储 flask 应用的信息的字典
    # routing 路由信息的 list [name, ...]
    # error 错误信息的 dict {code: message}

    def __init__(self, root: str, methods: list = None, interfaceInfo: dict = None):
        self.methods = methods if not methods is None else ["GET", "POST"]
        self.interfaceInfo = interfaceInfo if not interfaceInfo is None else {}
        # interfaceInfo 这个是用来存储 wrapper 应用的信息的字典
        # 可以每次请求的时候检查 请求的参数是否符合 里面的信息, 然后进行相应的操作

        self.root: str = root
        self.app: Flask = flask_data.app

        if root == '/':
            self.root = ''

        elif not root.startswith("/"):
            self.root = "/" + root

    def wrapper(self, path: str = None, **kwargs):
        """

        :param path: 当为空时, 默认使用 func.__name__
        :param kwargs: app.route 的参数
        :return:
        """
        def decorator(func):
            @self.app.route(f"{self.root}{path}", methods=self.methods, **kwargs)
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # 请求的参数是否符合 interfaceInfo 的信息
                if not self.interfaceInfo.get(func.__name__) is None:
                    _ = self.__judgmentRequests(request.method, func.__name__)
                    if _ != {}:
                        return _

                return func(*args, **kwargs)

            return wrapper

        return decorator

    def __judgmentRequests(self, method, name):
        if method != self.interfaceInfo[name]["methods"]:
            # 检查请求方法
            return self.wrongMethod(method)

        forms = self.__getTheParameters(method)
        haveTo = [
            key for key, data in self.interfaceInfo[name]["forms"].items() if data["haveTo"] == True
        ]
        for i in haveTo:
            if forms.get(i, False) is False:
                return self.badRequest(i)

        return {}

    def __getTheParameters(self, method):
        """
        :param method: 请求方法
        :return: dict
        """
        try:
            if method == "GET":
                forms = self.request_GET()

            else:
                forms = self.request_POST()

            return forms

        except json.decoder.JSONDecodeError:
            return {}

        except Exception:
            return {}

    def request_GET(self):
        return request.args.to_dict()

    def request_POST(self):
        return request.get_json()

    def wrongMethod(self, method):
        return {"code": 405, "message": f"Method {method} not allowed for this resource."}

    def badRequest(self, pals):
        return {
            "code": 400,
            "message": f"Bad Request! You need to provide the parameter {pals}"
            # "data": f"这是一个错误的请求! 您缺少了 {pals} 参数或者是这个参数出现错误"
        }
