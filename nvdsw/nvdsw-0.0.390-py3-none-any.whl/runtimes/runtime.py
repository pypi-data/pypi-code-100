from abc import ABC,abstractmethod 

class Runtime(ABC):
    @abstractmethod  
    def auth(self, creds): 
        pass

    @abstractmethod  
    def logout(self): 
        pass

    @abstractmethod
    def authed(self):
        pass

    # get the user stuff provided with the auth data
    @abstractmethod
    def get_user(self):
        pass
    

    @abstractmethod
    def get_menu(self):
        pass

    @abstractmethod
    def get_flavors(self):
        pass

    @abstractmethod
    def get_flavor(self, flavor_id):
        pass

    @abstractmethod
    def get_menu_item(self, menu_item_id):
        pass

    @abstractmethod
    def create_resource(self, menu_item_id, flavor_id, *params):
        pass

    @abstractmethod 
    def get_resource_ids(self):
        pass 
    
    @abstractmethod
    def get_resources(self):
        pass 

    # for status purposes
    @abstractmethod
    def get_resource(self, resource_id):
        pass   

    @abstractmethod
    def delete_resource(self, resource_id):
        pass   

    @abstractmethod
    def stop_resource(self, resource_id):
        pass 

    @abstractmethod
    def start_resource(self, resource_id):
        pass 

    @abstractmethod
    def restart_resource(self, resource_id):
        pass                                    