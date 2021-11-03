import requests

def up(url):
    print(f"您请求的链接是{url}")
    resp = requests.get(url)
    status = resp.status_code
    if status == 200:
        print("请求成功,奖励一朵小红花")
    else:
        print("失败了,随缘吧...")
