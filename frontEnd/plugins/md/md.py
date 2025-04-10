"""
plugins/md.py 文件的作用是
创建一个md容器, 让每一个md都有独立的空间(这么说好像也不对，因为一个容器内可以有多个md文件, 哈哈哈，不管了!)
防止图片重名，或者文件重名
"""
import json
import os

import frontmatter
import markdown

from fileMapping import appRegister
from fileMapping import plugIns, server

from . import config



@appRegister
class Container:
    """
    md容器类
    """
    __data__ = {}  # 容器的数据

    def __init__(self, name: str, alias: str = None):
        """
        初始化 md容器

        :param name: 容器名称
        :param alias: 别名
        """
        self.name = name
        self.alias = alias if alias else name
        self.path = os.path.join(plugIns.dataFolders(config.MD_DATA), config.container_file)
        if name not in os.listdir(self.path):
            # 创建容器
            self.createAContainer(name, alias)

        else:
            # 打开已有容器
            if not os.path.isfile(os.path.join(self.path, name, "__container.json")):
                # __container.json 文件不存在,说明该容器容器缺失,将对文件进行补全
                self.__completion__()
                self.__container()
            self.openTheContainer(name)

    def __completion__(self):
        """
        补全文件

        :return:
        """
        self.data = {
            "name": self.name,
            "alias": self.alias,
            "path": self.path,
            "fileDATA": {}
        }
        path = os.path.join(self.path, self.name)
        for i in os.listdir(path):
            if os.path.isfile(os.path.join(path, i)):
                self.data["fileDATA"][i] = {
                    "name": i,
                    "path": os.path.join(self.path, self.name, i),
                    "md5": server.small.file_md5(os.path.join(self.path, self.name, i))
                }

        self.__data__[self.name] = self.data

    def __container(self):
        """
        保存 container.json
        :return:
        """
        with open(os.path.join(self.path, self.name, "__container.json"), "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def createAContainer(self, name: str, alias: str = None):
        """
        创建 md容器
        :param name: 容器名称
        :param alias: 别名
        :return:
        """
        # 创建容器
        os.mkdir(os.path.join(self.path, name))
        self.name = name
        self.alias = alias if alias else name
        self.path = os.path.join(self.path, name)
        self.data = {
            "name": self.name,
            "alias": self.alias,
            "path": self.path,
            "fileDATA": {}
        }
        self.__data__[self.name] = self.data
        self.__container()

    def openTheContainer(self, name: str):
        """
        打开 md容器
        :param name:
        :return:
        """
        file = os.path.join(self.path, name, "__container.json")
        with open(file, "r", encoding="utf-8") as f:
            self.data = json.load(f)
            self.name = self.data["name"]
            self.alias = self.data["alias"]
            self.path = self.data["path"]
            self.__data__[self.name] = self.data

    def upload(self, data: str | bytes, name: str):
        """
        上传文件

        :param data:
        :param name:
        :return:
        """
        if isinstance(data, str):
            with open(os.path.join(self.path, self.name, name), "w", encoding="utf-8") as f:
                f.write(data)

        else:
            with open(os.path.join(self.path, self.name, name), "wb") as f:
                f.write(data)

        self.data["fileDATA"][name] = {
            "name": name,
            "path": os.path.join(self.path, name),
            "md5": server.small.file_md5(os.path.join(self.path, name))
        }

    def delete(self, name: str):
        """
        删除文件

        :param name:
        :return:
        """
        if name in self.data["fileDATA"]:
            os.remove(self.data["fileDATA"][name]["path"])
            del self.data["fileDATA"][name]
            return True

        else:
            return False

    def getFiles(self):
        """
        获取文件列表

        :return:
        """
        return list(self.data["fileDATA"].keys())

    def getMD(self, name: str):
        """
        获取文件内容

        :param name:
        :return:
        """
        if name in self.data["fileDATA"]:
            with open(self.data["fileDATA"][name]["path"], "r", encoding="utf-8") as f:
                return f.read()

        else:
            return None


@appRegister
class MD_html:
    def __init__(self, container: Container):
        """
        生成 html
        :param md_text:
        """
        if isinstance(container, Container):
            self.container = container
        else:
            raise TypeError("The container must be a Container object")

    def generated(self, md_text: str, url: str = ''):
        """
        生成 html
        :param url:
        :param md_text:
        :return:
        """
        path_file = os.path.join(self.container.path, self.container.name, md_text)
        post = frontmatter.load(path_file)
        md_html = markdown.markdown(
                post.content
        ).replace('src="/', f'src="/{url}')
        return md_html


@appRegister
def createAContainer(name: str, alias: str = None):
    """
    创建 & 打开 md容器

    :return:
    """
    if plugIns.dataFolders(config.MD_DATA) != False:
        try:
            return Container(name, alias)

        except FileExistsError as e:
            return False

    else:
        return False


@appRegister
def deleteAContainer(name: str):
    """
    删除 md容器

    :param name:
    :return:
    """
    if plugIns.dataFolders(config.MD_DATA) != False:
        path = plugIns.dataFolders(os.path.join(config.MD_DATA, config.container_file))
        if name in os.listdir(path):
            os.rmdir(os.path.join(path, name))
            return True

        else:
            return False

    else:
        return False


@appRegister
def getContainers():
    """
    获取 md容器列表

    :return:
    """
    if plugIns.dataFolders(config.MD_DATA) != False:
        path = plugIns.dataFolders(os.path.join(config.MD_DATA, config.container_file))
        containers = []
        for container in os.listdir(path):
            if os.path.isdir(os.path.join(path, container)):
                containers.append(container)

        return containers

    else:
        return []

