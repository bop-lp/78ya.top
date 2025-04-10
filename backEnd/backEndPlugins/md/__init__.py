import os
import json

from .md import Container
from . import config


def end():
    """
    结束
    保存容器内的数据
    :return:
    """
    for key, value in Container.__data__.items():
        try:
            with open(os.path.join(value["path"], value["name"], "__container.json"), "w", encoding="utf-8") as f:
                json.dump(value, f, ensure_ascii=False, indent=4)

        except Exception as e:
            pass


# 从配置中拉取动态路径, MD_DATA 为默认路径
__dataFolders__ = [config.MD_DATA, os.path.join(config.MD_DATA, config.container_file)]

__end__ = end
