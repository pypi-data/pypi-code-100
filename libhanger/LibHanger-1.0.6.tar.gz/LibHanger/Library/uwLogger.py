import logging
import os
from .uwConfig import cmnConfig

def loggerDecorator(outputString):

    """
    関数の開始～終了でコンソールに文字列を出力するデコレーター
    """

    def _loggerDecorator(func):

        """
        関数の開始～終了でコンソールに文字列を出力するデコレーター
        """

        def  wrapper(*args):

            """
            デコレーターのラッパー
            """

            print('(' + outputString + ') ...', end = '')
            logging.info('(' + outputString + ') ...')
            try:
                ret = func(*args)
                print('OK')
                logging.info('OK')
            except Exception as e:
                errorInfo = 'NG\n'\
                            '=== エラー内容 ===\n'\
                            'type:' + str(type(e)) + '\n'\
                            'args:' + str(e.args) + '\n'\
                            'e自身:' + str(e)

                print(errorInfo)
                logging.error(errorInfo)
                return
            return ret

        return wrapper

    return _loggerDecorator

def setting(config: cmnConfig):

    """
    ロガー設定

    Parameters
    ----------
    config : cmnConfig
        共通設定クラス
    """

    # ログ出力先がない場合、作成する
    if os.path.exists(config.LogFolderName) == False:
        os.mkdir(config.LogFolderName)

    # ロガー設定
    logging.basicConfig(filename=os.path.join(config.LogFolderName, config.LogFileName),
                        level=config.LogLevel, 
                        format=config.LogFormat)
