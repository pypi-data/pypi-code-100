"""
    Title: create_file.py
    Author: Kushagra A.
    Language: Python
    Date Created: 11-09-2021
    Date Modified: 23-09-2021
    Description:
        ###############################################################
        ## Create a file on a specified path   ## 
         ###############################################################
 """

from buildpan import find_path

def create_file(project_id, repo_name, path, username, provider):
    try:
        find_path.find_path()
        file_path = find_path.find_path.file_path

        all_project_id = []

        with open(f"{file_path}/info.txt", "a") as file:
            file.write("")
            file.close()

        dict = {
                "project_id": project_id,
                "repo_name": repo_name,
                "path": str(path),
                "username": username,
                "provider": provider
        }
        
        with open(f"{file_path}/info.txt", "r+") as file:
            info = file.readlines()
            for item in info:
                data = eval(item)
                all_project_id.append(data["project_id"])
        
        if project_id in all_project_id:
            print("repository already initiated")
        else:
            with open(f"{file_path}/info.txt", "a") as file:
                file.write(str(dict) + "\n")
    
    except Exception as e:
        print(e)
