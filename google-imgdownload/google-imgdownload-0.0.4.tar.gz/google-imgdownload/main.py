# my new image dataset from google
from selenium import webdriver
import time
import urllib.request
import os
from selenium.webdriver.common.keys import Keys
def googleimage(keyword):
    if not os.path.exists('D:\\tech'):
        os.mkdir('D:\\tech')
    os.chdir('D:\\tech')

    chromedriver_location='D:\\myweb\\chromedriver'
    browser = webdriver.Chrome(chromedriver_location) #incase you are chrome
    browser.get('https://www.google.co.in/')
    search = browser.find_element_by_name('q')
#     keywords=input('enter keyword to search')
    search.send_keys(keyword,Keys.ENTER)
    elem = browser.find_element_by_link_text('Images')
    elem.get_attribute('href')
    elem.click()
    value = 0
    for i in range(20):
       browser.execute_script('scrollBy('+ str(value) +',+1000);')
       value += 1000
       time.sleep(3)
    elem1 = browser.find_element_by_id('islmp')
    sub = elem1.find_elements_by_tag_name('img')
    try:
        if not os.path.exists('D:\\tech'):
            os.mkdir('D:\\tech')
        else:
            print(os.path.exists('D:\\tech'))
        os.mkdir(f'{keyword}')
    except FileExistsError:
        pass
    count = 0

    for i in sub:
        src = i.get_attribute('src')
        try:
            if src != None:
                src  = str(src)
                print(src)
                count+=1
#             os.chdir('downloads')
                urllib.request.urlretrieve(src, os.path.join(f'{keyword}','image'+str(count)+'.jpg'))
            else:
                raise TypeError
        except TypeError:
            print('fail')