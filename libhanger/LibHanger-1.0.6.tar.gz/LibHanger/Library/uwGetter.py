import datetime

def getNow():

    """ 
    現在日時取得
    
    Parameters
    ----------
    none
    """

    # 日本時刻取得
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))) 

def addDays(targetDate, addDays: int):
    
    """ 
    対象日付の日数を加算する
    
    Parameters
    ----------
    targetDate :
        加算対象日付
    addDays : int
        加算する日数
    """

    # 戻り値を返す
    return targetDate + datetime.timedelta(days=addDays)
