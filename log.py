import logging
import logging.handlers
import myParam
import os
import time

class brandLog():
    def __init__(self):
        self.logLevel = myParam.brand_LOG_LEVEL

    def getLogger(self):
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        self.setFormatter(fmt='[%(asctime)s %(name)s.%(levelname)s] %(message)s', datefmt='%m-%d-%Y %H:%M:%S') 
        #by default we are setting the default handler for the logger
        #which is the StreamHandler. When user creates his own custome handler
        #we will remove this handler.
        return logger

    def getLevelName(self, level):
        return logging.getLevelName(level)

    def addLevelName(self, level, LevelName):
        logging.addLevelName(level, LevelName)
    
    def setFormatter(self, fmt='[%(asctime)s %(name)s.%(levelname)s] %(message)s', datefmt='%m-%d-%Y %H:%M:%S'):
        self.formatter=logging.Formatter(fmt=fmt, datefmt=datefmt)

    #have some code to add filter mechanism
    #verified
    def disable(self, level):
        logging.disable(level)

    #need to verify for streamhandler. I feel that stdout is not flushed or closed
    def shutdown(self):
        logging.shutdown()

class brandClientLog(brandLog):
    def __init__(self, name=myParam.brand_CLIENT_LOGGER, level=myParam.DEBUG_LEVEL['DEBUG']):
        brandLog.__init__(self)
        self.name = name
        self.level = level
        self.logger = self.getLogger() 
        
    def debug(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'DEBUG'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.debug("Houston, we have a %s", "thorny problem", exc_info=1)
        """
        if self.logger.isEnabledFor(self.logLevel['DEBUG']):
            self.logger._log(self.logLevel['DEBUG'], msg, args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'INFO'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.info("Houston, we have a %s", "interesting problem", exc_info=1)
        """
        if self.logger.isEnabledFor(self.logLevel['INFO']):
            self.logger._log(self.logLevel['INFO'], msg, args, **kwargs) 

    def warning(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'WARNING'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.warning("Houston, we have a %s", "bit of a problem", exc_info=1)
        """
        if self.logger.isEnabledFor(self.logLevel['WARNING']):
            self.logger._log(self.logLevel['WARNING'], msg, args, **kwargs)

    warn = warning   
    
    def error(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'ERROR'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.error("Houston, we have a %s", "major problem", exc_info=1)
        """
        if self.logger.isEnabledFor(self.logLevel['ERROR']):
            self.logger._log(self.logLevel['ERROR'], msg, args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        """
        Convenience method for logging an ERROR with exception information.
        """
        kwargs['exc_info'] = 1
        self.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'CRITICAL'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.critical("Houston, we have a %s", "major disaster", exc_info=1)
        """
        if self.logger.isEnabledFor(self.logLevel['CRITICAL']):
            self.logger._log(self.logLevel['CRITICAL'], msg, args, **kwargs)

    fatal = critical 
    
    def log(self, level, msg, *args, **kwargs):
        self.logger._log(level, msg, args, **kwargs) 

    def addHandler(self, hdlr):
        hdlr.setFormatter(self.formatter)
        self.logger.addHandler(hdlr)

    def removeHandler(self, hdlr):
        hdlr.setLevel(self.level)
        self.logger.removeHandler(hdlr)


class brandServerLog(brandLog):
    def __init__(self):
        pass

class brandFutureLog(brandLog):
    def __init__(Self):
        pass

class brandRotatingFileHandler(logging.handlers.RotatingFileHandler):
    def __init__(self, filename, mode='a', maxBytes=myParam.CLIENT_LOG_SIZE, backupCount=myParam.CLIENT_LOGBKP_COUNT, encoding=None, delay=0):
        #filepath should be absolute path with appended filebasename
        self.logdir = os.path.join(myParam.brand_LOG_BASEPATH, myParam.brand_CLIENT_LOGDIR)
        if not os.path.exists(self.logdir):
            print 'making log directories'
            os.makedirs(self.logdir)
        self.filename = filename
        self.fileCount = 1
        self.filepath = self.getFilepath()
        self.maxBytes = maxBytes
        self.backupCount = backupCount
        logging.handlers.RotatingFileHandler.__init__(self, self.filepath, mode, maxBytes=maxBytes, backupCount=backupCount, encoding=encoding, delay=delay)
        #add other custome parameters of you want to add
        
    
    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
            print 'doing rollover'
            print 'filecount',self.fileCount
            print 'maxBytes',self.maxBytes
            print 'backupCount',self.backupCount
            print 'closed basefile',self.baseFilename
        if self.backupCount > 0:
            if self.fileCount < self.backupCount:
                self.baseFilename = self.getNewFilename()
                self.fileCount = self.fileCount+1
            else:
                #should delete oldest log file
                if os.path.exists(self.logdir):
                    logFiles = os.listdir(self.logdir)
                    logFiles.sort()
                    if logFiles:
                        os.remove(os.path.join(self.logdir, logFiles[0]))
                    self.baseFilename = self.getNewFilename()
                else:
                    print 'pass in doRollover getting called'
                    pass
        if not self.delay:
            print 'opening new file with basename:',self.baseFilename
            self.stream = self._open()
            
                
    def getFilepath(self):
        print 'getFilepath'
        if os.path.exists(self.logdir):
            logFiles = os.listdir(self.logdir)
            if logFiles:
                logFiles.sort(reverse=True)
                self.fileCount = len(logFiles)
                print 'continuing with old file since restart'
                return os.path.join(self.logdir,logFiles[0])
        self.fileCount = 1
        return self.getNewFilename()

    def getNewFilename(self):
        print 'getting new file for logging'
        suffix = time.strftime("-%m-%d-%H-%M-%S.log",time.localtime())
        filePrefixPath = os.path.join(self.logdir, self.filename)
        return filePrefixPath+suffix
