from bs4 import BeautifulSoup
import lxml, os, copy, pandas, time, datetime, requests
class SSFormat:
    
    class __Dict:
        
        def __init__(self):
            
            self.formatList = {
                "element_type" : [ None, str ],
                "search_type" : [ None, str ],
                "search_clue" : [ None, str ],
                "multiple" : [ False, bool ],
                "extract" : [ None, str ],
                "format" : [ None, any ],
                "nickname" : [ None, str ],
                "filter" : [ None, any ],
                "keep" : [ True, bool ]
            }
            
        def get(self, key):
            
            if (key in self.formatList):
                
                return self.formatList[key][0]
            
            else:
                
                print(f"Warning [SSFormat]: cannot fetch value with key {key}.\n")
        
        def alter(self, key, newVal):
            
            if ((key in self.formatList) and ((self.formatList[key][1] == any) or (type(newVal) == self.formatList[key][1]))):
                
                self.formatList[key][0] = newVal
                
            else:
                
                print(f"Warning [SSFormat]: cannot update {key} with {newVal}.\n")
    
    def help():
        
        print("SSInfo(): ")
        
        print("\t__init__(self, element_type, search_type = None, search_clue = None, multiple = False, extract = None, format = None, nickname = None, filter = None, keep = True)\n")
        
    def __parse_arguments(self, ** kwargs):
        
        for key, val in kwargs.items():
            
            self.dataList.alter(key, val)
            
    def __init__(self, element_type, ** kwargs):
        
        self.dataList = self.__Dict()
        
        self.dataList.alter("element_type", element_type)
        
        self.__parse_arguments(**kwargs)
    
    def __getitem__(self, key):
        
        return self.dataList.get(key)
    
class SSInfo:
    
    def help():
        
        print("SSInfo(): __init__(self, f_site, f_page, f_item, f_attr)\n")
    
    def __init__(self, f_site, f_page, f_item, f_attr):
        
        self.infoList = {
            "f_site" : f_site,
            "f_page" : f_page,
            "f_item" : copy.deepcopy(f_item),
            "f_attr" : copy.deepcopy(f_attr)
        }
            
    def __getitem__(self, key):
        
        if (key in self.infoList):
            
            return self.infoList[key]
        
        else:
            
            print("Warning [SSInfo]: cannot fetch value with key {key}.\n")
    
class SSData:
    
    def help():
        
        print("SSData(): ")
        
        print("\t[1] __init__(self, info, buffer = 100, timesleep = 0, filename = None)")
        
        print("\t[2] empty_data(self)")
        
        print("\t[3] buffer_exceeded(self)")
        
        print("\t[4] add_data(self, newData)")
        
        print("\t[5] save_data(self, start = False)\n")
    
    def __init__(self, info, buffer = 100, timesleep = 0, filename = None):
        
        self.info, self.buffer, self.filename = copy.deepcopy(info), buffer, self.__validate_name(filename)
        
        self.data, self.columns, self.tempname = self.empty_data(), self.__find_columns(), datetime.datetime.now().strftime("sstemp_%y%m%d%H%M%S.csv")
        
        self.timesleep = timesleep
    
    def __validate_name(self, name):
        
        if (type(name) != str):
            
            print(f"Warning [SSData]: {name} is not a string, using a random name.\n")
            
            return datetime.datetime.now().strftime("ssdata_%y%m%d%H%M%S.csv")
        
        elif ((len(name) >= 5) and (name[-4:] == ".csv")):
            
            return name
        
        else:
            
            print(f"Warning [SSData]: {name} is not a csv file, altering the file extension.\n")
            
            return name + ".csv"
            
    def empty_data(self):
        
        self.data = []
        
        return []
    
    def __find_columns(self):
        
        columns = []
        
        for index, attr in enumerate(self.info["f_attr"]):
            
            nickname = attr["nickname"]
            
            columns.append(nickname if (nickname != None) else index)
            
        return columns
    
    def buffer_exceeded(self):
        
        return (len(self.data) >= self.buffer)
    
    def add_data(self, newData):
        
        self.data += newData
    
    def __save_data(self):
        
        with open(self.filename, "a", encoding = "UTF-8") as WFILE:
            
            with open(self.tempname, "r", encoding = "UTF-8") as RFILE:
                
                WFILE.write(RFILE.read())
                
        os.remove(self.tempname)
    
    def __get_key(self, attrIndex):
    
        return self.columns[attrIndex]
        
    def __collapse_filter(self, data):
        
        for index in range(len(data) - 1, -1, -1):
            
            keep = True
            
            for _index, attr in enumerate(self.info["f_attr"]):
                
                if (self.info["f_attr"][_index]["filter"] != None):
                
                    if not (attr["filter"])(data[self.__get_key(_index)][index]):
                        
                        keep = False
                
            if not (keep):
                
                data = data.drop(index)
                
        for index in range(len(self.info["f_attr"]) - 1, -1, -1):
            
            if not (self.info["f_attr"][index]["keep"]):
            
                column = self.__get_key(index)
                
                data.pop(column)
            
        return data
    
    def save_data(self, start = False):
        
        self.__collapse_filter(pandas.DataFrame(self.data, columns = self.columns)).to_csv(
            self.tempname, 
            index = False, 
            header = start
        )
        
        self.__save_data()
    
