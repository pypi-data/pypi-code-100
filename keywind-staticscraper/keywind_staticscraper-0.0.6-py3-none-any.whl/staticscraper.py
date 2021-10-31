from bs4 import BeautifulSoup
from datetime import datetime
import lxml, time, requests, copy, os
class StaticScraper:
    def _attribute_format(element_type, search_by = None, identifier = None, formatting = None, find_all = False, function = None):
        return { 'et' : element_type, 'fi' : find_all, 'sb' : search_by, 'id' : identifier, 'fm' : formatting, 'fc' : function }
    def print_help():
        print("[1] Use StaticScraper._attribute_format(element_type, search_by = None, identifier = None, formatting = None, find_all = None, function = None)")
        print("\tVar = StaticScraper._attribute_format('div', 'class_', 'row-2-col-3', formatting = 'text')")
        print("\tVar = StaticScraper._attribute_format('div', 'class_', 'row-2-col-3', find_all = True, function = ~)", end = '\n\n')
        print("[2] Use StaticScraper(website, pageformat, itemformat, attribute_list, sleeptime = 0, filename = None)")
        print("\tVar = StaticScraper('http://keywind.com/videos/', 'page-{}.html', \n\t\t'StaticScraper._attribute_format( ... )', \n\t\t\"['StaticScraper._attribute_format( ... )']\", 2, './test.txt')", end = '\n\n')
        print("[3] Use Var.scrape_website(start = 1, pages = 15)")
    def __init__(self, website, pageformat, itemformat, attribute_list, sleeptime = 0, filename = None):
        self.website, self.pageformat = website, pageformat
        self.itemformat, self.attribute_list = copy.deepcopy(itemformat), copy.deepcopy(attribute_list)
        self.sleeptime, self.filename = sleeptime, filename
    def save_to_file(self):
        if (self.filename != None):
            with open(self.filename, 'a', encoding = 'UTF-8') as WF:
                for item in self.pageInfo:
                    WF.write(str(item) + '\n')
    def scrape_website(self, start = 1, pages = 1):
        for page in range(start, start + pages, 1):
            itemList = StaticScraper.custom_find(BeautifulSoup(requests.get(self.website + self.pageformat.format(page)).text, 'lxml'), 
                                                 self.itemformat['et'], self.itemformat['sb'], self.itemformat['id'], 
                                                 self.itemformat['fi'], self.itemformat['fm'], self.itemformat['fc'])
            self.pageInfo = []
            print("Scraping page {} of {} pages.".format(page, start + pages - 1), end = '\n\n')
            for item in itemList:
                itemData = dict.fromkeys(range(len(self.attribute_list)))
                for index, attribute in enumerate(self.attribute_list):
                    temp = StaticScraper.custom_find(item, attribute['et'], attribute['sb'], attribute['id'], attribute['fi'], attribute['fm'], attribute['fc'])
                    itemData[index] = temp
                self.pageInfo.append(itemData)
            self.save_to_file()
            time.sleep(self.sleeptime)
    def custom_find(source, element_type, search_by = None, identifier = None, find_all = False, formatting = None, function = None):
        result = (source.find_all if find_all else source.find)
        result = (result(element_type, **{search_by : identifier}) if search_by != None else result(element_type))
        result = (result if formatting == None else result.text if formatting == 'text' else result[formatting])
        return (result if function == None else function(result))
    def filter_file(self, a_index, function):
        if (os.path.isfile(self.filename)):
            file = open(self.filename, 'r', encoding = 'UTF-8')
            data = file.read().splitlines()
            file.close()
            self.erase_file()
            self.pageInfo = []
            counter = 0
            for datum in data:
                item = eval(datum)
                if (function(item[a_index])):
                    self.pageInfo.append(item)
                if (counter == 99):
                    self.save_to_file()
                    self.pageInfo = []
                counter = (counter + 1) % 100
            if (len(self.pageInfo)):
                self.save_to_file()
                self.pageInfo = []
    def erase_file(self):
        with open(self.filename, 'w', encoding = 'UTF-8') as FN:
            FN.write('')
    def filter_attributes(self, indexlist):
        if (os.path.isfile(self.filename)):
            file = open(self.filename, 'r', encoding = 'UTF-8')
            data = file.read().splitlines()
            file.close()
            counter = 0
            self.erase_file()
            self.pageInfo = []
            for datum in data:
                item = eval(datum)
                item = { key : val for key, val in item.items() if key in indexlist }
                self.pageInfo.append(item)
                if (counter == 99):
                    self.save_to_file()
                    self.pageInfo = []
                counter = (counter + 1) % 100
            if (len(self.pageInfo)):
                self.save_to_file()
                self.pageInfo = []
    def extract_attribute(self):
        if (os.path.isfile(self.filename)):
            file = open(self.filename, 'r', encoding = 'UTF-8')
            data = file.read().splitlines()
            file.close()
            counter = 0
            self.erase_file()
            self.pageInfo = []
            for datum in data:
                item = eval(datum)
                item = [ val for key, val in item.items() ][0]
                self.pageInfo.append(item)
                if (counter == 99):
                    self.save_to_file()
                    self.pageInfo = []
                counter = (counter + 1) % 100
            if (len(self.pageInfo)):
                self.save_to_file()
                self.pageInfo = []
#StaticScraper.print_help()
"""
def format_price(data):
    return eval(''.join([ x for x in data if x.isnumeric() or x == '.']))
def keep_item(data):
    return (data <= 60)
website = "http://books.toscrape.com/catalogue/"
pageformat = "page-{0}.html"
itemformat = StaticScraper._attribute_format('li', 'class_', "col-xs-6 col-sm-4 col-md-3 col-lg-3", find_all = True)
AF = StaticScraper._attribute_format
attribute_list = [ AF("p", 'class_', "price_color", formatting = 'text', function = format_price), 
                   AF("a", formatting = 'href') ]
SS = StaticScraper(website, pageformat, itemformat, attribute_list, sleeptime = 0, filename = 'pasdf.txt')
SS.erase_file()
SS.scrape_website()
SS.filter_file(0, keep_item)
SS.filter_attributes([0])
SS.extract_attribute()
"""