import os, sys, json, time, datetime, requests
from dateutil.tz import tzutc
import __main__


class conn():
    def __init__(self, useLocal=None):
        self.__reqSession__ = requests.Session()
        if useLocal:
            self.__server__ = 'http://localhost:5000'
        else:
            self.__server__ = 'https://skolocfd.com'
        credFile = os.path.expanduser('~') + os.sep + '.skolo' + os.sep + 'skolo.crendentials'
        if not os.path.exists(credFile):
            self.__exc__(401, 'Missing credentials. For information on generating valid credentials visit the link provided.', link=self.__server__ + '/docs?topic=Api#Configuring%20Credentials')
            self.__cred__ = 'None'
        else:
            self.__cred__ = open(credFile, 'r').readlines()[0]
        self.checkVersion()
        
        
    def __clearLine__(self, text):
        sys.stdout.write("\033[K") #clear line 
        print(text.replace('\n',''), end='\r', flush=True)
        
    
    def checkVersion(self):
        # Check for package updates
        verFile = os.path.expanduser('~') + os.sep + '.skolo' + os.sep + 'skolo.versionCheck'
        import skolo
        if not os.path.exists(verFile) or datetime.datetime.fromtimestamp(os.path.getmtime(verFile)) + datetime.timedelta(days=7) < datetime.datetime.now():
            try:
                vMax = max(requests.get('https://pypi.org/pypi/skolo/json').json()['releases'].keys())
            except:
                vMax = skolo.__version__
            if skolo.__version__ != vMax:
                print('\nALERT: skolo-' + skolo.__version__ + ' is installed, but skolo-' + vMax + ' is available:\n    python -m pip install --upgrade skolo\n')
            with open(verFile, 'w') as f:
                pass
        
    
    def __genResp__(self, HTTPStatusCode=200, errors=[], warnings=[], messages=[], link=''):
        return {k:v for k,v in locals().items() if k != 'self'}
        
        
    def __exc__(self, code, errMsg, link='' ):
        if type(errMsg) ==  str:
            errMsg = [errMsg]
        
        errResp = self.__genResp__(code, errors=errMsg, link=link)
        if hasattr(__main__, '__file__') and ('cliparser' in __main__.__file__.lower() or os.path.basename(__main__.__file__) == 'skolo'):
            print(json.dumps(errResp, indent=4, sort_keys=True))
            sys.exit(-1)
        else:
            print('    ERROR ' + str(code) + ': ' + ' '.join(errMsg))
            print('      ' + link)
            return errResp
            #raise Exception(errMsg)
        
    
    def __buildResp__(self, r):
        resp = {}
        if r.status_code == 401:
            resp = self.__exc__(r.status_code, 'Invalid credentials. For information on generating valid credentials visit the link provided.', link=self.__server__ + '/docs?topic=Api#Configuring%20Credentials')
        elif r.status_code == 403:
            resp = self.__exc__(r.status_code, 'Expired credentials. Please generate a new authentication token at the link provided.', link=self.__server__ + '/docs?topic=Api#Configuring%20Credentials')
        elif r.status_code == 404:
            resp = self.__exc__(r.status_code, r.text)
        elif r.status_code > 399:
            resp = self.__exc__(r.status_code, 'Unhandled server error - Please contact us.')
            
        if '[' not in r.text and '{' not in r.text:
            resp.update({'messages':[r.text]})
        else:
            resp = json.loads(r.text)
        resp.update({'HTTPStatusCode':r.status_code})
        return resp, r
        
        
    def __http__(self, url, req, json=None, data=None, files=None):
        args = {'url':url, 'json':json, 'data':data, 'files':files, 'auth':(self.__cred__, 'none')}
        args = {k:v for k,v in args.items() if v != None}
        if 'files' not in args:
            args['headers'] = {'Content-Type': 'application/json'}
            
        try:
            return self.__buildResp__(getattr(self.__reqSession__, req)(**args))
        except requests.exceptions.ConnectionError:
            try:
                a = self.__reqSession__.get('http://www.google.com')
            except requests.exceptions.ConnectionError:
                resp = self.__exc__(500, 'Connection refused. It appears your internet connection is down.')
            resp = self.__exc__(500, 'Connection refused. It appears the Skolo server is unreachable.')
            return resp, None
    
    
    def __get__(self, url, json={}):
        return self.__http__(url, 'get', json)
    
    
    def __post__(self, url, json={}):
        return self.__http__(url, 'post', json)
    
    
    def __uploadFile__(self, url, file, data):
        fd = {'file': ''}
        with open(file, 'rb') as fd['file']:
            return self.__http__(url, 'post', None, data, fd)
    
    
    def __buildUrl__(self, pre, suf='', filters=True):
        if not filters:
            return self.__server__ + pre    
        return self.__server__ + pre + self.__filterUrl__(self.__filters__) + suf
    
    
    def __filterUrl__(self, filters, ignore=[]):
        self.__filters__ = filters
        t = ''
        for k,v in filters.items():
            if k in ignore:
                continue
            t += '?' + k + '=' + v
        return t
    
    
    def checkExist(self):
        url = self.__buildUrl__('/api/exists')
        return self.__get__(url)[0]
    
    
    def __listChildren__(self):
        url = self.__buildUrl__('/api/list')
        return self.__get__(url)[0]



