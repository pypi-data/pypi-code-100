import jieba

__RAW_CN__ = ['我操', 'wc',   #No Fuck
              '你妈死了', 'NMSL', ' NM$L', 'nmzl', 'nm$l',  #Mother
              '傻逼', '伞兵', '申必', '啥b', 'sb', '杀币', '煞笔'  #idiot
              'nt', '脑瘫',   #nt
              'esu', '恶俗', '户籍', '身份证号',    #esu
              '尸体', '死人']   #dead

__RAW_EN__ = ['fuck', 'fk',     #fuck
              'idiot',  #idiot
              'sexy',   #yel
              'your mother dead']   #dead

__URL_BANNED__ = ['https://', 'http://', 'ftp://',  #qz
                  '.com', '.top', '.io',    #domain
                  '.cn', '.jp', '.us',  #country
                  '.icu', '.earth'] #other

__URL_ALLOW__ = ['baidu.com', '360.com', 'google.com', 'bing.com', 'shodan.io',     #Searcher
                 'minecraft.net', 'steampowered.com',   #Game
                 'microsoft.com', 'windows.com']    #Company

__URL_BAN__ = ['taobao.com', 'sb666.com']

__ERROR__ = ['Err0: Invalid Mode',
             'Err1: Invalid word list']

def text_check(text:str, mode:int):
    if mode == 1:
        split = jieba.lcut_for_search(text)
        for s in range(len(split)):
            for cn in range(len(__RAW_CN__)):
                if split[s] == __RAW_CN__[cn]:
                    return True
                else:
                    return False
    elif mode == 2:
        for en in range(len(__RAW_EN__)):
            if __RAW_EN__[en] in text:
                return True
            else:
                return False
    else:
        return __ERROR__[0]
    pass

def text_check_self(text:str, raws:list):
    if not isinstance(raws, list):
        return __ERROR__[1]

    rlist = str(raws)
    for raw in range(len(rlist)):
        if rlist[raw] in text:
            return True
        else:
            return False

def check_url(text:str, bypass:bool=True):
    if bypass:
        for a in range(len(__URL_ALLOW__)):
            if __URL_ALLOW__[a] in text:
                return False

    for banned in range(len(__URL_BANNED__)):
        if __URL_BANNED__[banned] in text:
            return True

def check_url_banned(text:str):
    for x in range(len(__URL_BAN__)):
        if __URL_BAN__[x] in text:
            return True

    return False
    pass


if __name__ == '__main__':
    print(check_url('You baidu.com'))