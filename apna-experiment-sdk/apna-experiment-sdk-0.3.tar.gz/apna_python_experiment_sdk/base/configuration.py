class Configuration:
    conf = dict()
    
    def __init__(self, **kwargs):
        self.conf.update(kwargs)
        
    def get_conf(self) -> dict:
        return self.conf