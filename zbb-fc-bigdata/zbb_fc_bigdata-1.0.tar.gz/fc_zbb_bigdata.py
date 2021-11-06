from bs4 import BeautifulSoup
import requests
import time

url = "http://news.baidu.com/"
r = requests.get(url)
html = r.text
soup = BeautifulSoup(html, 'html.parser')
ul_items = soup.find_all('ul', class_="ulist focuslistnews")
print(ul_items)
for ul in ul_items:
    # 取出title , 链接
    if ul.find('a'):
        a_title = ul.find('a').text
        a_href = ul.find('a').attrs['href']

        # 获取当前时间
        now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        with open('news' + now + '.txt', 'w', encoding='utf-8') as file:
            file.write("焦点新闻: " + a_title + "\n")
            file.write("点击查看详情: " + a_href + "\n")
    else:
        pass
        