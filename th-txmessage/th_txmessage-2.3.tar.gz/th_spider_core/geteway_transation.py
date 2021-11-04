from th_spider_core.geteway import GETEWays;
class GetewayTransation():
    getewayIns:GETEWays
    current_getway:str
    fiexd_geteway:str

    def __init__(self,baseurl,net_label) -> None:
        self.getewayIns = GETEWays(baseurl=baseurl,net_label=net_label)
        geteway = self.getewayIns.get_net();
        fixed_geteway = self.getewayIns.get_fixed();
        self.current_getway = geteway["geteway"];
        self.getewayIns.set_geteway({"gateway":self.current_getway});
        self.fiexd_geteway  = fixed_geteway["geteway"];


    def transation(self,func):
        def wrap_func(*args, **kwargs):
            flag = func(*args,**kwargs);
            if flag == False or flag is None:
                self.getewayIns.reset_geteway(self.current_getway)
                geteway = self.getewayIns.get_net();
                self.current_getway = geteway["geteway"];
                self.getewayIns.set_geteway({"gateway":self.current_getway});
            return flag;
        return wrap_func;



    def fixed_net_do(self,func):
        def wrap_func(*args, **kwargs):
            self.getewayIns.set_geteway({"gateway":self.fiexd_geteway});
            data = func(*args,**kwargs);
            self.getewayIns.set_geteway({"gateway":self.current_getway});
            return data;
        return wrap_func;