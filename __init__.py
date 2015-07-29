import log
from myParam import *
import logging
import time
import os

if __name__== '__main__':
    clientLog = log.brandClientLog()
    logHandler = log.brandRotatingFileHandler(os.path.join(brand_LOG_BASEPATH, brand_CLIENT_LOGDIR, brand_CLIENTLOG_BASENAME))
    __builtins__.brandClientLog = clientLog
    brandClientLog.addHandler(logHandler)
    brandClientLog.info("#...................................System Restarted......................................#")
    name = "brand Inc"
    i=0
    try:
        while 1:
            brandClientLog.debug("trying to log debug messages for :%s msg no.%d",name,i)
            brandClientLog.info("trying to log info messages for :%s msg no.%d", name, i)
            time.sleep(2)
            brandClientLog.warn("trying to log warn messages for :%s msg no.%d", name, i)
            brandClientLog.warning("trying to log warning messages for :%s msg no.%d", name, i)
            brandClientLog.error("trying to log error messages for :%s msg no.%d", name, i)
            time.sleep(2)
            brandClientLog.exception("trying to log exception messages for :%s msg no.%d", name, i)
            brandClientLog.critical("trying to log critical messages for :%s msg no.%d", name, i)
            i=i+1

            raise ArithmeticError
    except Exception as err:
        brandClientLog.exception(err)


