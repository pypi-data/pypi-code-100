import colorama, traceback
from python_helper.api.src.domain import Constant as c
from python_helper.api.src.service import SettingHelper, StringHelper, EnvironmentHelper, ObjectHelper, ReflectionHelper

LOG = 'LOG'
INFO = 'INFO'
STATUS = 'STATUS'
SUCCESS = 'SUCCESS'
SETTING = 'SETTING'
DEBUG = 'DEBUG'
WARNING = 'WARNING'
WRAPPER = 'WRAPPER'
FAILURE = 'FAILURE'
ERROR = 'ERROR'
TEST = 'TEST'

RESET_ALL_COLORS = colorama.Style.RESET_ALL

ENABLE_LOGS_WITH_COLORS = 'ENABLE_LOGS_WITH_COLORS'

from python_helper.api.src.helper import LogHelperHelper

global LOG_HELPER_SETTINGS

def logsWithColorsEnabled():
    return EnvironmentHelper.isTrue(ENABLE_LOGS_WITH_COLORS, default=False)

# import asyncio
# global OUTPUT_PRINT_LIST
# PRINTING = 'PRINTING'
# def loadLogger() :
#     global OUTPUT_PRINT_LIST
#     try :
#         if ObjectHelper.isNone(OUTPUT_PRINT_LIST) :
#             OUTPUT_PRINT_LIST = []
#     except Exception as exception :
#         OUTPUT_PRINT_LIST = []
#
# async def asyncAsyncPrintIt(itArgsAndKwargs) :
#     global LOG_HELPER_SETTINGS
#     while LOG_HELPER_SETTINGS[PRINTING] :
#         print('----------------------------------------------------------------------------------------------------------------------------------------------------------')
#         print('----------------------------------------------------------------------------------------------------------------------------------------------------------')
#         print('----------------------------------------------------------------------------------------------------------------------------------------------------------')
#         print('----------------------------------------------------------------------------------------------------------------------------------------------------------')
#         print('----------------------------------------------------------------------------------------------------------------------------------------------------------')
#         print('----------------------------------------------------------------------------------------------------------------------------------------------------------')
#         print('----------------------------------------------------------------------------------------------------------------------------------------------------------')
#         print('------------------------------------------------------------------------ awaiting ------------------------------------------------------------------------')
#         print('----------------------------------------------------------------------------------------------------------------------------------------------------------')
#         print('----------------------------------------------------------------------------------------------------------------------------------------------------------')
#         print('----------------------------------------------------------------------------------------------------------------------------------------------------------')
#         print('----------------------------------------------------------------------------------------------------------------------------------------------------------')
#         print('----------------------------------------------------------------------------------------------------------------------------------------------------------')
#         print('----------------------------------------------------------------------------------------------------------------------------------------------------------')
#         print('----------------------------------------------------------------------------------------------------------------------------------------------------------')
#     LOG_HELPER_SETTINGS[PRINTING] = True
#     print(itArgsAndKwargs[0], **itArgsAndKwargs[1])
#
# async def asyncPrintIt(itArgsAndKwargs) :
#     global LOG_HELPER_SETTINGS
#     await asyncAsyncPrintIt(itArgsAndKwargs)
#     LOG_HELPER_SETTINGS[PRINTING] = False
#
# async def printOutput() :
#     global OUTPUT_PRINT_LIST
#     while 0 < len(OUTPUT_PRINT_LIST) :
#         asyncio.run(asyncPrintIt(OUTPUT_PRINT_LIST.pop(0)))
#
# def logIt(it, **kwargs) :
#     global OUTPUT_PRINT_LIST
#     shouldPrint = True if 0 == len(OUTPUT_PRINT_LIST) else False
#     OUTPUT_PRINT_LIST.append([it, kwargs])
#     if shouldPrint :
#         printOutput()
# import logging
# LOGGER_INSTANCE = None

# def loadLogger(logger) :
#     return logger if ObjectHelper.isNotNone(logger) else logging.getLogger(__name__)

def logIt(it, **kwargs) :
    # logging.error(it, **kwargs)
    # logging.log(msg=args[0], level=9)
    # logger = loadLogger(LOGGER_INSTANCE)
    # logger.setLevel(logging.DEBUG)
    # logger.info(it)
    print(it, **kwargs)

