# C++ Project Builder written in Python
import subprocess as sbpr
import shutil

__version__ = "0.1"

class CmdBuilder:
    
    def __init__(self, cmd: str) -> None:
        self.cmd = cmd
        self.args: list[str] = []
        self.builded_cmd = None
    
    def add_arg(self, arg: str | list, *fmt):
        if isinstance(arg, list):
            self.args.extend(arg)
            return
        self.args.append(arg.format(*fmt))
    
    def rm_arg(self, arg: str):
        del self.args[arg]
    
    def __getitem__(self, index: int | str, limit:int=-1):
        return self.args[index] if isinstance(index, int) else [a for a in self.args if a.startswith(index)][:limit]
    
    def __setitem__(self, index: int | str, value: str):
        if isinstance(index, int):
            self.args[index] = value
            return
        for i, a in enumerate(self.args):
            if a.startswith(index):
                self.args[i] = value
    
    def _build_cmd(self, sep: str=" "):
        return  sep.join((self.cmd, *self.args))
    
    def build_cmd(self, sep: str=" "):
        self.builded_cmd = self._build_cmd(sep)
        return self.builded_cmd
    
    def run(self):
        return sbpr.run(self.builded_cmd)


class CXXProject:
    
    def __init__(self, compiler=None, cxx_std: str="c++11", all_warn: bool=True) -> None:
        self.comp = compiler
        if self.comp is None:
            if shutil.which("g++") is not None:
                print("Found gcc")
                self.comp = "g++"
            elif shutil.which("clang++") is not None:
                print("Found clang")
                self.comp = "clang++"
            else:
                print("No C++ compiler found. Required gcc or clang")
                exit(1)
        
        self.cmdb = None
        self.cxx_std = cxx_std
        self.Wall = all_warn
        
        self.libs = {}
        self.incl = []
        
        self.raw_args = []
        
        self.output = ""
    
    def add_include(self, path: str):
        if isinstance(path, (tuple, list)):
            self.incl.extend(path)
            return
        if path not in self.incl:
            self.incl.append(path)

    def add_lib(self, path: str, libname: str):
        self.libs[path] = self.libs.get(path, [])
        
        if isinstance(libname, (tuple, list)):
            self.libs[path].extend(libname)
            return
        self.libs[path].append(libname)
    
    def set_output(self, out: str):
        self.output = out
    
    def add_raw(self, raw_arg: str | list):
        if isinstance(raw_arg, list):
            self.raw_args.extend(raw_arg)
            return
        self.raw_args.append(raw_arg)
    
    def add_flag(self, flag: str, value: str=None, prefix: str='-', assign_char: str='='):
        self.add_raw('{p}{f}{back}'.format(p=prefix, f=flag, back='' if not value else f'{assign_char}{value}'))
    
    def build_cmd(self, m: str):
        self.cmdb = CmdBuilder(self.comp)
        
        self.cmdb.add_arg(m)
        
        if self.output:
            self.cmdb.add_arg(["-o", self.output])
        
        if self.Wall is True:
            self.cmdb.add_arg("-Wall")
        
        self.cmdb.add_arg("-std={}", self.cxx_std)
        
        for i in self.incl:
            self.cmdb.add_arg("-I{}", i)
        
        for libp, ps in self.libs.items():
            self.cmdb.add_arg("-L{}", libp)
            for p in ps:
                self.cmdb.add_arg("-l{}", p)
        
        self.cmdb.add_arg(self.raw_args)
        
        return self.cmdb.build_cmd()
    
    def run(self, main_file: str):
        print(self.build_cmd(main_file), end="\n\n")
        if (c := self.cmdb.run().returncode) != 0:
            print("\nError Occured while compiling. Exit Code:", c)
            exit(c)
    
    def autorun(self, main_file: str):
        self.run(main_file)
        o = self.output or "a.exe"
        print("Exit Code:", (c := sbpr.run(o).returncode))
        exit(c)