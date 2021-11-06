import requests, time, os, pandas, datetime, copy, random
class CRFormat:
    
    class __Dict:
        
        def __init__(self):
            
            self.dict = dict()
            
        def alter(self, key, value):
            
            if (type(key) != int):
                
                print(f"Warning [CRFormat]: key {key} is not an integer.\n")
            
            else:
            
                self.dict[key] = value
            
        def get(self, key):
            
            if (key in self.dict):
                
                return self.dict[key]
            
            else:
                
                print(f"Warning [CRFormat]: cannot fetch value with key {key}.\n")
    
    def help():
        
        print("CRFormat(): ")
        
        print("\t[1] __init__(self)")
        
        print("\t[2] alter(self, key, value)")
        
        print("\t[3] get(self, key)")
        
        print("\t[4] initialize(self)")
        
        print("\t[5] save_json(self, filename = None)")
        
        print("\t[6] load_json_file(self, filename)")
        
        print("\t[7] load_json_data(self, data)\n")
        
    def print_register(self, key = None):
        
        if (key == None):
            
            print(pandas.DataFrame(self.dict.dict, index = [0]))
            
        else:
            
            print(f"{key}: {self.dict.get(key)}.\n")
    
    def alter(self, key, value):
        
        self.dict.alter(key, value)
        
    def initialize(self):
        
        self.dict = self.__Dict()
    
    def get(self, key):
        
        return self.dict.get(key)
    
    def __init__(self):
        
        self.dict = self.__Dict()
    
    def __eval_key(self, key):
        
        if (type(key) == int):
            
            return key
        
        elif ((type(key) == str) and (key.isnumeric())):
            
            return eval(key)
        
        else:
            
            print(f"Warning [CRFormat]: cannot use {key} as key for it's non-numeric.\n")
    
    def __load_from(self, filename):
            
        dictionary = pandas.DataFrame(pandas.read_json(filename))
        
        for key, _ in dictionary.items():
            
            self.dict.alter(self.__eval_key(key), dictionary[key][0])
    
    def save_json(self, filename = None):
        
        if (type(filename) != str):
            
            print(f"Warning [CRFormat]: {filename} is not a string, using a random name.\n")
            
            filename = datetime.datetime.now().strftime("crdata_%y%m%d%H%M%S.json")
            
        elif (len(filename) >= 6):
            
            if (filename[-5:] != ".json"):
                
                print(f"Warning [CRFormat]: {filename} is not a json file, fixing extension.\n")
                
                filename += ".csv"
                
            elif (os.path.isfile(filename)):
                
                print(f"Warning [CRFormat]: {filename} already exists.\n")
                
                while True:
                    
                    userInput = input("Overwrite? (Y/N)> ").lower()
                    
                    if ("y" in userInput):
                        
                        break
                    
                    elif ("n" in userInput):
                        
                        print("Notice: generating a random name.\n")
                        
                        filename = datetime.datetime.now().strftime("crdata_%y%m%d%H%M%S.json")
                        
                        break
                    
                    else:
                        
                        print(f"Warning [CRFormat]: {userInput} is not explicit.\n")
                
        pandas.DataFrame(self.dict.dict, index = [0]).to_json(filename)
    
    def load_json_data(self, data):
        
        dictionary = pandas.DataFrame(data)
        
        for key, _ in dictionary.items():
            
            self.dict.alter(self.__eval_key(key), dictionary[key][0])
    
    def load_json_file(self, filename):
        
        if (type(filename) != str):
            
            print(f"Warning [CRFormat]: {filename} is not a string.\n")
            
        elif (len(filename) >= 6):
            
            if (filename[-5:] != ".json"):
                
                print(f"Warning [CRFormat]: {filename} is not a json file.\n")
                
            elif not (os.path.isfile(filename)):
                
                print(f"Warning [CRFormat]: {filename} does not exist.\n")
                
            else:
                
                self.__load_from(filename)
       
class CloudRegister:
    
    def help():
        
        print("CloudRegister(): ")
        
        print("\t[1] __init__(self, registerLink)")
        
        print("\t[2] fetch_register(self, key = None)\n")
    
    def __init__(self, registerLink):
        
        self.register = CRFormat()
        
        self.registerLink = registerLink
        
        self.tempname = self.__get_tempname()
        
    def __get_tempname(self):
        
        return datetime.datetime.now().strftime("crtemp_%y%m%d%H%M%S.json")
    
    def __validate_name(self, name):
        
        if (type(name) != str):
            
            print(f"Warning [CloudRegister]: {name} is not a string.\n")
            
        elif ((len(name) >= 6) and (name[-5:] == '.json')):
            
            return name
        
        else:
            
            print(f"Warning [CloudRegister]: {name} is not json file, fixing the extension.\n")
            
            return name + ".json"
        
    def __download_register(self):
        
        pulled = requests.get(self.registerLink).text
        
        with open(self.tempname, "w", encoding = "UTF-8") as WFILE:
            
            WFILE.write(pulled)
        
    def fetch_register(self):
            
        self.__download_register()
        
        self.register.load_json_file(self.tempname)
            
        os.remove(self.tempname)
        
        return copy.deepcopy(self.register)
            
class HumanEmulator:

    infinity, intertime = 1e6, 1e-2

    def help():
        
        print("HumanEmulator(): ")
        
        print("\t[1] __init__(self, minwait, maxwait)")
        
        print("\t[2] get(self) # get random number from [ minwait, maxwait ]")
        
        print("\t[3] sleep(self, showtime = False, inter = False) # display sleep time, use interruptive_sleep")
        
        print("\t[4] interruptive_sleep(timesleep) # allows keyboard interrupt\n")

    def __init__(self, minwait, maxwait):

        self.waitrange = [ *(self.__parse_wait(minwait, maxwait)) ]    
        
        #print(self.waitrange)
        
        self.random = random.Random(datetime.datetime.now())
        
    def __parse_wait(self, minwait, maxwait):
        
        minwait = minwait if (((type(minwait) == int) or (type(minwait) == float)) and (minwait >= 0)) else self.infinity
        
        maxwait = maxwait if (((type(maxwait) == int) or (type(maxwait) == float)) and (maxwait >= 0)) else self.infinity
        
        return min(minwait, maxwait), max(minwait, maxwait)
    
    def get(self):
        
        return self.random.randint(self.waitrange[0], self.waitrange[1])
    
    def interruptive_sleep(timesleep):
        
        SOT = datetime.datetime.now()
        
        while ((datetime.datetime.now() - SOT).total_seconds() < timesleep):
            
            time.sleep(HumanEmulator.intertime)
    
    def sleep(self, showtime = False, inter = False):
        
        timesleep = self.get()
        
        if (showtime):
            
            print(f"Sleeping for {timesleep} seconds.\n")
        
        if (inter):
            
            HumanEmulator.interruptive_sleep(timesleep)
            
        else:
            
            time.sleep(timesleep)
        
        return timesleep
