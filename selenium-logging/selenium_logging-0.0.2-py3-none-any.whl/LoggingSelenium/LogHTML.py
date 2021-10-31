"""
Class used to create logs with messages and screenshots in Logs folder
"""
import os
import sys
from datetime import datetime
import pyautogui


class LogHTML:

    createdLog = 0
    screenshotNumber = 0
    testLogFolderPath = ""
    drivers = None
    fileName=""

    @staticmethod
    def set_log_path(folderPath):
        if LogHTML.createdLog == 0:
            logName = os.path.basename(sys.argv[0])
            logFolderPath = folderPath
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

    @staticmethod
    def info(msg):
        """
        Log info message in log

        :param msg: Message to log
        :type msg: str
        """
        time = str(datetime.now()).split(".")[0]
        msg = time + " -- " + msg
        with open(LogHTML.fileName, 'a') as f:
            f.writelines("<p>"+msg+"</p>\n")

    @staticmethod
    def screenshot(msg=""):
        """
        Log screenshot with message

        :param msg: Message to log
        :type msg: str
        """
        time = str(datetime.now()).split(".")[0]
        msg = time + " -- " + msg
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
        time = str(datetime.now()).split(".")[0]
        msg = time + " -- " + msg
        screenshotName = str(LogHTML.screenshotNumber) + ".png"
        picturePath = os.path.join(LogHTML.testLogFolderPath, screenshotName)
        LogHTML.screenshotNumber += 1
        driver.save_screenshot(picturePath)
        with open(LogHTML.fileName, 'a') as f:
            f.write("<p><a href='{}'><img src='{}' height='150px' width='200px'></img></a><br>{}</p><hr>\n".format(screenshotName, screenshotName,msg))


