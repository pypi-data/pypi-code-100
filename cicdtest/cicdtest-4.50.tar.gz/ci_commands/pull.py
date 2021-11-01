"""
    Title: pull.py
    Author: Kushagra A.
    Language: Python
    Date Created: 31-08-2021
    Date Modified: 23-09-2021
    Description:
        ###############################################################
        ## Check for pull operation on a repository   ## 
         ###############################################################
 """

from buildpan.previous_commit import prev_commit
import requests, asyncio
from buildpan import setting, workflow, repo_pull, find_path
import click
from aiohttp import ClientSession, ClientResponseError


info = setting.info


# getting env variable
push_commit = info["PUSH_COMMIT_URL"]


@click.command()
def pull():
    '''
     For manually trigger  pull operation

    \f
    '''

    all_repo_name = []
    try:
        find_path.find_path()
        file_path = find_path.find_path.file_path

        #reading data from centralized file
        with open(file_path + "/info.txt") as file:
            info = file.readlines()
            for data in info:
                d = eval(data)
                repo_name = d["repo_name"]
                repo_name = "repo_name="+repo_name.lower()
                all_repo_name.append(repo_name)
        
        async def fetch(session, url):
            try:
                async with session.get(url) as response:
                    res = await response.read()
                    res=str(res)
                    index=res.index("'")
                    index1=res.index("'",index+1)
                    res=res[index+1:index1]

                    with open(file_path + "/info.txt") as file:
                        info = file.readlines()
                        for data in info:
                            d = eval(data)
                            repo_name = d["repo_name"].lower()

                            if repo_name == res:
                                path = d["path"]
                                project_id = d["project_id"]
                                username = d["username"]
                                provider = d["provider"]
                                # doing pull operation
                                repo_pull.repo_pull(path, project_id, repo_name, username, provider)
                                # if pull success calling deployment        
                                response = workflow.workflows(path, project_id, repo_name, username)
                                # if deployment fails go to previous commit
                                if response == False:
                                    prev_commit(path, repo_name, project_id, username, provider)
                        
            except ClientResponseError as e:
                print("e = ", e)
            except asyncio.TimeoutError:
                print("t out")
            except Exception as e:
                print("exc = ", e)
            else:
                return res
            return
        

        async def fetch_async(loop, repo):
            repo_name = str(repo)

            # using pooling for pull operation
            url = push_commit+"?"+repo_name.lower()
            tasks = []
            # try to use one client session
            async with ClientSession() as session:
                task = asyncio.ensure_future(fetch(session, url))
                tasks.append(task)

                await asyncio.gather(*tasks)
            return 
        

        for repo in all_repo_name:
            loop = asyncio.get_event_loop()
            future = asyncio.ensure_future(fetch_async(loop, repo))
            loop.run_until_complete(future)
            future.result()

    
    except Exception as e:
        print("No CI-CD operation is running.")



