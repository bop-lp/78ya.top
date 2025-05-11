import os
from pathlib import Path

import markdown
import frontmatter
from datetime import datetime

from flask import Flask, send_file, render_template
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
    path = File.public.config.get("file", False)

    @root_wed.wrapper("/about")
    def about():
        return render_template("about.html")


    @root_wed.wrapper("/blog")
    def blog():
        return render_template("blog.html")

    @root_wed.wrapper("/home")
    def root():
        return render_template("home.html")

    @root_wed.wrapper("/tools")
    def tools():
        return render_template("tools.html")

    @root_wed.wrapper("/")
    def root():
        return render_template("home.html")


    @root_wed.wrapper("/posts/<slug>")
    def show_post(slug):
        post_path = POSTS_DIR / f"{slug}.md"
        if not post_path.exists():
            return "文章不存在", 404

        post = Post(post_path)
        post.title = slug
        return render_template("post.html", post=post)

    # @root_wed.wrapper("/api/dmyiyan/api")
    # def dmyiyan_api():
    #     return "你好世界", 200


flaskApp = getAppRegister("FlaskApp")
if not flaskApp is None:
    try:
        run(flaskApp)
    except Exception as e:
        print(f"Error: {e}")
        # rich.print(inspectKB.stack())/

print("fileMapping is running.")
