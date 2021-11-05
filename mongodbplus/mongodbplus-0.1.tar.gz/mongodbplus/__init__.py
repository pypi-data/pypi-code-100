from pymongo import MongoClient
import json,os

class Colors: fail = '\033[91m' ; good = '\033[92m' ; end = '\033[0m'
class MongodbPlus:
    def __init__(self,databaseName:str):
        self.thisDir = os.path.dirname(__file__)+'/'
        self.databaseName=databaseName
        self.__mongoClient = MongoClient("mongodb://localhost:27017/")
        self.__mongoDb = self.__mongoClient[databaseName]
        self.__wasCollectionSet__ = False

    def setCollection(self,collectionName:str):
        self.collection = self.__mongoDb[collectionName]
        self.collectionName = collectionName
        self.__wasCollectionSet__ = True

    def showDatabases(self): return self.__mongoClient.list_database_names()

    def showCollections(self): return self.__mongoDb.list_collection_names()

    def count(self,filter:dict={},collectionName:str=''):
        # check if collection name was setted
        if collectionName: collectionName=collectionName
        elif self.__wasCollectionSet__: collectionName=self.collectionName
        else: self.__printCollectionNameError__() ; return False
        col = self.__mongoDb[collectionName]
        result = col.count_documents(filter)
        return result

    def deleteOne(self,filter:dict={},collectionName:str=''):
        # check if collection name was setted
        if collectionName: collectionName=collectionName
        elif self.__wasCollectionSet__: collectionName=self.collectionName
        else: self.__printCollectionNameError__() ; return False
        col = self.__mongoDb[collectionName]
        result = col.delete_one(filter)
        return result

    def deleteMany(self,filter:dict={},collectionName:str=''):
        # check if collection name was setted
        if collectionName: collectionName=collectionName
        elif self.__wasCollectionSet__: collectionName=self.collectionName
        else: self.__printCollectionNameError__() ; return False
        col = self.__mongoDb[collectionName]
        result = col.delete_many(filter)
        return result

    def findOne(self,filter:dict={},collectionName:str=''):
        # check if collection name was setted
        if collectionName: collectionName=collectionName
        elif self.__wasCollectionSet__: collectionName=self.collectionName
        else: self.__printCollectionNameError__() ; return False
        col = self.__mongoDb[collectionName]
        result = col.find_one(filter)
        return result

    def findMany(self,filter:dict={},collectionName:str=''):
        # check if collection name was setted
        if collectionName: collectionName=collectionName
        elif self.__wasCollectionSet__: collectionName=self.collectionName
        else: self.__printCollectionNameError__() ; return False
        col = self.__mongoDb[collectionName]
        result = col.find(filter)
        return result

    def updateOne(self,filter:dict={},newData:dict={},collectionName:str=''):
        # check if collection name was setted
        if collectionName: collectionName=collectionName
        elif self.__wasCollectionSet__: collectionName=self.collectionName
        else: self.__printCollectionNameError__() ; return False
        col = self.__mongoDb[collectionName]
        result = col.update_one(filter,{'$set':newData})
        return result

    def updateMany(self,filter:dict={},newData:dict={},collectionName:str=''):
        # check if collection name was setted
        if collectionName: collectionName=collectionName
        elif self.__wasCollectionSet__: collectionName=self.collectionName
        else: self.__printCollectionNameError__() ; return False
        col = self.__mongoDb[collectionName]
        result = col.update_many(filter,{'$set':newData})
        return result

    def insertOne(self,document:dict={},collectionName:str=''):
        # check if collection name was setted
        if collectionName: collectionName=collectionName
        elif self.__wasCollectionSet__: collectionName=self.collectionName
        else: self.__printCollectionNameError__() ; return False
        col = self.__mongoDb[collectionName]
        newId = col.count_documents({}) + 1
        document['_id']=newId
        result = col.insert_one(document)
        return result

    def insertMany(self,listOfDocuments:list=[],collectionName:str=''):
        # check if collection name was setted
        if collectionName: collectionName=collectionName
        elif self.__wasCollectionSet__: collectionName=self.collectionName
        else: self.__printCollectionNameError__() ; return False
        col = self.__mongoDb[collectionName]
        newId = col.count_documents({}) + 1
        newDocumentData=[]
        for d in listOfDocuments:
            d['_id']=newId
            newDocumentData.append(d)
            newId=newId+1
        result = col.insert_many(newDocumentData)
        return result

    def drop(self,collectionName:str=''):
        # check if collection name was setted
        if collectionName: collectionName=collectionName
        elif self.__wasCollectionSet__: collectionName=self.collectionName
        else: self.__printCollectionNameError__() ; return False
        result = self.__mongoDb.drop_collection(collectionName)
        return result
    
    def dropCollection(self,collections:list):
        for collectionName in collections:
            self.__mongoDb.drop_collection(collectionName)

    def export(self,exportToPath:str=''):
        collections = self.showCollections()
        collectionsList={}
        if collections:
            for collectionName in collections:
                # add colletion name to collection list to export
                collectionsList[collectionName]={}
                for item in self.findMany({},collectionName):
                    itemId = item['_id']
                    del item['_id']
                    collectionsList[collectionName][itemId]=item
        result = self.cuteME(collectionsList)
        if not exportToPath: open(f'{self.thisDir+self.databaseName}.json','w').write(result)
        else: open(f'{exportToPath+self.databaseName}.json','w').write(result)
        print(f'{Colors.good}collections in {self.databaseName} exported exportName:{self.databaseName}.json{Colors.end}')
        return True

    def Import(self,databasePath:str):
        # check if db path exits
        if not os.path.exists(databasePath):
            print(f'{Colors.fail}Path {databasePath} not found{Colors.end}')
            return False
        collections = json.loads(open(databasePath,'r').read())
        for collectionName,collectionItems in collections.items():
            # drop current collection if it exists
            if collectionName in self.showCollections(): self.dropCollection([collectionName])
            # insert item into current collection
            for itemId,itemData in collectionItems.items():
                itemData['_id']=int(itemId)
                self.C_O_L_L_E_C_T_I_O_N(collectionName).insert_one(itemData)
        
    def C_O_L_L_E_C_T_I_O_N(self,collectionName:str): return self.__mongoDb[collectionName]
    def M_O_N_G_O_C_L_I_E_N_T(self): return self.__mongoClient
    def __printCollectionNameError__(self):
        print(f'{Colors.fail}Set collection .setCollection(name) before runnig this function or set the collectionName:str{Colors.end}')
    def cuteME(self,data): return json.dumps(data,indent=4)