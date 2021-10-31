from pathlib import Path 
import re
import os
from urllib.request import urlretrieve
from urllib.parse import urlparse
import urllib 
import click
import sys
import threading 
import time
import requests
from bs4 import BeautifulSoup
class async_run:
    def __init__(self,max_threads = 5,time_wait = 0.1):
        self.running_threads = 0
        self.max_threads = max_threads
        self.time_wait = time_wait

    def append_params(self,func,params):
        while self.running_threads >= self.max_threads:
            time.sleep(self.time_wait)
        t=threading.Thread(target=self.wrapper_func,args=(func,params))
        t.start()
    def wrapper_func(self,*args):
        func,params = args
        self.running_threads += 1
        t = func(*params)
        self.running_threads -= 1
        return t 
global_dict = dict()
def is_html_file(fname):
    html_set = global_dict['html_set']
    if str(fname) in html_set:
        return False 
    else:
        html_set.add(str(fname))
    data = open(fname,'rb').read(1000)
    if data.find(b'html'):
        return True 
    else:
        return False

def get_html_url_bs4(html):
    pagesoup=BeautifulSoup(html,'lxml')
    hrefs = [('h',link.get('href')) for link  in pagesoup.find_all(name='a')]
    sts = ('src','data-src','xsrc')
    src = [('s',link.get(src_title)) for link  in pagesoup.find_all() for src_title in sts]
    src = [i for i in src if i[1]]
    return hrefs+src
def get_html_url_re(html):
    if isinstance(html,bytes):
        return get_html_url_re_bytes(html)
    def deal_with(url):
        title = 'h' if url[0] == 'h' else 's'
        for nos in '(+\\':
            if url.find(nos) !=-1:
                ut = None 
                break
        else:
            dn = url.find('=')
            ut = url[dn+1:].strip()
            if ut[0] == '"' or ut[0] == "'":
                ut = ut[1:]
        return title,ut
    href = re.compile('(href|src)= *.[^\'\" )]*')
    s = [deal_with(h.group()) for h in href.finditer(html)]
    s = [i for i in s if i[1]]
    return s
def get_html_url_re_bytes(html):
    def deal_with(url):
        title = 'h' if url[0] == b'h' else 's'
        for nos in b'(+\\':
            if url.find(nos) !=-1:
                ut = None 
                break
        else:
            dn = url.find(b'=')
            ut = url[dn+1:].strip()
            if ut[0] == ord('"') or ut[0] == ord("'"):
                ut = ut[1:]
        return title,ut
    href = re.compile(b'(href|src)= *.[^\'\" )]*')
    # print(html)
    # for h in href.finditer(html):
    #     print(h.group())
    s = [deal_with(h.group()) for h in href.finditer(html)]
    s = [(i,v.decode()) for i,v in s if v]
    return s
def get_html_url(html,filetype='text',ftype='bs4',title_dict = {'h':'href','s':'src'},charset_list=[1,'utf-8','gbk']):
    if filetype == 'path':
        read_ok = False
        for i in range(2):
            try:
                charset = charset_list[charset_list[0]]
                html = open(html,encoding=charset).read()
                read_ok = True
            except Exception as e:
                charset_list[0] += 1
                if charset_list[0] == len(charset_list):
                    charset_list[0] = 1
        if not read_ok:
            return []
    if ftype == 'bs4':
        t = get_html_url_bs4(html)
    else:
        t = get_html_url_re(html)
    return [f'{title_dict[title]}="{val}"' for title,val in t]


def get_all_url(filename):
    p = Path(filename)
    if p.is_file():
        i = p
        for h in get_html_url(i,filetype='path'):
            yield i.parent,h
        yield False,False
    else:
        htmls = 0
        for root,_,files in os.walk(p): 
            proot = Path(root)
            for j in files:
                i = proot / j
                if is_html_file(i):
                    htmls += 1
                    for h in get_html_url(i,filetype='path'):
                        yield i.parent,h
        if htmls == 0:
            yield False,False

            
def get_name_url(p,url,http='https'):
    # p:dir_path : Path('www.baidu.com/s/')
    urlp = urlparse(url)
    netloc = urlp.netloc
    if not url:
        return None,None
    if netloc:
        fname = Path(url[url.find('://')+3:])
        if not url.startswith('http'):
            url = http +':'+url
        hurl  = url
    else:
        ipre = 0
        while url.startswith('../'):
            ipre += 1
            url = url[3:]
        
        if url[0:2] == './':
            url = url[2:]
        elif url[0] == '/':
            ipre = len(p.parts) - 1
            url = url[1:]


        if ipre>0:
            parts = p.parts[:-ipre]
        else:
            parts = p.parts
        pdir = Path(os.sep.join(parts))
        fname = pdir / url
        hurl = http+'://'+str(fname)
    return fname,hurl


