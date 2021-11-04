from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

import time


def find_elements_by_text(driver, text, tag_name=''):
    elements = []
    if len(tag_name) > 0:
        elements = driver.find_elements_by_xpath(
            "//{tag_name}//*[text()='{text}']|//{tag_name}//*[@value='{text}']|//{tag_name}//*[@placeholder='{text}']".format(
                tag_name=tag_name, text=text))
    else:
        elements = driver.find_elements_by_xpath(
            "//*[text()='{0}']|//*[@value='{0}']|//*[@placeholder='{0}']".format(text))
    return elements


class WaitVisibilityLambda:
    def __init__(self, text, tag_name):
        self._text = text
        self._tag_name = tag_name

    def __call__(self, driver):
        elements = find_elements_by_text(driver, self._text, self._tag_name)
        if not elements or len(elements) == 0:
            return False
        else:
            if is_spinner_display(driver):
                return False
            return True


def find_element(driver, text, anchor_type='', tag_name=''):
    print('find_element start: ' + time.asctime(time.localtime(time.time())))
    wait = WebDriverWait(driver, 20, 0.5)
    result = wait.until(WaitVisibilityLambda(text, tag_name))
    print('find_element after awit element: ' + time.asctime(time.localtime(time.time())))

    elements = find_elements_by_text(driver, text, tag_name)
    print('find_element elements: ' + time.asctime(time.localtime(time.time())))
    # print(elements),
    if not elements or len(elements) == 0:
        return None

    max_probability_element = elements[0]
    if not anchor_type:
        return max_probability_element
    for element in elements:
        location = element.location
        print('element {0} location {1}'.format(element.text, location))
        if '左' in anchor_type:
            max_probabilty_location = max_probability_element.location
            if max_probabilty_location['x'] > location['x']:
                max_probability_element = element
        if '右' in anchor_type:
            max_probabilty_location = max_probability_element.location
            if max_probabilty_location['x'] < location['x']:
                max_probability_element = element
        if '上' in anchor_type:
            max_probabilty_location = max_probability_element.location
            if max_probabilty_location['y'] > location['y']:
                max_probability_element = element
        if '下' in anchor_type:
            max_probabilty_location = max_probability_element.location
            if max_probabilty_location['y'] < location['y']:
                max_probability_element = element

    return max_probability_element


# 查找最合适的element
# 算法：在mc_select之下 最接近的
# mc_select_input[1].send_keys(Keys.RETURN)
def find_max_probability_element(elements, anchor_element, anchor_type=''):
    max_probability_element = None
    anchor_location = anchor_element.location
    for element in elements:
        location = element.location
        if location['x'] >= anchor_location['x'] and location['y'] > anchor_location['y']:
            return element
    return max_probability_element


def click_element(web_driver, text, anchor_type=''):
    web_driver.implicitly_wait(1)  # seconds
    element = find_element(web_driver, text, anchor_type)
    if element:
        try:
            element.click()
        except WebDriverException:
            location = element.location
            print("Element {} {} is not clickable, so use mouse click on: {}".format(element.tag_name, text, location))
            actions = ActionChains(web_driver)  # initialize ActionChain object
            actions.move_by_offset(location['x'] + 5, location['y'] + 5)
            actions.click()
            actions.perform()
    else:
        pass  # 抛出异常


def login(web_driver, username, password, env='test'):
    if env == 'test':
        web_driver.get('https://test.salesforce.com/login.jsp?pw={1}&un={0}'.format(username, password))
        click_element(web_driver, 'Continue')
    else:  # 其他环境的okta登录处理
        pass


def open_url(driver, url):
    driver.implicitly_wait(2)
    driver.get(url)


