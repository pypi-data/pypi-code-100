import requests as r,json,os,time
from dateutil.relativedelta import relativedelta
from datetime import datetime


class Ydata:
    def __init__(self,symbol:str):
        self.symbol = symbol.upper()
        self.userAgent = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"}
        self.thisDir = os.path.dirname(__file__)
        # create cache dir if not exists
        if not os.path.exists(f'{self.thisDir}/cache/'): os.mkdir(f'{self.thisDir}/cache/')


    def currentPrice(self):
        url = f'https://finance.yahoo.com/quote/{self.symbol}/history?p={self.symbol}'
        content = r.get(url,headers=self.userAgent).text
        price = content.split('class="Trsdu(0.3s)')[1].split('</span>')[0].split('">')[1]
        return self.__getNumber(price)

    def historical(self,initialDate:str,endDate:str):
        cacheName = f'{initialDate}-{endDate}-{self.symbol}'
        # if cache exists return it and do not get new data from yahoo
        cache = self.__cache(cacheName)
        if cache: return cache
        period1 = int(time.mktime(datetime.strptime(initialDate,"%Y-%m-%d").timetuple()))
        period2 = int(time.mktime(datetime.strptime(endDate,"%Y-%m-%d").timetuple()))
        url = f'https://query1.finance.yahoo.com/v7/finance/download/{self.symbol}?period1={period1}&period2={period2}&interval=1d&events=history&includeAdjustedClose=true'
        content = r.get(url,headers=self.userAgent).text
        content = content.replace('''Date,Open,High,Low,Close,Adj Close,Volume\n''','')
        days = {}
        # add day price and information to days dictionary
        for line in content.splitlines():
            values = line.split(',')
            date = values[0]
            data = {
                'open':self.__getNumber(values[1]),
                'high':self.__getNumber(values[2]),
                'low':self.__getNumber(values[3]),
                'close':self.__getNumber(values[4]),
                'adjClose':self.__getNumber(values[5]),
                'volume':self.__getNumber(values[6])
            }
            days[date]=data
        # add and return cache
        newCache = self.__cache(cacheName,days)
        return newCache

    def oneWeek(self):
        nowDateTime = datetime.now()
        oneWeekAgo = nowDateTime-relativedelta(weeks=1)
        return self.historical(oneWeekAgo.strftime("%Y-%m-%d"),nowDateTime.strftime("%Y-%m-%d"))

    def twoWeeks(self):
        nowDateTime = datetime.now()
        oneWeekAgo = nowDateTime-relativedelta(weeks=2)
        return self.historical(oneWeekAgo.strftime("%Y-%m-%d"),nowDateTime.strftime("%Y-%m-%d"))

    def oneMonth(self):
        nowDateTime = datetime.now()
        oneMonthAgo = nowDateTime-relativedelta(months=1)
        return self.historical(oneMonthAgo.strftime("%Y-%m-%d"),nowDateTime.strftime("%Y-%m-%d"))
    
    def twoMonths(self):
        nowDateTime = datetime.now()
        oneMonthAgo = nowDateTime-relativedelta(months=2)
        return self.historical(oneMonthAgo.strftime("%Y-%m-%d"),nowDateTime.strftime("%Y-%m-%d"))

    def __cache(self,fileName:str,data=False):
        path = f'{self.thisDir}/cache/{fileName}.json'
        # if new data given write new cache
        if data: open(path,'w').write(json.dumps(data,indent=3))
        if os.path.exists(path): return json.loads(open(path,'r').read())
        else: return False
    
    def __getNumber(self,number:str):
        if '.' in number: return float(number)
        else: return int(number)