def run(http,dirname,ftypes,same_string):
    if global_dict['one']:
        u = get_all_url(global_dict['one_file'])
    else:
        u = get_all_url(dirname)
    if ftypes:
        ftypes = ['.'+i for i in ftypes.split(',')]
    dn = {'s':4,'h':5}
    ii = 0
    for p,surl in u:
        if p is False:
            return True
        url = surl[dn[surl[0]]:][1:-1]
        download = False
        filter_type = False
        if ftypes:
            filter_type = True
            for ft in ftypes:
                if url.endswith(ft):
                    download = True 
                    break 
        if same_string:
            filter_type = True 
            if url.find(same_string) != -1:
                download = True
        if not filter_type:
            download = True
        if download:
            ii += 1
            fname,hurl = get_name_url(p,url,http)
            if fname:
                download_file(fname,hurl)
    return False

def download_file_kernel(fname,url):
    # if urlparse(url).netloc != global_dict['netloc']:
    #     return
    
    parent_dir = fname.parent
    # 建立文件夹
    if not parent_dir.is_dir():
        pp = Path('.')
        for i in parent_dir.parts:
            pp = pp / i
            if pp.is_file():
                pt = pp.with_suffix('.__temp__ll')
                os.rename(pp,pt)
                os.makedirs(pp)
                os.rename(pt,pp/'index.html')
            elif not pp.exists():
                os.makedirs(pp)
    # 下载文件
    if fname.exists():
        print('file already exists.',fname)
        return 'exit'
    print('downloading file',fname)
    try:
        content = global_dict['session'].get(url, stream=True)
        with open(fname, "wb") as fp:
            for chunk in content.iter_content(chunk_size=512):
                fp.write(chunk)
        return 'download'
    except Exception as e:
        print('download failed',e)

def download_file(fname,url):
    url_set = global_dict['url_set']
    if url in url_set:
        return
    url_set.add(url)
    global_dict['downloader'].append_params(download_file_kernel,(fname,url))
def init_env(fname,url,netloc):
    t = download_file_kernel(fname,url)
    if global_dict['one']:
        global_dict['one_file'] = fname 
        return
    if t=='exit':
        if fname.is_dir():
            p = fname / 'index.html'
            if not p.exists():
                download_file_kernel(p,url)
            else: 
                return
    if fname.name == netloc:
        temp_name = fname.with_suffix('.__temp__ll')
        os.rename(fname,temp_name)
        os.mkdir(fname)
        os.rename(temp_name,fname/'index.html')
def decode_direction(dirname):
    # 将编码过得目录名称进行解码
    parse = urllib.parse
    for root,dirs,fs in os.walk(dirname):
        proot = Path(root)
        for fn in fs:
            nfn = parse.unquote(fn)
            if fn != nfn:
                print(proot/nfn)
                os.rename(proot/fn,proot/nfn)
        r0 = parse.unquote(root)
        if r0 != root:
            print(r0)
            os.rename(root,r0)
@click.command()
@click.argument('args',nargs=-1)
@click.option('--parallel','-p',default=2,help='必行下载数')
@click.option('--url',default=None,help='指定url')
@click.option('--ftypes',default=None,help='指定文件类型: jpg,jpeg')
@click.option('--ss',default=None,help='same_string,匹配到相似字符后再进行匹配')
@click.option('--decode_name',default='',help='对目录名称进行解码处理')
@click.option('--convert_links','-k',default='',help='转换为本地url')
@click.option('--one',help="只下载一个页面的所有信息",is_flag=True)
def main(args,parallel,url,ss,ftypes,decode_name,convert_links,one):
    if not url:
        url = args[0]
    headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}  

    purl = urlparse(url)
    scheme = purl.scheme
    netloc = purl.netloc 
    global_dict['scheme'] = scheme
    global_dict['netloc'] = netloc
    global_dict['session'] = requests.Session()
    global_dict['session'].headers = headers
    global_dict['downloader'] = async_run(max_threads=parallel)
    fname,hurl = get_name_url(None,url)
    global_dict['url_set'] = set()
    global_dict['html_set'] = set()
    global_dict['one'] = one 
    global_dict['first_url'] = url

    init_env(fname,url,netloc)
    while True:
        if run(scheme,netloc,ftypes,ss):
            break
        if one:
            break
    if decode_name:
        decode_direction(decode_name)
    if convert_links:
        from . import convert_url
        convert_url.convert_dir(convert_links,parallel)
if __name__=='__main__':
    main()