def set_value(web_driver, label_text, value, anchor_type=''):
    label_element = find_element(web_driver, label_text, anchor_type)
    print('set_value label element:{0}'.format(label_element.location))
    if label_element:
        if 'select' in anchor_type:  # 下拉选项
            select_input_elements = find_elements_by_text(web_driver, 'Search...')
            print('input elements count: {0}'.format(len(select_input_elements)))
            select_input_element = find_max_probability_element(select_input_elements, label_element)
            print('found select input elemnt: {0}'.format(select_input_element.location))
            select_input_element.send_keys(Keys.RETURN)
            click_element(web_driver, value, '')
        if 'lookup' in anchor_type:  # lookup
            select_input_elements = find_elements_by_text(web_driver, 'Search...')
            print('input elements count: {0}'.format(len(select_input_elements)))
            select_input_element = find_max_probability_element(select_input_elements, label_element)
            print('found select input elemnt: {0}'.format(select_input_element.location))
            select_input_element.click()
            web_driver.implicitly_wait(2)
            active_element = web_driver.switch_to.active_element
            active_element.send_keys(value)
            active_element.send_keys(Keys.RETURN)
            click_element(web_driver, value)
            click_element(web_driver, '确定')
        else:  # 默认找input或 textarea元素 进行录入
            parent = label_element.find_element_by_xpath("..")
            input_elements = parent.find_elements_by_xpath("//input|//textarea")
            input_element = find_max_probability_element(input_elements, label_element, '下')
            input_element.send_keys(value)


def is_spinner_display(driver):
    spinner_elements = driver.find_elements_by_xpath("//lightning-spinner")
    for spinner_element in spinner_elements:
        if spinner_element.is_displayed():
            return True
    return False;


class WaitTableVisibilityLambda:
    def __init__(self, match):
        self._match = match

    def __call__(self, driver):
        tables = pd.read_html(driver.page_source, match=self._match)
        if len(tables) > 0:
            if is_spinner_display(driver):  # 有loading
                return False
            return True
        else:
            return False


def get_table_data(driver, column_names=[], table_index=0):
    driver.implicitly_wait(1)  # seconds
    element = find_element(driver, column_names[0], tag_name='table')
    assert element is not None, 'can not find table element'

    wait = WebDriverWait(driver, 20, 0.5)
    result = wait.until(WaitTableVisibilityLambda(column_names[0]))
    print(result)

    match_str = '|'.join(column_names)
    tables = pd.read_html(driver.page_source, match=match_str)
    assert len(tables) == 1, 'table match error: ' + match_str
    html_table_pd = tables[table_index][column_names]
    return html_table_pd


# expect_result 为True 表示希望table和record的值匹配，为False表示table需要还没有对应的record行
def check_table_value(driver, record, expect_result=True, row_index=0, table_match=None):
    column_names = []
    for name, value in record.items():
        column_names.append(name)

    driver.implicitly_wait(1)  # seconds

    element = find_element(driver, column_names[0], tag_name='table')
    assert element is not None, 'can not find table element'

    if expect_result:
        wait = WebDriverWait(driver, 20, 0.5)
        result = wait.until(WaitTableVisibilityLambda(record[column_names[0]]))
        print(result)

    match_str = '|'.join(column_names) if not table_match else '.+'
    tables = pd.read_html(driver.page_source, match=match_str)
    assert len(tables) == 1, 'table match error: ' + match_str
    error_msg = 'no row data match with row_index: {}'.format(row_index)
    html_table_pd = tables[0][column_names]
    is_match = True
    if len(html_table_pd) > row_index:
        html_table_row = html_table_pd.iloc[row_index, :]
        print(html_table_row)
        if len(html_table_row) > 0:
            for name in column_names:
                if html_table_row[name] != record[name]:
                    is_match = False
                    error_msg = "Chcek {name} error: expect value is {expect_value}, current value is {current_value}" \
                        .format(name=name, expect_value=record[name], current_value=html_table_row[name])
                    break
        else:
            is_match = False
    else:
        is_match = False

    if expect_result:
        assert is_match, error_msg
    else:
        assert not is_match, 'value exist'