# Generic account connection
class acct(conn):
    def __init__(self, args):
        kD = {'project':'proj', 'run':'case', 'orien':'rh'}
        self.__filters__={}
        for key in ['project', 'proj', 'run', 'case', 'orien', 'rh']:
            if key in kD:
                target = kD[key]
            else:
                target = key
            if hasattr(args, key) and getattr(args, key):
                self.__filters__[target] = getattr(args, key)
        super(acct, self).__init__(args.local)
        self.checkExist()



class Run(conn):
    def __init__(self, proj, run, useLocal=False):
        self.proj = proj
        self.run = run
        self.__filters__ = {'proj':proj, 'case':run}
        super(Run, self).__init__(useLocal)
        self.checkExist()
        
        
    def listOrientations(self):    
        """
    Returns a list of all orientations for a given run; no inputs.
    """
        resp = self.__listChildren__()
        return resp['orienList']
    
    
    def createNew(self, comment, tag='None', geometry=False, noOrientations=False, noSettings=False, noPostpro=False):
        """
    Creates a new run, based on the current run.
    Required arguments:
    comment     Run description, as seen in "comment" column of the project spreadsheet
    
    Optional arguments:
    geometry            Copy geometry from baseline
    noOrientations     Don't copy orientations from baseline
    noSettings         Don't copy run settings from baseline
    noPostpro          Don't copy post processing templates from baseline
    """
        jsonData = {'tag':tag, 'comment':comment, 'geometry':geometry, 'settings': not noSettings, 'orientations':not noOrientations, 'postpro': not noPostpro}
        url = self.__buildUrl__('/api/newCase')
        resp, r = self.__post__(url, jsonData)
                
        if r.status_code < 400:
            resp.update({'link':self.__server__ + '/case?proj=' + self.proj + '?case=' + resp['newRunName'] + '?step=settings'})
        
        return resp

        
        
