
class globalValues:

    """
    オブジェクト共有クラス
    """

    def __init__(self):
        
        """
        コンストラクタ
        """

        self.config = None
        """ ログファイル名 """

# インスタンス生成(import時に実行される)
gv = globalValues()
