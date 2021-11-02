import os,json,shutil
class Colors: fail = '\033[91m' ; good = '\033[92m' ; end = '\033[0m'
class JsonFiles:
    def __init__(self,fileName:str,defaultData:str='list'):
        self.modulePath = os.path.dirname(__file__)+'/'
        self.thisDir = f'{self.modulePath}json/'
        self.fileName = fileName.strip()
        self.jsonPath = f'{self.thisDir+fileName}.json'
        self.jsonData = False
        # create json folder if not exists
        if not os.path.isdir(self.thisDir): os.mkdir(self.thisDir)
        # create this json file if not exists
        if not os.path.exists(self.jsonPath):
            # check if default data type is list or dictionary
            if defaultData not in ['list','dict']:
                print(f'{Colors.fail}Only list or dict defaultData accepted{Colors.end}')
                return False
            if defaultData == 'list': open(self.jsonPath,'w').write('[]')
            else: open(self.jsonPath,'w').write('{}')

    def read(self):
        if os.path.exists(self.jsonPath):
            jsonData = json.loads(open(self.jsonPath,'r').read())
            self.jsonData = jsonData ; return jsonData
        else: print(f'{Colors.fail} The json object {self.fileName} do not exists{Colors.end}') ; return False

    def drop(self):
        if os.path.exists(self.jsonPath): os.remove(self.jsonPath) ; return True
        else: print(f'{Colors.fail} The json object {self.fileName} do not exists{Colors.end}') ; return False

    def update(self):
        if self.jsonData: open(self.jsonPath,'w').write(json.dumps(self.jsonData,indent=4)) ; return True
        else: print(f'{Colors.fail} Use .read() to read the json data before you can update it.{Colors.end}') ; return False

    def export(self,dirPath:str):
        if os.path.isdir(dirPath):
            print(f'{Colors.fail}Path > {dirPath} < exists, deleted it or choose another one.{Colors.end}') ; return False
        shutil.copytree(self.thisDir,dirPath) ; return True

    def Import(self,dirPath:str,overWrite=False):
        if not os.path.isdir(dirPath):
            print(f'{Colors.fail}Given path > {dirPath} < do not exists.{Colors.end}') ; return False
        # import
        files = os.listdir(dirPath)
        for file in files:
            filePath = dirPath+file
            newFilePath = self.thisDir+file
            if overWrite: shutil.copy(filePath,newFilePath) ; return True
            # check if json file exists
            if os.path.exists(newFilePath):
                print(f'{Colors.fail}json file > {file} < exists.{Colors.end}') ; return False
    
    def fileList(self): return os.listdir(self.thisDir)

    def reset(self): 
        # this will delete all json objects
        answer = input('All the json objects will be deleted ok/no?').strip().lower()
        if answer == 'ok' or answer == 'yes':
            for obj in os.listdir(self.thisDir): os.remove(self.thisDir+obj)
        print(f'{Colors.good}All data were deleted{Colors.end}') ; return True