# Connection to specific proj:run:orientation
class Orientation(conn):
    def __init__(self, proj, run, orien, useLocal=False):
        self.proj = proj
        self.run = run
        self.orien = orien
        self.__filters__ = {'proj':proj, 'case':run, 'rh':orien}
        super(Orientation, self).__init__(useLocal)
        self.checkExist()
        
        
    def submit(self, cmd='submit', costLimit=None):
        """
    Submits the current orientation, with the following commands:
    
    Optional arguments:
    command     Choose the command to execute:
        submit:     default. Full job submissing - setup, mesh, solve, & post
        setup:      setup the run (create job files, check inputs), but do not submit
        mesh:       mesh only
        post:       post processing only
        
    costLimit       Specify a limit to accepted cost, above which job submission will be aborted - must be an integer
    """
        if self.orien == 'geomCommon':
            return self.__genResp__(errors=['geomCommon is not a valid orientation. Such an orientation may only used by the upload command'])
        
        if cmd == None:
            cmd = 'submit'
        
        # Submit job
        suf = '?fromApi=true'
        if costLimit:
            float(costLimit)
            suf += '?costLimit=' + str(int(costLimit))
        
        url = self.__buildUrl__('/runBerd', suf)
        jsonData = {'cmd':cmd, 'rhSel':self.__filters__['rh'], 'override':'initstl'}
        resp, r = self.__post__(url, jsonData)
        print(cmd.capitalize() + ' job is queueing', end='\r')
        
        # Watch job status
        watchUrl = self.__buildUrl__('/getStatus/' + resp['jobID'] + '?fromApi=true', filters=False   )
        t, dt, tMax, status = 0, 1, 60*3, 'queueing'
        while t < tMax and status not in ['finished', 'failed']: # 5 min timeout
            watch, w = self.__get__(watchUrl)
            status = watch['task']['status']
            
            if 'log' in watch['task']['meta'] and len(watch['task']['meta']['log']) > 0:
                lines = [line for line in watch['task']['meta']['log'] if not line.startswith(' ')]
                if lines != []:
                    self.__clearLine__(lines[-1])
            elif status != 'queueing':
                self.__clearLine__(cmd + ' job is ' + status)
            
            time.sleep(dt)
            t += dt
        print()
        watch['taskLog'] = watch['task']['meta']['log']
        watch['link'] = self.__buildUrl__('/case?proj=', '?step=submit')
        del(watch['task'])
        
        return watch
        
        
    def __describeFile__(self, f):
        return {'upload':True, 'size':os.path.getsize(f), 'mtime':str(datetime.datetime.fromtimestamp(os.path.getmtime(f), tz=tzutc()))}
        
        
    def upload(self, folder, force=False):
        """
    Uploads geometry to a run or orientation:
    Required arguments:
    folder:     File or folder containing geometry to upload. stl/stl.gz are uploaded, all others are ignored
    
    Optional arguments:
    force:      Force upload regardless of file timestamp. (by default, only files newer than those on the server are uploaded)
    """
        t0 = time.time()
        from concurrent.futures import ThreadPoolExecutor
        exts = ('.stl', '.stl.gz', '.vtp', '.vtp.gz')
        
        # Create list of files
        files, tSize, t0 = {}, 0, time.time()
        if os.path.isdir(folder):
            for item in sorted(os.listdir(folder), key=str.casefold):
                if item.endswith(exts):
                    ful = folder + os.sep + item
                    files[ful] = self.__describeFile__(ful)
        elif os.path.exists(folder):
            files[folder] = self.__describeFile__(folder)
        else:
            self.__exc__('Specified file location is neither a file nor a folder: ' + folder)
        
        # See which files are actually out-of-date on server
        if not force:
            url = self.__buildUrl__('/api/needsUpload')
            respNeed, r = self.__get__(url, json=files)
            for f in files:
                if f in respNeed['fileInfo'] and not respNeed['fileInfo'][f]['upload']:
                    files[f]['upload'] = False
        
        # Parallel uploading
        resp = {'HTTPStatusCode':200}
        url = self.__buildUrl__('/upload', '?units=Meters')
        def parUpload(geom):
            resp, r = self.__uploadFile__(url, geom, files[geom])
            self.__clearLine__('    Uploading: ' + geom)
            return (geom, resp)

        pool = ThreadPoolExecutor(max_workers=6)
        filesToUpload = sorted([item for item in files if force or respNeed['fileInfo'][item]['upload']], key=str.casefold)
        for geom in pool.map(parUpload, filesToUpload):
            if geom[1]['HTTPStatusCode'] == 200:
                files[geom[0]] = 'Upload successful'
                tSize += os.path.getsize(geom[0])
        self.__clearLine__('')
        
        if len(files) == 0:
            warnings = ['Zero suitable files (' + ', '.join(exts) + ') found at destination: ' + os.path.abspath(folder)]
        else:
            warnings = []

        resp = {'HTTPStatusCode':resp['HTTPStatusCode'], 'messages':['Uploaded %.1f Mb from %i files in %.1f sec.' % (tSize/(1024*1024), len(filesToUpload), time.time()-t0)], 'errors':[], 'warnings':warnings, 'fileInfo':files}
        resp['link'] = self.__buildUrl__('/case?proj=', '?step=upload')
        return resp