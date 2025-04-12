import os
from pathlib import Path

import markdown
import frontmatter
from datetime import datetime

from flask import Flask, send_file, render_template, make_response
from flask import request
from flask import jsonify

import inspect as inspectKB
from fileMapping import File, getAppRegister

__run__ = False
path = File.public.config['flask']['static_folder']
POSTS_DIR = Path(os.path.join(path, 'md'))


class Post:
    def __init__(self, path):
        post = frontmatter.load(path)
        self.slug = path.stem
        self.title = post.metadata.get("title", "未命名文章")
        self.date = post.metadata.get("date", datetime.now())
        self.content = markdown.markdown(post.content, extensions=["fenced_code"])

        content = post.content.replace('<img ', '<img class="md-image" ')
        self.content = markdown.markdown(content, extensions=[
            'fenced_code',
            'attr_list'  # 启用属性列表扩展
        ])


def get_posts():
    return sorted(
        [Post(p) for p in POSTS_DIR.glob("*.md")],
        key=lambda x: x.date,
        reverse=True
    )


def run(flaskApp):
    class root(flaskApp):
        def wrongMethod(self, method):
            return {"code": 405, "message": f"I only accept the method {method}."}

    root_wed = root("", interfaceInfo={"root": {"methods": "GET", "forms": {}}})
    # path = File.public.config.get("file", False)

    @root_wed.wrapper("/posts/<slug>")
    def show_post(slug):
        post_path = POSTS_DIR / f"{slug}.md"
        if not post_path.exists():
            return "文章不存在", 404

        post = Post(post_path)
        post.title = slug
        return render_template("post.html", post=post)

    @root_wed.wrapper("/")
    def root():
        return render_template("login.html")

    @root_wed.wrapper("/md/list/<pages>")
    def md_list(pages: int):
        """

        :param pages: 页数
        :return: 返回 md html
        """
        response = make_response({"page": pages, "content": render_template("md_list.html")})
        response.headers.add('Access-Control-Allow-Origin', '*')  # 允许所有来源访问
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST')  # 允许 GET 和 POST 请求
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')  # 允许的请求头


        return response


flaskApp = getAppRegister("FlaskApp")
if not flaskApp is None:
    try:
        run(flaskApp)
    except Exception as e:
        print(f"Error: {e}")
        # rich.print(inspectKB.stack())/

