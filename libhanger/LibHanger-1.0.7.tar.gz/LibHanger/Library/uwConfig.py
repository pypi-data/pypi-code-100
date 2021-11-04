import configparser
import os
import pathlib
import logging
import traceback
from .uwException import * 

class cmnConfig:

    """
    共通設定クラス
    """ 

    def __init__(self):

        """
        コンストラクタ
        """

        self.LogFileName = 'default.log'
        """ ログファイル名 """

        self.LogFolderName = 'log'
        """ ログ出力先フォルダ名 """

        self.LogFormat = '%(levelname)s : %(asctime)s : %(message)s'
        """ ログフォーマット定義 """

        self.LogLevel:int = logging.DEBUG
        """ ログレベル """

        self.config_ini = None
        """ iniファイル読込内容 """

    def getConfig(self, scriptPath: str, configFileDirName: str = ''):

        """ 
        設定ファイルを読み込む 
        
        Parameters
        ----------
        self : LibHanger.cmnConfig
            共通設定クラス
        scriptPath : str
            スクリプトファイルパス
        configFileDirName : str
            config.iniがあるディレクトリ名
        
        """
        
        # configparser宣言
        config_ini = configparser.ConfigParser()

        # iniファイルパス取得
        iniDirPath = pathlib.Path(os.path.abspath(os.path.dirname(scriptPath)))
        iniFilePath = os.path.join(iniDirPath, configFileDirName, 'config.ini')

        # iniファイル存在確認
        if (not os.path.exists(iniFilePath)): 
            try:
                raise iniFilePathError
            except iniFilePathError as e:
                print(e)
                with open("log/error.log", 'a') as f:
                    traceback.print_exc(file=f)

        # iniファイル読込
        config_ini.read(iniFilePath, encoding='utf-8')

        # 各設定値をインスタンス変数にセット
        self.setConfigValue('LogFileName',config_ini,'DEFAULT','LOGFILE_NAME', str)
        self.setConfigValue('LogFolderName',config_ini,'DEFAULT','LOGFOLDER_NAME', str)
        self.setConfigValue('LogFormat',config_ini,'DEFAULT','LOGFORMAT', str)
        self.setConfigValue('LogLevel',config_ini,'DEFAULT','LOGLEVEL', int)
        
        # 読込内容をインスタンス変数に設定する
        self.config_ini = config_ini

    def setConfigValue(self, 
                       insVariableName: str, 
                       config_ini: list, 
                       section: str, 
                       key: str, 
                       dataType: type):
        
        """ 
        iniファイルから読み取った値をインスタンス変数セットする \n
        指定したセクション、キーが存在しない場合はインスタンス変数の元値を保持する
        
        Parameters
        ----------
        self : LibHanger.cmnConfig
            共通設定クラス
        insVariableName : str
            インスタンス変数名
        config_ini : list
            iniファイル読込内容List
        section : str
            iniファイルセクション名
        key : str
            iniファイルキー名
        dataType : type
            インスタンス変数のデータ型
        """

        if config_ini[section].get(key) != None:
            
            if dataType is str:
                setattr(self, insVariableName, config_ini[section][key])
            elif dataType is int:
                setattr(self, insVariableName, int(config_ini[section][key]))
            elif dataType is float:
                setattr(self, insVariableName, float(config_ini[section][key]))

