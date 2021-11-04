import pysftp, os

import os,pickle
class Remote:
    def __init__(self, conf):
        self.c = conf
        self.hist_pickle=os.path.join(self.c.local_root,"up_hist.pickle").replace("\\","/")

    def get_upload_records(self):
        if os.path.exists(self.hist_pickle):
            with open(self.hist_pickle, 'rb') as file:
                try:
                    data=pickle.load(file)
                    return data
                except EOFError:
                    return None

    def save_upload_records(self, data):
        with open(self.hist_pickle, 'wb') as file:
            pickle.dump(data, file)

    def upload_record_or_not(self, file_path):
        if file_path==self.hist_pickle:
            return False
        already=self.get_upload_records()
        new_rev=os.path.getmtime(file_path)
        if already is not None:
            old_rev=already.get((self.c.host, file_path), None)
            if new_rev!=old_rev:
                already[(self.c.host, file_path)]=new_rev
                self.save_upload_records(already)
                return True
            else:
                return False
        else:
            dic={}
            dic[(self.c.host, file_path)]=new_rev
            self.save_upload_records(dic)
            return True
    def upload(self, data):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        with pysftp.Connection(self.c.host, username=self.c.user, port=self.c.port,password=self.c.pwd, cnopts=cnopts) as shell:
            for i in data:
                will_up=self.upload_record_or_not(i[0])
                if will_up:
                    print ("upload file:",i[0])
                    remote_dir = os.path.dirname(i[1])
                    shell.makedirs(remote_dir, mode=777)
                    shell.put(i[0], i[1])
    
    def download(self, data):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        with pysftp.Connection(self.c.host, username=self.c.user, port=self.c.port,password=self.c.pwd, cnopts=cnopts) as shell:
            for i in data:
                local_dir = os.path.dirname(i[0])
                os.makedirs(local_dir, exist_ok=True, mode=777)
                shell.get(i[1], i[0])
    
    def get_remote(self, dir):
        files = self._get_remote(dir, [])
        return files
    
    def _get_remote(self, root, res):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        with pysftp.Connection(self.c.host, username=self.c.user, port=self.c.port,password=self.c.pwd, cnopts=cnopts) as shell:
            data = shell.listdir(root)
            for d in data:
                new = os.path.join(root, d).replace("\\", "/")
                if shell.isfile(new):
                    res.append(new)
                else:
                    self._get_remote(new, res)
        return res
    
    def cmd(self, cmds):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        with pysftp.Connection(self.c.host, username=self.c.user,port=self.c.port, password=self.c.pwd, cnopts=cnopts) as shell:
            common_cmds = ["/usr/bin/bash -c", f"cd {self.c.remote_root}"]
            all = common_cmds + cmds
            cmd = ";".join(all)
            res = shell.execute(cmd)
            print("***********************")
            for i in res:
                print(i.decode("utf-8"))
