# ***************************************************************
# Copyright (c) 2021 Jittor. All Rights Reserved. 
# Maintainers: Dun Liang <randonlang@gmail.com>. 
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
# ***************************************************************
from multiprocessing import Pool
import multiprocessing as mp
import subprocess as sp
import os
import re
import sys
import inspect
import datetime
import contextlib
import platform
import threading
import time
from ctypes import cdll
import shutil
import urllib.request

if platform.system() == 'Darwin':
    mp.set_start_method('fork')

class LogWarper:
    def __init__(self):
        self.log_silent = int(os.environ.get("log_silent", "0"))
        self.log_v = int(os.environ.get("log_v", "0"))

    def log_capture_start(self):
        cc.log_capture_start()

    def log_capture_stop(self):
        cc.log_capture_stop()

    def log_capture_read(self):
        return cc.log_capture_read()

    def _log(self, level, verbose, *msg):
        if self.log_silent or verbose > self.log_v:
            return
        ss = ""
        for m in msg:
            if callable(m):
                m = m()
            ss += str(m)
        msg = ss
        f = inspect.currentframe()
        fileline = inspect.getframeinfo(f.f_back.f_back)
        fileline = f"{os.path.basename(fileline.filename)}:{fileline.lineno}"
        if cc and hasattr(cc, "log"):
            cc.log(fileline, level, verbose, msg)
        else:
            time = datetime.datetime.now().strftime("%m%d %H:%M:%S.%f")
            tid = threading.get_ident()%100
            v = f" v{verbose}" if verbose else ""
            print(f"[{level} {time} {tid:02}{v} {fileline}] {msg}")
    
    def V(self, verbose, *msg): self._log('i', verbose, *msg)
    def v(self, *msg): self._log('i', 1, *msg)
    def vv(self, *msg): self._log('i', 10, *msg)
    def vvv(self, *msg): self._log('i', 100, *msg)
    def vvvv(self, *msg): self._log('i', 1000, *msg)
    def i(self, *msg): self._log('i', 0, *msg)
    def w(self, *msg): self._log('w', 0, *msg)
    def e(self, *msg): self._log('e', 0, *msg)
    def f(self, *msg): self._log('f', 0, *msg)

class DelayProgress:
    def __init__(self, msg, n):
        self.msg = msg
        self.n = n
        self.time = time.time()

    def update(self, i):
        if LOG.log_silent:
            return
        used = time.time() - self.time
        if used > 2:
            eta = used / (i+1) * (self.n-i-1)
            print(f"{self.msg}({i+1}/{self.n}) used: {used:.3f}s eta: {eta:.3f}s", end='\r')
            if i==self.n-1: print()

# check is in jupyter notebook
def in_ipynb():
    try:
        cfg = get_ipython().config 
        if 'IPKernelApp' in cfg:
            return True
        else:
            return False
    except:
        return False

@contextlib.contextmanager
def simple_timer(name):
    print("Timer start", name)
    now = time.time()
    yield
    print("Time stop", name, time.time()-now)

@contextlib.contextmanager
def import_scope(flags):
    if os.name != 'nt':
        prev = sys.getdlopenflags()
        sys.setdlopenflags(flags)
    yield
    if os.name != 'nt':
        sys.setdlopenflags(prev)

def try_import_jit_utils_core(silent=None):
    global cc
    if cc: return
    if not (silent is None):
        prev = os.environ.get("log_silent", "0")
        os.environ["log_silent"] = str(int(silent))
    try:
        # if is in notebook, must log sync, and we redirect the log
        if is_in_ipynb: os.environ["log_sync"] = "1"
        import jit_utils_core as cc
        if is_in_ipynb:
            cc.ostream_redirect(True, True)
    except Exception as _:
        if int(os.environ.get("log_v", "0")) > 0:
            print(_)
        pass
    if not (silent is None):
        os.environ["log_silent"] = prev

def run_cmd(cmd, cwd=None, err_msg=None, print_error=True):
    LOG.v(f"Run cmd: {cmd}")
    if cwd:
        r = sp.run(cmd, cwd=cwd, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT)
    else:
        r = sp.run(cmd, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT)
    try:
        s = r.stdout.decode('utf8')
    except:
        s = r.stdout.decode('gbk')
    if r.returncode != 0:
        if print_error:
            sys.stderr.write(s)
        if err_msg is None:
            err_msg = f"Run cmd failed: {cmd}"
        if not print_error:
            err_msg += "\n"+s
        raise Exception(err_msg)
    if len(s) and s[-1] == '\n': s = s[:-1]
    return s


