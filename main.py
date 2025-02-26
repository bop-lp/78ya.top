import flask
from fileMapping import File, pathConversion, getAppRegister


f = File(pathConversion(__file__, "plugins"), printLog=True)
if __name__ == '__main__':
    f.runAll()

    #
    # appRun = getAppRegister("AppRun")
    # appRun()


