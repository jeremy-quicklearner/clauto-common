import time

from util.log import Log

mylog = Log("/var/log/clauto")
mylog = Log()

while 1:
    time.sleep(1)
    mylog.level_set("CRT")
    mylog.critical("This message is critical")
    mylog.config("This message is configgey")
    mylog.error("This message is errorey")
    mylog.warning("This message is a warning")
    mylog.info("This message is informative")
    mylog.debug("This message is debuggey")
    mylog.verbose("This message is verbose")

    mylog.level_set("CFG")
    mylog.critical("This message is critical")
    mylog.config("This message is configgey")
    mylog.error("This message is errorey")
    mylog.warning("This message is a warning")
    mylog.info("This message is informative")
    mylog.debug("This message is debuggey")
    mylog.verbose("This message is verbose")

    mylog.level_set("ERR")
    mylog.critical("This message is critical")
    mylog.config("This message is configgey")
    mylog.error("This message is errorey")
    mylog.warning("This message is a warning")
    mylog.info("This message is informative")
    mylog.debug("This message is debuggey")
    mylog.verbose("This message is verbose")

    mylog.level_set("WRN")
    mylog.critical("This message is critical")
    mylog.config("This message is configgey")
    mylog.error("This message is errorey")
    mylog.warning("This message is a warning")
    mylog.info("This message is informative")
    mylog.debug("This message is debuggey")
    mylog.verbose("This message is verbose")

    mylog.level_set("INF")
    mylog.critical("This message is critical")
    mylog.config("This message is configgey")
    mylog.error("This message is errorey")
    mylog.warning("This message is a warning")
    mylog.info("This message is informative")
    mylog.debug("This message is debuggey")
    mylog.verbose("This message is verbose")

    mylog.level_set("DBG")
    mylog.critical("This message is critical")
    mylog.config("This message is configgey")
    mylog.error("This message is errorey")
    mylog.warning("This message is a warning")
    mylog.info("This message is informative")
    mylog.debug("This message is debuggey")
    mylog.verbose("This message is verbose")

    mylog.level_set("VRB")
    mylog.critical("This message is critical")
    mylog.config("This message is configgey")
    mylog.error("This message is errorey")
    mylog.warning("This message is a warning")
    mylog.info("This message is informative")
    mylog.debug("This message is debuggey")
    mylog.verbose("This message is verbose")
