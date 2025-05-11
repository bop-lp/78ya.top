from fileMapping import File

dataFolders = "MD_DATA"

MD_DATA = File.public.get('config', {}).get("dataFolders", dataFolders)

container_file = File.public.get('config', {}).get("container", "container")
# 专门用于装容器的文件夹
