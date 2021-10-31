from bs4 import BeautifulSoup as BS
import lxml, os, time, requests, copy

class SSInfo:
    
    def __init__(self, f_url, f_page, f_item, f_attr):
        self.f_url, self.f_page, self.f_item, self.f_attr = \
            f_url, f_page, copy.deepcopy(f_item), copy.deepcopy(f_attr)
            
    def help():
        print("SSInfo.help(): (self, f_url, f_page, f_item, f_attr)", end = '\n\n')
        
class SSFormat:
    
    def __init__(self, element_type, search_type = None, search_clue = None, multiple = False, format = None, extract = None):
        
        self.ssFormat = { 'element_type' : element_type, 'search_type' : search_type, 'search_clue' : search_clue, 
                          'multiple' : multiple, 'format' : format, 'extract' : extract }
    
    def __getitem__(self, key):
        
        return self.ssFormat[key]
    
    def alter(self, **kwargs):
        
        for key, val in kwargs.items():
            
            self.ssFormat[key] = copy.deepcopy(val)
    
    def help():
        print("SSFormat.help(): (self, element_type, search_type = None, search_clue = None, \n\tmultiple = False, format = None, extract = None)", end = '\n\n')

class StaticScraper:
    
    def __init__(self, webinfo, filename = None, timesleep = 0, buffer = 100):
        
        self.webinfo, self.filename, self.timesleep, self.buffer = copy.deepcopy(webinfo), filename, timesleep, buffer
    
    def help():
        print("StaticScraper.help(): ")
        print("[1] (self, webinfo, filename = None, buffer = 100)")
        print("[2] self.scrape_webpages(self, start = 1, pages = 1)")
        print("[3] self.filter_by_threshold(self, thresh_index, thresh_function, \n\tinputname = None, outputname = None)")
        print("[4] self.collapse_columns(self, column_indices, inputname = None, outputname = None)", end = '\n\n')
    
    def __save_record(self, filename = None, start_empty = False):
        
        filename = (filename if (filename != None) else self.filename)
        
        if (filename == None):
            
            return None

        if (start_empty):
        
            self.__erase_file(filename)
        
        with open(filename, 'a', encoding = 'UTF-8') as FILE:
            
            for scraped in self.scrapeList:
                
                FILE.write(str(scraped) + '\n')
    
    def __erase_file(self, filename):
        
        with open(filename, 'w', encoding = 'UTF-8') as FILE:
        
            FILE.write('')
    
    def __buffer_exceeded(self):
        
        return (len(self.scrapeList) == self.buffer)
    
    def __scrape_webpage(self, webpage):
        
        self.scrapeList = []
        
        itemList = self.__custom_find(
            BS(requests.get(webpage).text, 'lxml'),
            self.webinfo.f_item
        )
        
        for item in itemList:
            
            self.scrapeList.append( [ self.__custom_find(item, attr) for attr in self.webinfo.f_attr ] )
            
            if (self.__buffer_exceeded()):
                
                self.__save_record()
        
                self.scrapeList = []
        
        if (len(self.scrapeList)):
            
            self.__save_record()
            
            self.scrapeList = []
    
    def __prompt_overwrite(self, filename):
        
        if ((filename != None) and (os.path.isfile(filename))):
            
            print("File already exists, overwrite?")
            
            userInput = input("> (y/n)").lower()
            
            if ('y' in userInput):
                
                print("Will overwite the destination file.", end = '\n\n')
            
                self.__erase_file(filename)
            
            elif ('n' in userInput):
            
                print("Will write to end of file, errors may occur.", end = '\n\n')
            
            else:
                
                print("Cancelling procedure.", end = '\n\n')
        
                return None
        
        return 0
    
    def scrape_webpages(self, start = 1, pages = 1):
        
        if (self.__prompt_overwrite(self.filename) == None):
          
            return None
        
        for page in range(start, start + pages):
            
            print("Scraping page {} of {} pages.".format(page, start + pages - 1))
            
            self.__scrape_webpage(self.webinfo.f_url + self.webinfo.f_page.format(page))
            
            print("\tScraped page {} of {} pages.".format(page, start + pages - 1), end = '\n\n')
            
            time.sleep(self.timesleep)
    
    def __custom_find(self, source, format_info):
        
        result = (source.find_all if format_info['multiple'] else source.find)
        
        result = result(format_info['element_type'], **({} if (format_info['search_type'] == None) else ({format_info['search_type'] : format_info['search_clue']})))
        
        result = (result if (format_info['extract'] == None) else (result.text) if (format_info['extract'] == 'text') else (result[format_info['extract']]))
        
        return (result if (format_info['format'] == None) else (format_info['format'](result)))
    
    def filter_by_threshold(self, thresh_index, thresh_function, inputname = None, outputname = None):
        
        file_name = (inputname if (inputname != None) else self.filename)
        
        if (self.__prompt_overwrite(outputname) == None):
            
            return None
        
        if (os.path.isfile(file_name)):
            
            try:
                
                print("Filtering by threshold from {}.".format(file_name))
                
                FILE = open(file_name, 'r', encoding = 'UTF-8')
                
                DATA = FILE.read().splitlines()
                
                FILE.close()
                
                self.scrapeList = []
                
                for data in DATA:
                    
                    data = eval(data)
                    
                    if (thresh_function(data[thresh_index])):
                        
                        self.scrapeList.append(data)
                    
                    if ((outputname != None) and (self.__buffer_exceeded())):
                        
                        self.__save_record(filename = outputname)
                        
                        self.scrapeList = []
                
                if (len(self.scrapeList)):
                    
                    self.__save_record(filename = outputname, start_empty = (outputname == None))
                    
                    self.scrapeList = []
                
                print("\tFiltered by threshold from {}.".format(file_name), end = '\n\n')
            
            except Exception as exr:
                
                print("\tError: {}".format(exr), end = '\n\n')
        
        else:
            
            print("Error: Could not open {}".format(file_name), end = '\n\n')
    
    def __extract(self, source, column_indices):
        
        return (source if (len(column_indices) > 1) else source[0])
    
    def collapse_columns(self, column_indices, inputname = None, outputname = None):
        
        file_name = (inputname if (inputname != None) else self.filename)
        
        if (self.__prompt_overwrite(outputname) == None):
            
            return None
        
        if (os.path.isfile(file_name)):
            
            try:
                
                print("Collapsing columns from {}.".format(file_name))
                
                FILE = open(file_name, 'r', encoding = 'UTF-8')
                
                DATA = FILE.read().splitlines()
                
                FILE.close()
                
                self.scrapeList = []
                
                for data in DATA:
                    
                    self.scrapeList.append(self.__extract([ x for index, x in enumerate(eval(data)) if index in column_indices ], column_indices))
                    
                    if ((outputname != None) and (self.__buffer_exceeded())):
                        
                        self.__save_record(filename = outputname)
                        
                        self.scrapeList = []
                        
                if (len(self.scrapeList)):
                    
                    self.__save_record(filename = outputname, start_empty = (outputname == None))
                    
                    self.scrapeList = []
                    
                print("\tCollapsed columns from {}.".format(file_name), end = '\n\n')
            
            except Exception as exr:
                
                print("\tError: {}".format(exr), end = '\n\n')
        
        else:
            
            print("Error: Could not open {}".format(file_name), end = '\n\n')
