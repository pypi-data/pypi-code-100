import html,pymysql,sys,os,re
from werkzeug.utils import secure_filename



class XSS:

    @staticmethod
    def escape(s):
        return html.escape(s,quote=True)

    @staticmethod
    def escape_form(obj):
        d={}
        for x in dict(obj.form):
            d.update({x:XSS.escape(dict(obj.form)[x][0])}) if  sys.version_info < (3,0) else d.update({x:XSS.escape(dict(obj.form)[x])})
        return d

    @staticmethod
    def escape_args(obj):
        d={}
        for x in dict(obj.args):
            d.update({x:XSS.escape(dict(obj.args)[x][0])}) if  sys.version_info < (3,0) else d.update({x:XSS.escape(dict(obj.args)[x])})
        return d


class CSRF:

    @staticmethod
    def validate_flask(obj,allowed_domains=[]):
        domains=[obj.host] if (not allowed_domains or len(allowed_domains)==0) else allowed_domains
        referer=obj.headers.get('Referer','')
        if referer.strip()=="" or referer.strip().lower()=="null":
            return False
        a=referer.split("://")[1].split("/")[0]
        if a not in domains:
            return False
        return True

    @staticmethod
    def validate(referer,allowed_domains):
        if referer.strip()=="" or referer.strip().lower()=="null":
            return False
        a=referer.split("://")[1].split("/")[0]
        if a not in allowed_domains:
            return False
        return True


class SQLI:

    @staticmethod
    def escape(s):
        return pymysql.converters.escape_string(s)

    @staticmethod
    def escape_form(obj):
        d={}
        for x in dict(obj.form):
            d.update({x:SQLI.escape(dict(obj.form)[x][0])}) if  sys.version_info < (3,0) else d.update({x:SQLI.escape(dict(obj.form)[x])})
        return d

    @staticmethod
    def escape_args(obj):
        d={}
        for x in dict(obj.args):
            d.update({x:SQLI.escape(dict(obj.args)[x][0])}) if  sys.version_info < (3,0) else d.update({x:SQLI.escape(dict(obj.args)[x])})
        return d


class FILE_UPLOAD:

    @staticmethod
    def check_file(f,allowed_extensions=['png','jpg','jpeg','gif','pdf'],allowed_mimetypes=["application/pdf","application/x-pdf","image/png","image/jpg","image/jpeg"]):
        return FILE_UPLOAD.valid_file(f,allowed_extensions,allowed_mimetypes)

    @staticmethod
    def valid_extension(f,extentions):
        try:
            return f.split(".")[1].lower() in extentions
        except:
            return False

    @staticmethod
    def valid_mimetype(f,mimetypes):
        try:
            return f.content_type.lower() in mimetypes
        except:
            return False

    @staticmethod
    def valid_file(f,extentions,mimetypes):
        return FILE_UPLOAD.valid_extension(FILE_UPLOAD.secure_filename(f),extentions) and FILE_UPLOAD.valid_mimetype(f,mimetypes)

    @staticmethod
    def secure_filename(f):
        return secure_filename(".".join(f.filename.split(".")[:2]))

    @staticmethod
    def save_file(f,path=""):
        os.makedirs(path, exist_ok=True)
        file_path=path+FILE_UPLOAD.secure_filename(f) if (path[-1]=="/" or path[-1]=="\\") else (path+'/'+FILE_UPLOAD.secure_filename(f) if sys.platform.startswith('win')==False else path+'\\'+FILE_UPLOAD.secure_filename(f))
        f.save(file_path)
        return file_path


class FORM_INPUTS:

    @staticmethod
    def alphabet(s,length=(1,25)):
        return all(x.isalpha() for x in s.strip().split()) and (len(s.strip())<=length[1] and len(s.strip())>=length[0])

    @staticmethod
    def alphanumeric(s,length=(1,25)):
        return all(x.isalnum() for x in s.strip().split()) and (len(s.strip())<=length[1] and len(s.strip())>=length[0])

    @staticmethod
    def numeric(s,length=(1,15)):
        return all(x.isnumeric() for x in s.strip().split()) and (len(s.strip())<=length[1] and len(s.strip())>=length[0])

    @staticmethod
    def email(s,regex=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',length=(6,25)):
        return True if (re.fullmatch(regex, s.strip()) and (len(s.strip())<=length[1] and len(s.strip())>=length[0])) else False

    @staticmethod
    def password(s,length=(6,25)):
        return (len(s.strip())<=length[1] and len(s.strip())>=length[0])

    @staticmethod
    def passwords_match(a,b,length=(6,25)):
        return FORM_INPUTS.password(a,length=length) and FORM_INPUTS.password(b,length=length) and a==b

    @staticmethod
    def regex_match(s,rg,length=(1,25)):
        return True if (re.fullmatch(rg, s.strip()) and (len(s.strip())<=length[1] and len(s.strip())>=length[0])) else False

    @staticmethod
    def phone_number(s,length=(8,15),replace_mines=True):
        return s.strip()[0]=="+" and FORM_INPUTS.numeric(s.strip()[1:] if replace_mines==False else s.strip()[1:].replace('-',' '),length=length)


class PATH_TRAVERSAL:

    @staticmethod
    def check(path):
        return os.path.realpath(path).startswith(os.getcwd())


class RCE:

    safe_command_characters=["-","+","/","*","_",",","'",'"','.','\\',':',"#","!","?","%","[","]","{","}","=","~","<",">","^"]
    safe_eval_characters=["-","+","/","*","%",".","(","[","]",",","{","}","=","<",">","'",'"','!',':']
    
    @staticmethod
    def command(cmd,length=(1,100),replaced_value=" "):
        for x in RCE.safe_command_characters:
            cmd=cmd.replace(x,replaced_value)
        return FORM_INPUTS.alphanumeric(cmd,length=length)

    @staticmethod
    def eval(cmd,length=(1,20),replaced_value=" "):
        for x in RCE.safe_eval_characters:
            cmd=cmd.replace(x,replaced_value)
        return FORM_INPUTS.alphanumeric(cmd,length=length)