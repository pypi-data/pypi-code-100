"""
Class used to create logs with messages and screenshots in Logs folder
"""
import os
import sys
from datetime import datetime
import pyautogui


class LogHTML:

    DEBUG="DEBUG"
    INFO="INFO"
    WARNING="WARNING"
    ERROR="ERROR"
    CRITICAL="CRITICAL"
    screenshot_use=True
    createdLog = 0
    screenshotNumber = 0
    testLogFolderPath = ""
    drivers = None
    fileName=""
    logLevel="DEBUG"
    shouldMeasure=False

    @staticmethod
    def set_log_path(folderPath):
        if LogHTML.createdLog == 0:
            logName = os.path.basename(sys.argv[0])
            logFolderPath = folderPath
            try:
                any(x.startswith(logName) for x in os.listdir(logFolderPath))
            except:
                LogHTML.shouldMeasure=False
                if folderPath!="":
                    print("Wrong path for logging: "+folderPath)
                return
            if any(x.startswith(logName) for x in os.listdir(logFolderPath)):
                logFolderNumbers = []
                for x in os.listdir(logFolderPath):
                    if x.startswith(logName):
                        try:
                            logFolderNumbers.append(int(x.split("-")[1]))
                        except:
                            pass
                try:
                    newNumber = max(logFolderNumbers)
                except:
                    newNumber = 0
                newTestLogFolderPath = newNumber + 1
                testLogFolderPath = os.path.join(logFolderPath, logName + "-" + str(newTestLogFolderPath))
                os.mkdir(testLogFolderPath)
            else:
                testLogFolderPath = os.path.join(logFolderPath, logName)
                os.mkdir(testLogFolderPath)
            LogHTML.testLogFolderPath = testLogFolderPath
            LogHTML.fileName = os.path.join(testLogFolderPath, logName + ".html")
            with open(LogHTML.fileName, 'w'):
                pass
            LogHTML.createdLog = 1
            LogHTML.shouldMeasure=True

    @staticmethod
    def set_logging_level(level, use_screenshot=True):
        LogHTML.logLevel=level
        LogHTML.screenshot_use = use_screenshot

    @staticmethod
    def log_level_check(type):
        if(LogHTML.logLevel==LogHTML.DEBUG):
            return True
        elif(LogHTML.logLevel==LogHTML.INFO):
            if(type==LogHTML.DEBUG):
                return False
            else:
                return True
        elif (LogHTML.logLevel == LogHTML.WARNING):
            if (type == LogHTML.DEBUG or type == LogHTML.INFO):
                return False
            else:
                return True
        elif (LogHTML.logLevel == LogHTML.ERROR):
            if (type == LogHTML.ERROR or type == LogHTML.CRITICAL):
                return True
            else:
                return False
        elif (LogHTML.logLevel == LogHTML.CRITICAL):
            if (type == LogHTML.CRITICAL):
                return True
            else:
                return False



    @staticmethod
    def __write_msg(msg, type):
        if LogHTML.shouldMeasure:
            if LogHTML.log_level_check(type):
                if LogHTML.createdLog > 0:
                    time = str(datetime.now()).split(".")[0]
                    msg = time + " -- "+type+": " + msg
                    with open(LogHTML.fileName, 'a') as f:
                        f.writelines("<p>"+msg+"</p><hr>\n")

    @staticmethod
    def info(msg):
        """
        Log info message in log

        :param msg: Message to log
        :type msg: str
        """
        LogHTML.__write_msg(msg, LogHTML.INFO)

    @staticmethod
    def debug(msg):
        """
        Log debug message in log

        :param msg: Message to log
        :type msg: str
        """
        LogHTML.__write_msg(msg, LogHTML.DEBUG)

    @staticmethod
    def warning(msg):
        """
        Log warning message in log

        :param msg: Message to log
        :type msg: str
        """
        LogHTML.__write_msg(msg, LogHTML.WARNING)

    @staticmethod
    def error(msg):
        """
        Log error message in log

        :param msg: Message to log
        :type msg: str
        """
        LogHTML.__write_msg(msg, LogHTML.ERROR)

    @staticmethod
    def critical(msg):
        """
        Log critical message in log

        :param msg: Message to log
        :type msg: str
        """
        LogHTML.__write_msg(msg, LogHTML.CRITICAL)




    @staticmethod
    def screenshot(msg=""):
        """
        Log screenshot with message

        :param msg: Message to log
        :type msg: str
        """
        if LogHTML.screenshot_use and LogHTML.shouldMeasure:
            if LogHTML.createdLog > 0:
                time = str(datetime.now()).split(".")[0]
                msg = time + " -- IMG: " + msg
                screenshotName = str(LogHTML.screenshotNumber) + ".png"
                picturePath = os.path.join(LogHTML.testLogFolderPath, screenshotName)
                LogHTML.screenshotNumber += 1
                pyautogui.screenshot(picturePath)
                with open(LogHTML.fileName, 'a') as f:
                    f.write("<p><a href='{}'><img src='{}' height='150px' width='200px'></img></a><br>{}</p><hr>\n".format(screenshotName, screenshotName,msg))

    @staticmethod
    def screenshotSelenium(driver, msg=""):
        """
        Log screenshot with message

        :param msg: Message to log
        :type msg: str
        """
        if LogHTML.screenshot_use and LogHTML.shouldMeasure:
            if LogHTML.createdLog > 0:
                time = str(datetime.now()).split(".")[0]
                msg = time + " -- IMG: " + msg
                screenshotName = str(LogHTML.screenshotNumber) + ".png"
                picturePath = os.path.join(LogHTML.testLogFolderPath, screenshotName)
                LogHTML.screenshotNumber += 1
                driver.save_screenshot(picturePath)
                with open(LogHTML.fileName, 'a') as f:
                    f.write("<p><a href='{}'><img src='{}' height='150px' width='200px'></img></a><br>{}</p><hr>\n".format(screenshotName, screenshotName,msg))


