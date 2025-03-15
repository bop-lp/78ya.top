
import os

from flask import Flask, send_file, render_template
from flask import request
from flask import jsonify

import inspect as inspectKB
from fileMapping import File, getAppRegister

__run__ = False


def run(flaskApp):
    class root(flaskApp):
        def wrongMethod(self, method):
            return {"code": 405, "message": f"I only accept the method {method}."}

    root = root("", interfaceInfo={"root": {"methods": "GET", "forms": {}}})
    path = File.public.config.get("file", False)

    # @root.wrapper("/download/<name>")
    def downloadMD(name: str):
        try:
            if path is False:
                return jsonify({
                    "code": 505,
                }), 500

            if not os.path.exists(os.path.join(path, name)):
                return jsonify({
                    "code": 404,
                    "status": f"没有找到文件 {name}",
                }), 404

            data = send_file(os.path.join(path, name), as_attachment=True)
            return data

        except Exception as f:
            return jsonify({
                "code": 500,
                "status": "error",
                "message": f"Error: {f}",
            }), 500

    # @root.wrapper("/")
    # def root():
    #     try:
    #         client_ip = request.headers.get("X-Real-IP", request.remote_addr)
    #     except:
    #         client_ip = False
    #
    #     # print(f"client_ip: {client_ip}")
    #     return jsonify({
    #         "code": 200,
    #         "status": "success",
    #         "message": "Welcome to fileMapping.",
    #         "client_ip": client_ip,
    #     })

    @root.wrapper("/")
    def root():
        return render_template("index.html")



flaskApp = getAppRegister("FlaskApp")
if not flaskApp is None:
    try:
        run(flaskApp)
    except Exception as e:
        print(f"Error: {e}")
        # rich.print(inspectKB.stack())/

print("fileMapping is running.")