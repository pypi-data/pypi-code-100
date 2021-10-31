from bs4 import BeautifulSoup
from datetime import datetime
import lxml, time, requests, copy
class StaticScraper:
    """
    def make_string(string):
        return None if string == None else "'" + string + "'"
    """
    def _attribute_format(element_type, search_by = None, identifier = None, formatting = None, find_all = False, function = None):
        return { 'et' : element_type, 'fi' : find_all, 'sb' : search_by, 'id' : identifier, 'fm' : formatting, 'fc' : function }
    def print_help():
        print("[1] Use StaticScraper._attribute_format(element_type, search_by = None, identifier = None, formatting = None, find_all = None, function = None)")
        print("\tVar = StaticScraper._attribute_format('div', 'class_', 'row-2-col-3', formatting = 'text'")
        print("\tVar = StaticScraper._attribute_format('div', 'class_', 'row-2-col-3', find_all = True, function = ~", end = '\n\n')
        print("[2] Use StaticScraper(website, pageformat, itemformat, attribute_list, sleeptime = 0, filename = None)")
        print("\tVar = StaticScraper('http://keywind.com/videos/', 'page-{}.html', \n\t\t'StaticScraper._attribute_format( ... )', \n\t\t\"['StaticScraper._attribute_format( ... )']\", 2, './test.txt')", end = '\n\n')
        print("[3] Use Var.scrape_website(start = 1, pages = 15)")
    def __init__(self, website, pageformat, itemformat, attribute_list, sleeptime = 0, filename = None):
        """
        self.itemsearch = "BeautifulSoup(requests.get({0}).text, 'lxml').find{1}({2}, {3} = {4}){5}"
        self.sitemsearch = "BeautifulSoup(requests.get({0}).text, 'lxml').find{1}({2}){3}"
        self.attrsearch = "{0}.find{1}({2}, {3} = {4}){5}"
        self.sattrsearch = "{0}.find{1}({2}){3}"
        """
        #
        self.website, self.pageformat = website, pageformat
        self.itemformat, self.attribute_list = copy.deepcopy(itemformat), copy.deepcopy(attribute_list)
        self.sleeptime, self.filename = sleeptime, filename
        #print(self.itemformat)
    def save_to_file(self):
        if (self.filename != None):
            with open(self.filename, 'a', encoding = 'UTF-8') as WF:
                for item in self.pageInfo:
                    WF.write(str(item) + '\n')
    def scrape_website(self, start = 1, pages = 1):
        for page in range(start, start + pages, 1):
            """
            itemList = (eval(self.sitemsearch.format('"' + self.website + self.pageformat.format(page) + '"', self.itemformat['fi'], self.itemformat['et'], self.itemformat['fm'])) \
                if (self.itemformat['sb'] == None) \
                else eval(self.itemsearch.format('"' + self.website + self.pageformat.format(page) + '"', self.itemformat['fi'], self.itemformat['et'], self.itemformat['sb'], self.itemformat['id'], self.itemformat['fm'])))
            """
            itemList = StaticScraper.custom_find(BeautifulSoup(requests.get(self.website + self.pageformat.format(page)).text, 'lxml'), 
                                                 self.itemformat['et'], self.itemformat['sb'], self.itemformat['id'], 
                                                 self.itemformat['fi'], self.itemformat['fm'], self.itemformat['fc'])
            #print(self.itemformat)
            #print(itemList)
            #print(self.website + self.pageformat.format(page))
            self.pageInfo = []
            for item in itemList:
                itemData = dict.fromkeys(range(len(self.attribute_list)))
                for index, attribute in enumerate(self.attribute_list):
                    """
                    temp = (eval(self.sattrsearch.format('item', attribute['fi'], attribute['et'], attribute['fm'])) \
                        if (attribute['sb'] == None) \
                        else eval(self.attrsearch.format('item', attribute['fi'], attribute['et'], attribute['sb'], attribute['id'], attribute['fm'])))
                    """
                    temp = StaticScraper.custom_find(item, attribute['et'], attribute['sb'], attribute['id'], attribute['fi'], attribute['fm'], attribute['fc'])
                    itemData[index] = temp
                self.pageInfo.append(itemData)
            self.save_to_file()
            time.sleep(self.sleeptime)
    def custom_find(source, element_type, search_by = None, identifier = None, find_all = False, formatting = None, function = None):
        #result = (source.find_all if find_all else source.find)(**{'name':element_type} if (search_by != None) else **{ 'name' : element_type, search_by : identifier })
        result = (source.find_all if find_all else source.find)
        result = (result(element_type, **{search_by : identifier}) if search_by != None else result(element_type))
        result = (result if formatting == None else result.text if formatting == 'text' else result[formatting])
        return (result if function == None else function(result))
#StaticScraper.print_help()
"""
website = "http://books.toscrape.com/catalogue/"
pageformat = "page-{0}.html"
itemformat = StaticScraper._attribute_format('li', 'class_', "col-xs-6 col-sm-4 col-md-3 col-lg-3", find_all = True)
AF = StaticScraper._attribute_format
attribute_list = [ AF("p", 'class_', "price_color", formatting = 'text'), 
                   AF("a", formatting = 'href') ]
SS = StaticScraper(website, pageformat, itemformat, attribute_list, sleeptime = 0, filename = 'pasdf.txt')
SS.scrape_website()
"""