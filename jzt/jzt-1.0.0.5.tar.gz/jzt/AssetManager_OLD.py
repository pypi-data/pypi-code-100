import requests
import datetime
import ast


class AssetManager:
    
    url="https://console.jazeetech.com/getAsset/"
    
    def __init__(self, access_key, url=""):
        
        self.access_key = access_key
        if(len(url)!=0):
            self.url = url

    def getAsset(self, name=""):
           
        request_url = self.url+"?asset={0}&key={1}".format(name, self.access_key)
        response = requests.get(request_url)
        if(response.status_code==200):
            response = response.content.decode('ascii')
            response = ast.literal_eval(response)

            success = response["success"]=="True"    
            if(success):
                try:
                    asset_type = response["type"]
                    if(asset_type == "text"):
                        text = response["text"]
                        return text
                        
                    elif(asset_type == "number"):
                        number = float(response["number"])
                        return number
                        
                    elif(asset_type == "credential"):
                        username = response["username"]
                        password = response["password"]
                        return (username, password)
                except Exception as e:
                    #print(e)
                    message = "Somthing went wrong"
                    raise Exception(message)
                    
            else:
                message = response["message"]
                raise Exception(message)
            
        else:
            message = "Connection could not be established. Please check your internet connection."
            raise Exception(message)
    





