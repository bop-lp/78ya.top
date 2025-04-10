from fileMapping import appRegister, File
from fileMapping.helperFunctions_expansion.helperFunctions import deep_update, configConvertTodict

from . import Register
from . import data
from . import config

# API
from .funos import nameLegitimacyChecks

# __run__ = False
__level__ = 2

__version__ = "0.0.1"
__description__ = "File Mapping Flask Plugin"


# def main():
config = deep_update(configConvertTodict(config), File.public["config"].get("flask", {}))


def run():
    host = config["host"]
    port = config["port"]

    data.app.run(host=host, port=port)

appRegister(run, "AppRun")
appRegister(nameLegitimacyChecks)