def loadSettings() :
    global LOG_HELPER_SETTINGS
    # logger = loadLogger(LOGGER_INSTANCE)
    # logger.setLevel(logging.DEBUG)
    ###- logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    colorama.deinit()
    settings = {}
    settings[SettingHelper.ACTIVE_ENVIRONMENT] = SettingHelper.getActiveEnvironment()
    for level in LogHelperHelper.LEVEL_DICTIONARY :
        settings[level] = c.TRUE if EnvironmentHelper.isTrue(level, default=True) else c.FALSE
    LOG_HELPER_SETTINGS = settings
    if logsWithColorsEnabled():
        colorama.init()
        # logging.basicConfig(level=logging.DEBUG)
        logIt(RESET_ALL_COLORS, end=c.BLANK)

loadSettings()

def log(origin, message, exception=None, muteStackTrace=False, newLine=False, level=LOG) :
    LogHelperHelper.softLog(origin, message, level, muteStackTrace=muteStackTrace, newLine=newLine, exception=exception)

def info(origin, message, newLine=False) :
    LogHelperHelper.softLog(origin, message, INFO, muteStackTrace=True, newLine=newLine)

def status(origin, message, newLine=False) :
    LogHelperHelper.softLog(origin, message, STATUS, muteStackTrace=True, newLine=newLine)

def success(origin, message, newLine=False) :
    LogHelperHelper.softLog(origin, message, SUCCESS, muteStackTrace=True, newLine=newLine)

def setting(origin, message, muteStackTrace=False, newLine=False) :
    LogHelperHelper.softLog(origin, message, SETTING, muteStackTrace=muteStackTrace, newLine=newLine)

def debug(origin, message, exception=None, muteStackTrace=False, newLine=False) :
    LogHelperHelper.softLog(origin, message, DEBUG, muteStackTrace=muteStackTrace, newLine=newLine, exception=exception)

def warning(origin, message, exception=None, muteStackTrace=False, newLine=False) :
    LogHelperHelper.softLog(origin, message, WARNING, muteStackTrace=muteStackTrace, newLine=newLine, exception=exception)

def wraper(origin, message, exception, muteStackTrace=False, newLine=False) :
    LogHelperHelper.hardLog(origin, message, exception, WRAPPER, muteStackTrace=muteStackTrace, newLine=newLine)

def failure(origin, message, exception, muteStackTrace=False, newLine=False) :
    LogHelperHelper.hardLog(origin, message, exception, FAILURE, muteStackTrace=muteStackTrace, newLine=newLine)

def error(origin, message, exception, muteStackTrace=False, newLine=False) :
    LogHelperHelper.hardLog(origin, message, exception, ERROR, muteStackTrace=muteStackTrace, newLine=newLine)

def test(origin, message, exception=None, muteStackTrace=False, newLine=False) :
    LogHelperHelper.softLog(origin, message, TEST, muteStackTrace=muteStackTrace, newLine=newLine, exception=exception)

def printLog(message, level=LOG, condition=False, muteStackTrace=False, newLine=True, margin=True, exception=None) :
    LogHelperHelper.printMessageLog(level, message, condition=condition, muteStackTrace=muteStackTrace, newLine=newLine, margin=margin, exception=exception)

def printInfo(message, condition=False, newLine=True, margin=True) :
    LogHelperHelper.printMessageLog(INFO, message, condition=condition, muteStackTrace=True, newLine=newLine, margin=margin)

def printStatus(message, condition=False, newLine=True, margin=True) :
    LogHelperHelper.printMessageLog(STATUS, message, condition=condition, muteStackTrace=True, newLine=newLine, margin=margin)

def printSuccess(message, condition=False, newLine=True, margin=True) :
    LogHelperHelper.printMessageLog(SUCCESS, message, condition=condition, muteStackTrace=True, newLine=newLine, margin=margin)

def printSetting(message, condition=False, muteStackTrace=False, newLine=True, margin=True) :
    LogHelperHelper.printMessageLog(SETTING, message, condition=condition, muteStackTrace=muteStackTrace, newLine=newLine, margin=margin)