class StaticScraper:
    
    def help():
        
        print("StaticScraper(): ")
        
        print("\t [1]__init__(self, info)")
        
        print("\t [2]scrape(self, start = 1, pages = 1)\n")
    
    def __init__(self, info):
        
        self.info = copy.deepcopy(info)
        
        self.f_page = self.__format_webpage()
    
    def __format_webpage(self):
        
        site, page = self.info.info["f_site"], self.info.info["f_page"]
        
        A, B = site[-1] == "/", page[0] == "/"
        
        if (A and B):
            
            return site[:-1] + page
        
        elif (A or B):
            
            return site + page
        
        else:
        
            return site + "/" + page
    
    def __find_attributes(self, source, attr):
        
        data = source.find_all if (attr["multiple"]) else source.find
        
        data = data(
            attr["element_type"],
            ** (
                {} if ((attr["search_type"] == None) or (attr["search_clue"] == None)) else { attr["search_type"] : attr["search_clue"] }
            )
        )
        
        data = (
            data if (type(attr["extract"]) != str)
            else data.text if (attr["extract"] == "text")
            else data[attr["extract"]]
        )
        
        if (attr["format"] != None):
            
            data = attr["format"](data)
            
        return data
    
    def __scrape_webpage(self, page):
        
        webpage = self.f_page.format(page)
        
        data = BeautifulSoup(requests.get(webpage).text, "lxml")
        
        itemList = self.__find_attributes(data, self.info.info["f_item"])
        
        scraped = []
        
        for item in itemList:
            
            attrList = []
            
            for attr in self.info.info["f_attr"]:
                
                attrList.append(self.__find_attributes(item, attr))
                
            scraped.append(attrList)
            
        time.sleep(self.info.timesleep)
        
        return scraped
        
    def scrape(self, start = 1, pages = 1):
        
        start = True
        
        print(f"Scraping {self.info.info['f_site']}")
        
        for page in range(start, start + pages):
            
            progress = page - start + 1
            
            print(f"\tScraping page {page} ({progress}/{pages})")
            
            self.info.add_data(self.__scrape_webpage(page))
            
            if (self.info.buffer_exceeded()):
                
                self.info.save_data(start)
                
                self.info.empty_data()
                
                start = False
            
            print(f"\t\tScraped page {page} ({progress}/{pages})\n")
            
        if (len(self.info.data)):
            
            self.info.save_data(start)
            
            self.info.empty_data()
"""
def format_price(price):
    return eval(''.join([ x for x in price if x.isnumeric() or x == '.']))
def filter_price(price):
    return (price <= 40)
website = "http://books.toscrape.com/catalogue/"
pageformat = "page-{}.html"
itemformat = SSFormat(
    element_type = "li", search_type = "class_", search_clue = "col-xs-6 col-sm-4 col-md-3 col-lg-3", multiple = True
)
attrList = [
    SSFormat(element_type = "p", search_type = "class_", search_clue = "price_color", extract = "text", nickname = "price", format = format_price, filter = filter_price, keep = False),
    SSFormat(element_type = "a", extract = "href", nickname = "url")
]
info = SSInfo(website, pageformat, itemformat, attrList)
data = SSData(info, timesleep = 2)
scraper = StaticScraper(data)
scraper.scrape(start = 1, pages = 5)
"""