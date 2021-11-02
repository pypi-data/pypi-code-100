import json,requests as r
class Colors: fail = '\033[91m' ; good = '\033[92m' ; end = '\033[0m'

class TwitterPlus:
    def __init__(this,apiKey:str='',apiSecretKey:str='',apiToken:str='',apiSecretToken:str='',apiBearerToken:str=''):
        # check what variables are given
        if apiKey:this.key=apiKey
        else:this.key=False
        if apiSecretKey:this.secretKey=apiSecretKey
        else:this.secretKey=False
        if apiToken:this.token=apiToken
        else:this.token=False
        if apiSecretToken:this.secretToken=apiSecretToken
        else:this.secretToken=False
        if apiBearerToken:this.bearerToken=apiBearerToken
        else:this.bearerToken=False
        this.BASE_URL = 'https://api.twitter.com/2/'

    def getUserId(this,userName:str):
        apiResp = r.get(f'{this.BASE_URL}users/by?usernames={userName}&tweet.fields=author_id',headers=this.__auth(0)).json()
        if 'data' not in apiResp: print(f'{Colors.fail}{str(apiResp)}{Colors.end}') ; return False
        else: return apiResp['data'][0]['id']

    def timeline(this,username:str,max_results:int=100):
        userId = this.getUserId(username)
        params = {"tweet.fields": "created_at" ,'max_results':max_results}
        url = f"{this.BASE_URL}users/{userId}/tweets"
        apiResp = r.get(url,params=params,headers=this.__auth(1)).json()
        if 'data' not in apiResp: print(f'{Colors.fail}{str(apiResp)}{Colors.end}') ; return False
        else: return apiResp

    def __pretty(this,data): return json.dumps(data,indent=3)

    def __auth(this,userAgentNum:int):
        if not this.bearerToken:print(f'{Colors.fail}bearer token can not be empty{Colors.end}') ; return False
        userAgent=['v2UserLookupPython','v2UserTweetsPython']
        return {
            'Authorization':'Bearer '+this.bearerToken,
            'User-Agent':userAgent[userAgentNum]
        }