def printDebug(message, condition=False, muteStackTrace=False, newLine=True, margin=True, exception=None) :
    LogHelperHelper.printMessageLog(DEBUG, message, condition=condition, muteStackTrace=muteStackTrace, newLine=newLine, margin=margin, exception=exception)

def printWarning(message, condition=False, muteStackTrace=False, newLine=True, margin=True, exception=None) :
    LogHelperHelper.printMessageLog(WARNING, message, condition=condition, muteStackTrace=muteStackTrace, newLine=newLine, margin=margin, exception=exception)

def printWarper(message, condition=False, muteStackTrace=False, newLine=True, margin=True, exception=None) :
    LogHelperHelper.printMessageLog(WRAPPER, message, condition=condition, muteStackTrace=muteStackTrace, newLine=newLine, margin=margin, exception=exception)

def printFailure(message, condition=False, muteStackTrace=False, newLine=True, margin=True, exception=None) :
    LogHelperHelper.printMessageLog(FAILURE, message, condition=condition, muteStackTrace=muteStackTrace, newLine=newLine, margin=margin, exception=exception)

def printError(message, condition=False, muteStackTrace=False, newLine=True, margin=True, exception=None) :
    LogHelperHelper.printMessageLog(ERROR, message, condition=condition, muteStackTrace=muteStackTrace, newLine=newLine, margin=margin, exception=exception)

def printTest(message, condition=False, muteStackTrace=False, newLine=True, margin=True, exception=None) :
    LogHelperHelper.printMessageLog(TEST, message, condition=condition, muteStackTrace=muteStackTrace, newLine=newLine, margin=margin, exception=exception)

def prettyPython(
        origin,
        message,
        dictionaryInstance,
        quote = c.SINGLE_QUOTE,
        tabCount = 0,
        nullValue = c.NONE,
        trueValue = c.TRUE,
        falseValue = c.FALSE,
        logLevel = LOG,
        condition = True
    ) :
    if condition :
        stdout, stderr = EnvironmentHelper.getCurrentSoutStatus()
        prettyPythonValue = StringHelper.prettyPython(
            dictionaryInstance,
            quote = quote,
            tabCount = tabCount,
            nullValue = nullValue,
            trueValue = trueValue,
            falseValue = falseValue,
            withColors = logsWithColorsEnabled(),
            joinAtReturn = False
        )
        LogHelperHelper.softLog(origin, StringHelper.join([message, c.COLON_SPACE, *prettyPythonValue]), logLevel)
        EnvironmentHelper.overrideSoutStatus(stdout, stderr)

def prettyJson(
        origin,
        message,
        dictionaryInstance,
        quote = c.DOUBLE_QUOTE,
        tabCount = 0,
        nullValue = c.NULL_VALUE,
        trueValue = c.TRUE_VALUE,
        falseValue = c.FALSE_VALUE,
        logLevel = LOG,
        condition = True
    ) :
    if condition :
        stdout, stderr = EnvironmentHelper.getCurrentSoutStatus()
        prettyJsonValue = StringHelper.prettyJson(
            dictionaryInstance,
            quote = quote,
            tabCount = tabCount,
            nullValue = nullValue,
            trueValue = trueValue,
            falseValue = falseValue,
            withColors = logsWithColorsEnabled(),
            joinAtReturn = False
        )
        LogHelperHelper.softLog(origin, StringHelper.join([message, c.COLON_SPACE, *prettyJsonValue]), logLevel)
        EnvironmentHelper.overrideSoutStatus(stdout, stderr)

def getExceptionMessage(exception) :
    if ObjectHelper.isEmpty(exception) :
        return c.UNKNOWN
    exceptionAsString = str(exception)
    if c.BLANK == exceptionAsString :
        return ReflectionHelper.getName(exception.__class__)
    else :
        return exceptionAsString

def getTracebackMessage(muteStackTrace) :
    tracebackMessage = c.BLANK
    try :
        tracebackMessage = traceback.format_exc()
    except :
        tracebackMessage = f'{c.NEW_LINE}'
    if muteStackTrace :
        return StringHelper.join(tracebackMessage.split(c.NEW_LINE)[-2:], character=c.NEW_LINE)
    return LogHelperHelper.NO_TRACEBACK_PRESENT_MESSAGE if LogHelperHelper.NO_TRACEBACK_PRESENT == str(tracebackMessage) else tracebackMessage
