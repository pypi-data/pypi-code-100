# coding=utf-8
#
# Author: Ualter Otoni Pereira
# ualter.junior@gmail.com

import os, sys
import json, time
import boto3, base64
import docker
import threading
from typing import Tuple
from botocore.exceptions import ClientError
from pyecr.messages import Messages
from pyecr.utils import Utils
from pyecr.style import Style
from pyecr.completers_suggesters import *
from pyecr.completers_suggesters import _request_confirm_y_n as confirm_y_n
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML as Prompt_HTML
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.output import ColorDepth

class PyEcr:

    def __init__(self):
        print(f" {Style.CYAN}{Emoticons.pointRight()} Loading...")
        caller_identity = self.get_current_aws_session()
        self.aws_account = caller_identity["Account"]

    def botoSession(self, profile="default"):
        # Check if there's a session already (STS)    
        if 'AWS_ACCESS_KEY_ID' in os.environ and \
           'AWS_SECRET_ACCESS_KEY' in os.environ and \
           'AWS_SESSION_TOKEN' in os.environ:
            return boto3.session.Session(
                aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                aws_session_token=os.environ['AWS_SESSION_TOKEN']
            )
        if not profile:
           return boto3.Session()
        return boto3.Session(profile_name=profile)

    def docker_pull_image(self, suggestions) -> Tuple[str, str]:
        images        = suggestions
        message       = [('class:green', f' Docker Image to Pull  <TAB>.....................................: ')]
        session       = PromptSession()
        toolbar       = Prompt_HTML(f'{toolbar_margin}{toolbar_default}')
        image_name    = session.prompt(message,style=Prompt_Style,
                                 completer=MyCustomCompleter(suggestions),
                                 complete_while_typing=True,validate_while_typing=False,
                                 #validator=MyValidator(images,"Image not valid, different from the ECR Repository name"),
                                 key_bindings=general_bindings,bottom_toolbar=toolbar,
                                 auto_suggest=MySuggestion(images),rprompt='<<<    Image Pull (Local Docker) ',color_depth=ColorDepth.TRUE_COLOR)
        
        if not image_name or image_name.strip() == "":
            return None, None

        
        message       = [('class:green', f' Docker Image Tag to Pull  <TAB>.................................: ')]
        session       = PromptSession()
        toolbar       = Prompt_HTML(f'{toolbar_margin}{toolbar_default}')
        image_tag     = session.prompt(message,style=Prompt_Style,
                                 completer=MyCustomCompleter(["latest","1.0"]),
                                 complete_while_typing=True,validate_while_typing=False,
                                 validator=TagValidator("Tag not valid"),
                                 key_bindings=general_bindings,bottom_toolbar=toolbar,
                                 auto_suggest=MySuggestion(images),rprompt='<<<    Image Pull (Local Docker) ',color_depth=ColorDepth.TRUE_COLOR)

        if not image_tag or image_tag.strip() == "":
            return None, None
        
        lock             = threading.Lock()
        x_pos            = 16
        start_x_line     = x_pos
        total_status     = 25
        x_lines          = {}
        _count           = 0
        _watch_count     = 11
        _watch_index     = 0
        _margin          = "  "
        _horiz_lines     = f"{Style.GREEN}+{'-'.ljust(110,'-')}+{Style.RESET}"
        _tag             = None
        _pulling_message = None

        def increment_line():
            lock.acquire()
            nonlocal start_x_line
            try:
                start_x_line += 1
            finally:
                lock.release()
        
        def size_align(str, size):
            return str.ljust(size, " ")

        docker_client    = docker.from_env()
        # previous_status = None
        # need_break_line = False
        for p in docker_client.api.pull(image_name, tag=image_tag, stream=True, decode=True):
            _count           += 1
            _status           = p['status'] if 'status' in p else None
            _id               = p['id'] if 'id' in p else None
            _progress_details = p['progressDetail'] if 'progressDetail' in p else None
            _progress         = p['progress'] if 'progress' in p else None

            if "pulling from" in _status.lower():
                _tag             = _id
                _status_colorful = _status[:len("Pulling from")] + f"{Style.IYELLOW}" + _status[len("Pulling from"):]
                _pulling_message =   f"""{Style.IGREEN}{size_align(_id,12)}  {Style.CYAN}{_status_colorful}"""  
                
            if _status.lower() == "download complete":
                _progress = Emoticons.ok()
            elif _status.lower() == "verifying checksum":
                _progress = Emoticons.magnifier()
            elif _status.lower() == "pull complete":
                _progress = Emoticons.thumbsUp()
            
            if not _progress:
                _progress = Emoticons.waiting()

            if _id:
                if not _id in x_lines:
                    increment_line()
                    x_lines[_id]  = start_x_line
                x_line = x_lines[_id]
                
                # Print First Line Only (TAG)
                _progress_first_line_tag = f"{_pulling_message} {Emoticons.images_waiting(0, _watch_index)}                "
                if _watch_index == _watch_count:
                    _watch_index  = 0
                else:
                    _watch_index += 1
                sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x_lines[_tag], 0, f"{_margin}{_progress_first_line_tag}"))
                sys.stdout.flush()

                # Print Layers Download and Pulling, by Id, each one in its own line 
                output  = f"""{_margin}{Style.IGREEN}{size_align(_id,12)}  {Style.CYAN}{size_align(_status,20)}  {Style.IYELLOW}{_progress}{Style.GREEN}                                                                          """
                sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x_pos - 2, 0, f"{Style.IBLUE} Wait...{Style.GREEN}"))
                sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x_pos - 1, 0, _horiz_lines))
                sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x_pos, 0, " ".ljust(120," ")))
                sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x_line, 0, output))
                sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x_pos + total_status, 0, " ".ljust(120," ")))
                sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x_pos + total_status + 1, 0, _horiz_lines))
                sys.stdout.flush()
            else:
                if "Digest" in _status:
                    _progress = Emoticons.ok()
                    increment_line()
                elif "Status: Downloaded" in _status:
                    _progress = Emoticons.ok()
                    increment_line()
                    start   = _status.find("Downloaded")
                    end     = len("Downloaded")
                    _status = _status[:start] + f"{Style.IYELLOW}Downloaded{Style.CYAN}" + _status[start+end:]
                output  = f"""{_margin}{Style.IGREEN}>>{"-".ljust(9,"-") + ">"}  {Style.CYAN}{size_align(_status,20)}  {Style.IYELLOW}{_progress}{Style.GREEN}                                                                                                                  """
                sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (start_x_line, 0, output))
                sys.stdout.flush()
        
        return image_name, image_tag
    
    def docker_image_tag(self, _repository_uri, _image_name, _image_tag, ecr_client=None):
        #docker_client = self.get_docker_ecr_login(ecr_client)
        docker_client  = docker.from_env()
        return docker_client.api.tag(image=f"{_image_name}:{_image_tag}",repository=_repository_uri,tag=_image_tag)


    def list_ecr_repository(self) -> Tuple[dict, list, object]:
        ecr_client      = self.botoSession().client("ecr");
        resp_list_repos = ecr_client.describe_repositories()
        list_repos_dict = {}
        list_repos      = []
        for rep in resp_list_repos['repositories']:
            short_name = rep['repositoryArn'][rep['repositoryArn'].rfind(':repository/')+len(':repository/'):]
            list_repos_dict[short_name] = {
                'name': rep['repositoryName'],
                'uri': rep['repositoryUri'],
                'arn':rep['repositoryArn'],
                'short_name': short_name
            }
            list_repos.append(short_name)
        list_repos.sort()
        return list_repos_dict, list_repos, ecr_client

    def get_docker_ecr_login(self, ecr_client=None) -> object:
        if ecr_client == None:
            ecr_client  = self.botoSession().client("ecr");

        docker_client      = docker.from_env()
        token              = ecr_client.get_authorization_token()
        username, password = base64.b64decode(token['authorizationData'][0]['authorizationToken']).decode().split(':')
        registry           = token['authorizationData'][0]['proxyEndpoint']
        docker_client.login(username, password, registry=registry)
        return docker_client

    def create_ecr_repository(self, name, ecr_client=None) -> object:
        if ecr_client == None:
            ecr_client  = self.botoSession().client("ecr");
        
        new_repository = ecr_client.create_repository(
            repositoryName=name,
            imageTagMutability='IMMUTABLE',
            imageScanningConfiguration={'scanOnPush': True}
        )
        return new_repository
    
    def get_ecr_auth_config(self, ecr_client=None):
        if ecr_client == None:
            ecr_client  = self.botoSession().client("ecr");

        token              = ecr_client.get_authorization_token()
        username, password = base64.b64decode(token['authorizationData'][0]['authorizationToken']).decode().split(':')
        registry           = token['authorizationData'][0]['proxyEndpoint']
        auth_config = {'username': username, 'password': password}
        return auth_config

    def _clean_lines(self, x_pos):
        _from = x_pos + 5
        _to   = x_pos + 27
        for k in range(_from, _to):
            sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (k, 0, " ".ljust(120," ")))

    def docker_push_image(self, repository_uri, image_name, image_tag, ecr_client=None):
        if ecr_client == None:
            ecr_client  = self.botoSession().client("ecr");

        lock             = threading.Lock()
        x_pos            = 16
        start_x_line     = x_pos
        total_status     = 25
        x_lines          = {}
        _count           = 0
        _watch_count     = 11
        _watch_index     = 0
        _margin          = "  "
        _horiz_lines     = f"{Style.GREEN}+{'-'.ljust(110,'-')}+{Style.RESET}"
        _tag             = None
        _pushing_message = None

        def increment_line():
            lock.acquire()
            nonlocal start_x_line
            try:
                start_x_line += 1
            finally:
                lock.release()
        
        def size_align(str, size):
            return str.ljust(size, " ")

        self._clean_lines(x_pos)

        docker_client    = docker.from_env()
        auth_config      = self.get_ecr_auth_config(ecr_client=ecr_client)

        for p in docker_client.api.push(repository_uri, tag=image_tag, stream=True, decode=True, auth_config=auth_config):

            _count           += 1
            _status           = p['status'] if 'status' in p else None
            _id               = p['id'] if 'id' in p else None
            _progress_details = p['progressDetail'] if 'progressDetail' in p else None
            _progress         = p['progress'] if 'progress' in p else None

            # with open(f"push_image_{image_name.replace('/','_')}_{image_tag}.json","a") as f:
            #     f.write(str(p) + ",\n")

            if _status:
                if "the push refers" in _status.lower():
                    _tag             = "first_line"
                    _id              = "first_line"
                    _pushing_message =   f"""{Style.IGREEN}{Style.CYAN}{_status}"""  
                    
                if _status.lower() == "layer already exists":
                    _progress = Emoticons.ok()
                elif _status.lower() == "waiting":
                    _progress = Emoticons.waiting()
                elif _status.lower() == "preparing":
                    _progress = Emoticons.waitDistract()
                elif _status.lower() == "pushed":
                    _progress = Emoticons.thumbsUp()
                
                if not _progress:
                    _progress = ""
    
                if _id:
                    if not _id in x_lines:
                        increment_line()
                        x_lines[_id]  = start_x_line
                    x_line = x_lines[_id]
                    
                    # Print First Line Only (TAG)
                    _progress_first_line_tag = f"{_pushing_message} {Emoticons.images_waiting(0, _watch_index)}                                                                                                                                                                    "
                    if _watch_index == _watch_count:
                        _watch_index  = 0
                    else:
                        _watch_index += 1
                    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x_lines[_tag], 0, f"{_margin}{_progress_first_line_tag}"))
                    sys.stdout.flush()
    
                    # Print Layers Download and Pulling, by Id, each one in its own line 
                    output  = f"""{_margin}{Style.IGREEN}{size_align(_id,12)}  {Style.CYAN}{size_align(_status,20)}  {Style.IYELLOW}{_progress}{Style.GREEN}                                                                                                                        """
                    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x_pos - 2, 0, f"{Style.IBLUE} Wait...{Style.GREEN}"))
                    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x_pos - 1, 0, _horiz_lines))
                    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x_pos, 0, " ".ljust(120," ")))
                    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x_line, 0, output))
                    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x_pos + total_status, 0, " ".ljust(120," ")))
                    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x_pos + total_status + 1, 0, _horiz_lines))
                    sys.stdout.flush()
                else:
                    if "Digest" in _status:
                        _progress = Emoticons.ok()
                        increment_line()
                    elif "Status: Downloaded" in _status:
                        _progress = Emoticons.ok()
                    output  = f"""{_margin}{Style.IGREEN}>>{"-".ljust(9,"-") + ">"}  {Style.CYAN}{size_align(_status,20)}  {Style.IYELLOW}{_progress}{Style.GREEN}                                                                                                                  """
                    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (start_x_line, 0, output))
                    sys.stdout.flush()
            else:
                # _status is None
                pass
    
    def workflow_docker_pull_ecr(self):
        # List of Repositories
        Utils.clearScreen()
        list_repos_dict, list_repos, ecr_client = self.list_ecr_repository()

        self.print_credentials()

        # Pick up a ECR Repository
        message               = [('class:green', f' Create a new ECR Repository at AWS Account '),('class:green2',{self.aws_account}),('class:green',' [y/n]...? ')]
        session               = PromptSession()
        toolbar               = Prompt_HTML(f'{toolbar_margin}{toolbar_default}')
        resp_create_new_repo  = session.prompt(message,style=Prompt_Style,
                                 completer=MyCustomCompleter(["Y","N"]),
                                 complete_while_typing=True,validate_while_typing=False,
                                 validator=MyValidator(["Y","N","y","n"],"not valid answer, must be \"y\" or \"n\"..."),
                                 key_bindings=general_bindings,bottom_toolbar=toolbar,
                                 auto_suggest=MySuggestion(["Y","N"]),rprompt='<<<    Create New Repository ',color_depth=ColorDepth.TRUE_COLOR)
        if not resp_create_new_repo or resp_create_new_repo.strip() == "":
            return
        
        repository = None
        if resp_create_new_repo.lower() != "y":
            message           = [('class:green', f' Choose the ECR Repository from the list '),('class:green2',' <TAB> or Type it'),('class:green','.......: ')]
            session           = PromptSession()
            toolbar           = Prompt_HTML(f'{toolbar_margin}{toolbar_default}')
            chosen_repository = session.prompt(message,style=Prompt_Style,
                                    completer=MyCustomCompleter(list_repos),
                                    complete_while_typing=True,validate_while_typing=False,
                                    #validator=MyValidator(list_repos,"ECR Reposiroty not found in the list"),
                                    key_bindings=general_bindings,bottom_toolbar=toolbar,
                                    auto_suggest=MySuggestion(["Y","N"]),rprompt='<<<    Choose ECR Repository ',color_depth=ColorDepth.TRUE_COLOR)
            if not chosen_repository or chosen_repository.strip() == "":
                return
            repository = chosen_repository
        else:
            message              = [('class:green', f' Type the name of the new ECR Repository '),('class:green','........................: ')]
            session              = PromptSession()
            toolbar              = Prompt_HTML(f'{toolbar_margin}{toolbar_default}')
            new_repository_name  = session.prompt(message,style=Prompt_Style,
                                    #completer=MyCustomCompleter(list_repos),
                                    complete_while_typing=True,validate_while_typing=False,
                                    validator=RepositoryNameValidator("ECR Reposiroty not found in the list"),
                                    key_bindings=general_bindings,bottom_toolbar=toolbar,
                                    auto_suggest=MySuggestion(["Y","N"]),rprompt='<<<    New ECR Repository ',color_depth=ColorDepth.TRUE_COLOR)
            if not new_repository_name or new_repository_name.strip() == "":
                return
            try:
                new_repository = self.create_ecr_repository(new_repository_name, ecr_client=ecr_client)
                new_repo_dict  = new_repository['repository']
                short_name     = new_repo_dict['repositoryArn'][new_repo_dict['repositoryArn'].rfind(':repository/')+len(':repository/'):]
                list_repos_dict[short_name] = {
                    'name': new_repo_dict['repositoryName'],
                    'uri': new_repo_dict['repositoryUri'],
                    'arn':new_repo_dict['repositoryArn'],
                    'short_name': short_name
                }
            except ClientError as e:
                if "RepositoryAlreadyExistsException" in str(e):
                    short_name = new_repository_name
                    #Messages.showWarning(f"Repository \"{Style.IBLUE}{short_name}{Style.GREEN}\" already exists!")
                else:
                    raise e
            list_repos.append(short_name)
            repository = short_name

        image_name, image_tag   = self.docker_pull_image([repository])
        if not image_tag or image_tag.strip() == "":
            return
        
        repository_uri = list_repos_dict[repository]['uri']
        if self.docker_image_tag(f"{repository_uri}:{image_tag}", image_name, image_tag, ecr_client=ecr_client):
           print(f"{Style.GREEN} {Emoticons.ok()} Image Tagged: {Style.IBLUE}{repository_uri}:{image_tag}{Style.GREEN}, ready to push to ECR AWS Account {Style.IYELLOW}{self.aws_account}{Style.GREEN}!")

        self.docker_push_image(repository_uri, image_name, image_tag, ecr_client=ecr_client)
        print(f"{Style.GREEN} {Emoticons.ok()} Image Pushed: {Style.IBLUE}{repository_uri}:{image_tag}{Style.GREEN}, to ECR AWS Account {Style.IYELLOW}{self.aws_account}{Style.GREEN}!")
        print(f" {Emoticons.thumbsUp()}\n\n                                                                             ")

    def get_current_aws_session(self):
        try:
            callerIdentity = self.botoSession()  \
                                  .client('sts').get_caller_identity()
            return callerIdentity
        except ClientError as e:
            if e.response['Error']['Code'] == "AccessDenied":
                msg = e.response['Error']['Message']
                Messages.showError("Access Denied!",f"{msg}")
                return None
            elif e.response['Error']['Code'] == "InvalidClientTokenId":
                msg = e.response['Error']['Message']
                Messages.showError("The security token included in the request is invalid! Clean your session and try again",f"{msg}")
                return None
            else:
                print(e.response['Error']['Code'])
                raise e

    def print_credentials(self):
        credentials = self.get_current_aws_session()
        Messages.showMessage("CURRENT AWS SESSION",f"""
    {Style.GREEN}User Id.......: {Style.IBLUE}{credentials['UserId']}{Style.RESET}
    {Style.GREEN}Account.......: {Style.IBLUE}{credentials['Account']}{Style.RESET}
    {Style.GREEN}Arn...........: {Style.IBLUE}{credentials['Arn']}{Style.RESET}
""")
# {Style.IGREEN}The ECR repository will be create at this AWS Account: {Style.IBLUE}{credentials['Account']}{Style.GREEN}



