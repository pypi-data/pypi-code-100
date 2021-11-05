import os
from os import path
from LibHanger.Library.uwConfig import cmnConfig
from LibHanger.Library.uwGetter import getPlatform
from LibHanger.Library.uwGlobals import *

class mercariConfig(cmnConfig):

    class structScrapingType:
        
        """
        スクレイピング方法
        """ 
        
        def __init__(self):

            """ 
            コンストラクタ
            """

            self.selenium = 1
            """ for selenium""" 

            self.beutifulSoup = 2
            """ for beutifulSoup""" 
    
    """
    mercarizer共通設定クラス(mercariConfig)
    """ 

    def __init__(self):
        
        """ 
        コンストラクタ
        """ 
        
        # スクレイピング方法インスタンス
        self.scrapingType = self.structScrapingType()

        # 基底側のコンストラクタ呼び出し
        super().__init__()
        
        self.UserEgent_Mozilla = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        """ ユーザーエージェント Mozilla """

        self.UserEgent_AppleWebKit = 'AppleWebKit/537.36 (KHTML, like Gecko)'
        """ ユーザーエージェント AppleWebKit """

        self.UserEgent_Chrome = 'Chrome/94.0.4606.61 Safari/537.36'
        """ ユーザーエージェント Chrome """

        self.ScrapingType = self.scrapingType.selenium
        """ スクレイピング方法 """

        self.MercariUrl = 'https://jp.mercari.com/'
        """ メルカリURL """

        self.MercariUrlSearch = 'search?'
        """ メルカリURL Search Keyword"""

        self.DelayTime:int = 2
        """ 1ページ読み込むごとに発生する待機時間(秒) """

        self.ItemTagName = '.ItemGrid__ItemGridCell-sc-14pfel3-1'
        """ 商品タグCSSクラス名 """

        self.DelayWaitElement = 'div-eagle-search-1580185158495-0'
        """ DOMに発生するまで待機するエレメント """

        self.WebDriverTimeout:int = 10
        """ Webドライバーのタイムアウト時間(秒) """

        self.WebDriverPath = ''
        """ Webドライバーパス """

        self.WebDriverPathWin = ''
        """ Webドライバーパス(Windows) """

        self.WebDriverPathLinux = ''
        """ Webドライバーパス(Linux) """

        self.WebDriverPathMac = ''
        """ Webドライバーパス(Mac) """

    def getConfig(self, scriptPath:str, configFileDirName:str = ''):

        """ 
        設定ファイルを読み込む 
        
        Parameters
        ----------
        self : LibHanger.cmnConfig
            共通設定クラス
        scriptPath : string
            スクリプトファイルパス

        """

        # 基底側のiniファイル読込
        super().getConfig(scriptPath, configFileDirName)

        # ユーザーエージェント Mozilla
        super().setConfigValue('UserEgent_Mozilla',self.config_ini,'USER_EGENT','USEREGENT_MOZILLA',str)

        # ユーザーエージェント AppleWebKit
        super().setConfigValue('UserEgent_AppleWebKit',self.config_ini,'USER_EGENT','USEREGENT_APPLEWEBKIT',str)

        # ユーザーエージェント Chrome
        super().setConfigValue('UserEgent_Chrome',self.config_ini,'USER_EGENT','USEREGENT_CHROME',str)

        # スクレイピング方法
        super().setConfigValue('ScrapingType',self.config_ini,'SITE','SCRAPING_TYPE',int)

        # メルカリURL
        super().setConfigValue('MercariUrl',self.config_ini,'SITE','MERCARI_URL',str)

        # メルカリURL Search Keyword
        super().setConfigValue('MercariUrlSearch',self.config_ini,'SITE','MERCARI_URL_SEARCH',str)

        # 待機時間
        super().setConfigValue('DelayTime',self.config_ini,'SITE','DELAY_TIME',int)

        # BeutifulSoupで取得する商品タグ名
        super().setConfigValue('ItemTagName', self.config_ini,'SITE','ITEM_TAG_NAME',str)

        # DOMに発生するまで待機するエレメント
        super().setConfigValue('DelayWaitElement', self.config_ini,'SITE','DELAY_WAIT_ELEMENT',str)

        # Webドライバータイムアウト(秒)
        super().setConfigValue('WebDriverTimeout', self.config_ini,'SITE','WEBDRIVER_TIMEOUT',int)

        # WebDriverパス(Windows)
        super().setConfigValue('WebDriverPathWin', self.config_ini,'SITE','WEBDRIVER_PATH_WIN',str)

        # WebDriverパス(Linux)
        super().setConfigValue('WebDriverPathLinux', self.config_ini,'SITE','WEBDRIVER_PATH_LINUX',str)

        # WebDriverパス(Mac)
        super().setConfigValue('WebDriverPathMac', self.config_ini,'SITE','WEBDRIVER_PATH_MAC',str)

        # WebDriverパス
        self.WebDriverPath = self.getWebDriverPath(scriptPath)

    def getWebDriverPath(self, scriptPath):
        
        """ 
        Webドライバーパスを取得する
        
        Parameters
        ----------
        self : LibHanger.cmnConfig
            共通設定クラス
        scriptPath : string
            スクリプトファイルパス

        """

        if getPlatform() == gv.platForm.win:
            return os.path.join(path.dirname(scriptPath), self.WebDriverPathWin)
        elif getPlatform() == gv.platForm.linux:
            return os.path.join(path.dirname(scriptPath), self.WebDriverPathLinux)
        elif getPlatform() == gv.platForm.mac:
            return os.path.join(path.dirname(scriptPath), self.WebDriverPathMac)

