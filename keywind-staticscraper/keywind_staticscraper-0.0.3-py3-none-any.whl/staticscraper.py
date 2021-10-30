from bs4 import BeautifulSoup
from datetime import datetime
import lxml, time, requests, copy
class StaticScraper:
    def make_string(string):
        return None if string == None else "'" + string + "'"
    def _attribute_format(element_type, search_by = None, identifier = None, formatting = '', find = ''):
        return { 'et' : StaticScraper.make_string(element_type), 'fi' : find, 'sb' : search_by, 'id' : StaticScraper.make_string(identifier), 'fm' : formatting }
    def print_help():
        print("[1] Use StaticScraper._attribute_format(element_type, search_by = None, identifier = None, formatting = '', find = '')")
        print("\tVar = StaticScraper._attribute_format('div', 'class_', 'row-2-col-3', formatting = '.text'")
        print("\tVar = StaticScraper._attribute_format('div', 'class_', 'row-2-col-3', find = '_all'", end = '\n\n')
        print("[2] Use StaticScraper(website, pageformat, itemformat, attribute_list, sleeptime = 5, filename = None)")
        print("\tVar = StaticScraper('http://keywind.com/videos/', 'page-{}.html', \n\t\t'StaticScraper._attribute_format( ... )', \n\t\t\"['StaticScraper._attribute_format( ... )']\", 2, './test.txt')", end = '\n\n')
        print("[3] Use Var.scrape_website(start = 1, pages = 15)")
    def __init__(self, website, pageformat, itemformat, attribute_list, sleeptime = 5, filename = None):
        self.itemsearch = "BeautifulSoup(requests.get({0}).text, 'lxml').find{1}({2}, {3} = {4}){5}"
        self.sitemsearch = "BeautifulSoup(requests.get({0}).text, 'lxml').find{1}({2}){3}"
        self.attrsearch = "{0}.find{1}({2}, {3} = {4}){5}"
        self.sattrsearch = "{0}.find{1}({2}){3}"
        #
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
            itemList = (eval(self.sitemsearch.format('"' + self.website + self.pageformat.format(page) + '"', self.itemformat['fi'], self.itemformat['et'], self.itemformat['fm'])) \
                if (self.itemformat['sb'] == None) \
                else eval(self.itemsearch.format('"' + self.website + self.pageformat.format(page) + '"', self.itemformat['fi'], self.itemformat['et'], self.itemformat['sb'], self.itemformat['id'], self.itemformat['fm'])))
            self.pageInfo = []
            for item in itemList:
                itemData = dict.fromkeys(range(0, len(self.attribute_list), 1))
                for index, attribute in enumerate(self.attribute_list):
                    temp = (eval(self.sattrsearch.format('item', attribute['fi'], attribute['et'], attribute['fm'])) \
                        if (attribute['sb'] == None) \
                        else eval(self.attrsearch.format('item', attribute['fi'], attribute['et'], attribute['sb'], attribute['id'], attribute['fm'])))
                    itemData[index] = temp
                self.pageInfo.append(itemData)
            self.save_to_file()
            time.sleep(self.sleeptime)
#StaticScraper.print_help()
"""
website = "http://books.toscrape.com/catalogue/"
pageformat = "page-{0}.html"
itemformat = StaticScraper._attribute_format("li", 'class_', "col-xs-6 col-sm-4 col-md-3 col-lg-3", find = '_all')
AF = StaticScraper._attribute_format
attribute_list = [ AF("p", 'class_', "price_color", formatting = '.text'), 
                   AF("a", formatting = '["href"]') ]
SS = StaticScraper(website, pageformat, itemformat, attribute_list, sleeptime = 2, filename = 'pasdf.txt')
SS.scrape_website()
"""