def test_print_specific_line():
    lock         = threading.Lock()
    x_pos        = 19
    start_x_line = x_pos
    total_status = 9
    x_lines      = {}
    _count       = 0
    _watch_count = 11
    _watch_index = 0
    _margin      = "  "
    _horiz_lines = f"{Style.GREEN}+{'-'.ljust(110,'-')}+{Style.RESET}"

    def increment_line():
        lock.acquire()
        nonlocal start_x_line
        try:
            start_x_line += 1
        finally:
            lock.release()
    
    def size_align(str, size):
        return str.ljust(size, "-")
    
    with open('sample.json') as json_file:
        data             = json.load(json_file)
        _tag             = None
        _pulling_message = None
        for p in data:
            _count           += 1
            _status           = p['status'] if 'status' in p else None
            _id               = p['id'] if 'id' in p else None
            _progress_details = p['progressDetail'] if 'progressDetail' in p else None
            _progress         = p['progress'] if 'progress' in p else None

            if "pulling from" in _status.lower():
                _tag             = _id
                _status_colorful = _status[:len("Pulling from")] + f"{Style.IYELLOW}" + _status[len("Pulling from"):]
                _pulling_message =   f"""{Style.IGREEN}{size_align(_id,12)}  {Style.CYAN}{_status_colorful}"""  
                
            if _status.lower() == "download complete":
                _progress = Emoticons.ok()
            elif _status.lower() == "verifying checksum":
                _progress = Emoticons.magnifier()
            elif _status.lower() == "pull complete":
                _progress = Emoticons.thumbsUp()
            
            if not _progress:
                _progress = Emoticons.waiting()

            if _id:
                if not _id in x_lines:
                    increment_line()
                    x_lines[_id]  = start_x_line
                x_line = x_lines[_id]
                
                # Print First Line Only (TAG)
                _progress_first_line_tag = f"{_pulling_message} {Emoticons.images_waiting(0, _watch_index)}                "
                if _watch_index == _watch_count:
                    _watch_index  = 0
                else:
                    _watch_index += 1
                sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x_lines[_tag], 0, f"{_margin}{_progress_first_line_tag}"))
                sys.stdout.flush()

                # Print Layers Download and Pulling, by Id, each one in its own line 
                output  = f"""{_margin}{Style.IGREEN}{size_align(_id,12)}  {Style.CYAN}{size_align(_status,20)}  {Style.IYELLOW}{_progress}{Style.GREEN}                                                                          """
                sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x_pos - 1, 0, _horiz_lines))
                sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x_pos, 0, " ".ljust(120," ")))
                sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x_line, 0, output))
                sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x_pos + total_status, 0, " ".ljust(120," ")))
                sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x_pos + total_status + 1, 0, _horiz_lines))
                sys.stdout.flush()
            else:
                if "Digest" in _status:
                    _progress = Emoticons.thumbsUp()
                    increment_line()
                elif "Status: Downloaded" in _status:
                    _progress = Emoticons.thumbsUp()
                    increment_line()
                    start   = _status.find("Downloaded")
                    end     = len("Downloaded")
                    _status = _status[:start] + f"{Style.IYELLOW}Downloaded{Style.CYAN}" + _status[start+end:]
                output  = f"""{_margin}{Style.IGREEN}>>{"-".ljust(9,"-") + ">"}  {Style.CYAN}{size_align(_status,20)}  {Style.IYELLOW}{_progress}{Style.GREEN}                                                                                                                  """
                sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (start_x_line, 0, output))
                sys.stdout.flush()
                
            time.sleep(0.05)
    time.sleep(5)
    print(x_lines)

def main():
    #test_print_specific_line()
    """Start PyEcr"""
    try:
        pyecr = PyEcr()
        #pyecr.docker_pull_image()
        #pyecr.create_ecr_repository()
        pyecr.workflow_docker_pull_ecr()
    except KeyboardInterrupt:
        pass    

if __name__ == "__main__":
    main()