from fileMapping import appRegister

from . import Register
from . import data

# API
from .funos import nameLegitimacyChecks

__run__ = False
__level__ = 2

__version__ = "0.0.1"
__description__ = "File Mapping Flask Plugin"

# @register.threadRegistration(__level__=-1)
def run():
    host = data.config["host"]
    port = data.config["port"]

    data.app.run(host=host, port=port)

appRegister(run, "AppRun")
appRegister(nameLegitimacyChecks)