def do_compile(args):
    cmd, cache_path, jittor_path = args
    try_import_jit_utils_core(True)
    if cc:
        return cc.cache_compile(cmd, cache_path, jittor_path)
    else:
        run_cmd(cmd)
        return True

pool_size = 0

def pool_cleanup():
    global p
    p.__exit__(None, None, None)
    del p

def pool_initializer():
    if os.name == 'nt':
        os.environ['log_silent'] = '1'
        os.environ['gdb_path'] = ""
    if cc is None:
        try_import_jit_utils_core()
    if cc:
        cc.init_subprocess()

def run_cmds(cmds, cache_path, jittor_path, msg="run_cmds"):
    global pool_size, p
    bk = mp.current_process()._config.get('daemon')
    mp.current_process()._config['daemon'] = False
    if pool_size == 0:
        try:
            mem_bytes = get_total_mem()
            mem_gib = mem_bytes/(1024.**3)
            pool_size = min(16,max(int(mem_gib // 3), 1))
            LOG.i(f"Total mem: {mem_gib:.2f}GB, using {pool_size} procs for compiling.")
        except ValueError:
            # On macOS, python with version lower than 3.9 do not support SC_PHYS_PAGES.
            # Use hard coded pool size instead.
            pool_size = 4
            LOG.i(f"using {pool_size} procs for compiling.")
        if os.name == 'nt':
            # a hack way to by pass windows
            # multiprocess spawn init_main_from_path.
            # check spawn.py:get_preparation_data
            spec_bk = sys.modules['__main__'].__spec__
            tmp = lambda x:x
            tmp.name = '__main__'
            sys.modules['__main__'].__spec__ = tmp
        p = Pool(pool_size, initializer=pool_initializer)
        p.__enter__()
        if os.name == 'nt':
            sys.modules['__main__'].__spec__ = spec_bk
        import atexit
        atexit.register(pool_cleanup)
    cmds = [ [cmd, cache_path, jittor_path] for cmd in cmds ]
    try:
        n = len(cmds)
        dp = DelayProgress(msg, n)
        for i,_ in enumerate(p.imap_unordered(do_compile, cmds)):
            dp.update(i)
    finally:
        mp.current_process()._config['daemon'] = bk

if os.name=='nt' and getattr(mp.current_process(), '_inheriting', False):
    # when windows spawn multiprocess, disable sub-subprocess
    os.environ["DISABLE_MULTIPROCESSING"] = '1'
    os.environ["log_silent"] = '1'
        
if os.environ.get("DISABLE_MULTIPROCESSING", '0') == '1':
    os.environ["use_parallel_op_compiler"] = '0'
    def run_cmds(cmds, cache_path, jittor_path, msg="run_cmds"):
        cmds = [ [cmd, cache_path, jittor_path] for cmd in cmds ]
        n = len(cmds)
        dp = DelayProgress(msg, n)
        for i,cmd in enumerate(cmds):
            dp.update(i)
            do_compile(cmd)


def download(url, filename):
    if os.path.isfile(filename):
        if os.path.getsize(filename) > 100:
            return
    LOG.v("Downloading", url)
    urllib.request.urlretrieve(url, filename)
    LOG.v("Download finished")

def get_jittor_version():
    path = os.path.dirname(__file__)
    with open(os.path.join(path, "../jittor/__init__.py"), "r", encoding='utf8') as fh:
        for line in fh:
            if line.startswith('__version__'):
                version = line.split("'")[1]
                break
        else:
            raise RuntimeError("Unable to find version string.")
    return version

def get_str_hash(s):
    import hashlib
    md5 = hashlib.md5()
    md5.update(s.encode())
    return md5.hexdigest()

def get_cpu_version():
    v = platform.processor()
    try:
        if os.name == 'nt':
            import winreg
            key_name = r"Hardware\Description\System\CentralProcessor\0"
            field_name = "ProcessorNameString"
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_name)
            value = winreg.QueryValueEx(key, field_name)[0]
            winreg.CloseKey(key)
            v = value
        elif platform.system() == "Darwin":
            r, s = sp.getstatusoutput("sysctl -a sysctl machdep.cpu.brand_string")
            if r==0:
                v = s.split(":")[-1].strip()
        else:
            with open("/proc/cpuinfo", 'r') as f:
                for l in f:
                    if l.startswith("model name"):
                        v = l.split(':')[-1].strip()
                        break
    except:
        pass
    return v
    
def short(s):
    ss = ""
    for c in s:
        if str.isidentifier(c) or str.isnumeric(c) \
            or str.isalpha(c) or c in '.-+':
            ss += c
    if len(ss)>14:
        return ss[:14]+'x'+get_str_hash(ss)[:2]
    return ss

def find_cache_path():
    from pathlib import Path
    path = str(Path.home())
    # jittor version key
    jtv = "jt"+get_jittor_version().rsplit('.', 1)[0]
    # cc version key
    ccv = cc_type+get_version(cc_path)[1:-1] \
        if cc_type != "cl" else cc_type
    # os version key
    osv = platform.platform() + platform.node()
    if len(osv)>14:
        osv = osv[:14] + 'x'+get_str_hash(osv)[:2]
    # py version
    pyv = "py"+platform.python_version()
    # cpu version
    cpuv = get_cpu_version()
    dirs = [".cache", "jittor", jtv, ccv, pyv, osv, cpuv]
    dirs = list(map(short, dirs))
    cache_name = "default"
    try:
        if "cache_name" in os.environ:
            cache_name = os.environ["cache_name"]
        else:
            # try to get branch name from git
            r = sp.run(["git","branch"], cwd=os.path.dirname(__file__), stdout=sp.PIPE,
                   stderr=sp.PIPE)
            assert r.returncode == 0
            bs = r.stdout.decode().splitlines()
            for b in bs:
                if b.startswith("* "): break
            
            cache_name = b[2:]
        for c in " (){}": cache_name = cache_name.replace(c, "_")
    except:
        pass
    if os.environ.get("debug")=="1":
        dirs[-1] += "_debug"
    for name in os.path.normpath(cache_name).split(os.path.sep):
        dirs.append(name)
    os.environ["cache_name"] = cache_name
    LOG.v("cache_name: ", cache_name)
    path = os.path.join(path, *dirs)
    os.makedirs(path, exist_ok=True)
    if path not in sys.path:
        sys.path.append(path)
    return path

def get_version(output):
    if output.endswith("mpicc"):
        version = run_cmd(f"\"{output}\" --showme:version")
    elif os.name == 'nt' and (
        output.endswith("cl") or output.endswith("cl.exe")):
        version = run_cmd(output)
    else:
        version = run_cmd(f"\"{output}\" --version")
    v = re.findall("[0-9]+\\.[0-9]+\\.[0-9]+", version)
    if len(v) == 0:
        v = re.findall("[0-9]+\\.[0-9]+", version)
    assert len(v) != 0, f"Can not find version number from: {version}"
    if 'clang' in version and platform.system() == 'Darwin':
        version = "("+v[-3]+")"
    else:
        version = "("+v[-1]+")"
    return version

def get_int_version(output):
    ver = get_version(output)
    ver = ver[1:-1].split('.')
    ver = tuple(( int(v) for v in ver ))
    return ver

def find_exe(name, check_version=True, silent=False):
    output = shutil.which(name)
    if not output:
        raise RuntimeError(f"{name} not found")
    if check_version:
        version = get_version(name)
    else:
        version = ""
    if not silent:
        LOG.i(f"Found {name}{version} at {output}.")
    return output

def env_or_find(name, bname, silent=False):
    if name in os.environ:
        path = os.environ[name]
        if path != "":
            version = get_version(path)
            if not silent:
                LOG.i(f"Found {bname}{version} at {path}")
        return path
    return find_exe(bname, silent=silent)

def get_cc_type(cc_path):
    bname = os.path.basename(cc_path)
    if "clang" in bname: return "clang"
    if "icc" in bname or "icpc" in bname: return "icc"
    if "g++" in bname: return "g++"
    if "cl" in bname: return "cl"
    LOG.f(f"Unknown cc type: {bname}")

def get_py3_config_path():
    global _py3_config_path
    if _py3_config_path: 
        return _py3_config_path

    if os.name == 'nt':
        return None
    else:
        # Search python3.x-config
        # Note:
        #   This may be called via c++ console. In that case, sys.executable will
        #   be a path to the executable file, rather than python. So, we cannot infer 
        #   python-config path only from sys.executable.
        #   To address this issue, we add predefined paths to search,
        #       - Linux: /usr/bin/python3.x-config
        #       - macOS (installed via homebrew): /usr/local/bin/python3.x-config
        #   There may be issues under other cases, e.g., installed via conda.
        py3_config_paths = [
            os.path.dirname(sys.executable) + f"/python3.{sys.version_info.minor}-config",
            sys.executable + "-config",
            f"/usr/bin/python3.{sys.version_info.minor}-config",
            f"/usr/local/bin/python3.{sys.version_info.minor}-config",
            f'/opt/homebrew/bin/python3.{sys.version_info.minor}-config',
            os.path.dirname(sys.executable) + "/python3-config",
        ]
        if "python_config_path" in os.environ:
            py3_config_paths.insert(0, os.environ["python_config_path"])

        for py3_config_path in py3_config_paths:
            if os.path.isfile(py3_config_path):
                break
        else:
            raise RuntimeError(f"python3.{sys.version_info.minor}-config "
                f"not found in {py3_config_paths}, please specify "
                f"enviroment variable 'python_config_path',"
                f" or install python3.{sys.version_info.minor}-dev")
        _py3_config_path = py3_config_path
        return py3_config_path

def get_py3_include_path():
    global _py3_include_path
    if _py3_include_path: 
        return _py3_include_path
    
    if os.name == 'nt':
        # Windows
        sys.executable = sys.executable.lower()
        _py3_include_path = '-I"' + os.path.join(
            os.path.dirname(sys.executable),
            "include"
        ) + '"'
    else:
        _py3_include_path = run_cmd(get_py3_config_path()+" --includes")
    return _py3_include_path


def get_py3_extension_suffix():
    global _py3_extension_suffix
    if _py3_extension_suffix: 
        return _py3_extension_suffix
    
    if os.name == 'nt':
        # Windows
        _py3_extension_suffix = f".cp3{sys.version_info.minor}-win_amd64.pyd"
    else:
        _py3_extension_suffix = run_cmd(get_py3_config_path()+" --extension-suffix")
    return _py3_extension_suffix

def get_total_mem():
    if os.name == 'nt':
        from ctypes import Structure, c_int32, c_uint64, sizeof, byref, windll
        class MemoryStatusEx(Structure):
            _fields_ = [
                ('length', c_int32),
                ('memoryLoad', c_int32),
                ('totalPhys', c_uint64),
                ('availPhys', c_uint64),
                ('totalPageFile', c_uint64),
                ('availPageFile', c_uint64),
                ('totalVirtual', c_uint64),
                ('availVirtual', c_uint64),
                ('availExtendedVirtual', c_uint64)]
            def __init__(self):
                self.length = sizeof(self)
        m = MemoryStatusEx()
        assert windll.kernel32.GlobalMemoryStatusEx(byref(m))
        return m.totalPhys
    else:
        return os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')

is_in_ipynb = in_ipynb()
cc = None
LOG = LogWarper()

check_msvc_install = False
msvc_path = ""
if os.name == 'nt' and os.environ.get("cc_path", "")=="":
    from pathlib import Path
    msvc_path = os.path.join(str(Path.home()), ".cache", "jittor", "msvc")
    cc_path = os.path.join(msvc_path, "VC", r"_\_\_\_\_\bin", "cl.exe")
    check_msvc_install = True
else:
    cc_path = env_or_find('cc_path', 'g++', silent=True)
os.environ["cc_path"] = cc_path
cc_type = get_cc_type(cc_path)
cache_path = find_cache_path()

_py3_config_path = None
_py3_include_path = None
_py3_extension_suffix = None

if os.name == 'nt':
    from pathlib import Path
    try:
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context
    except:
        pass
    if check_msvc_install:
        if not os.path.isfile(cc_path):
            from jittor_utils import install_msvc
            install_msvc.install(msvc_path)
    mpath = os.path.join(str(Path.home()), ".cache", "jittor", "msvc")
    if cc_path.startswith(mpath):
        msvc_path = mpath
    os.RTLD_NOW = os.RTLD_GLOBAL = os.RTLD_DEEPBIND = 0
    path = os.path.dirname(cc_path).replace('/', '\\')
    if path:
        sys.path.insert(0, path)
        os.environ["PATH"] = path+';'+os.environ["PATH"]
        if hasattr(os, "add_dll_directory"):
            os.add_dll_directory(path)
