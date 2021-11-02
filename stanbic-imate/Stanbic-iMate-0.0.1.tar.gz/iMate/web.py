from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC


class WebAutomate:
    def __init__(self, wait_time):
        self.wait = wait_time

    def drop_down_by_name(self, element_name, value):
        """Selects Dropdown by Element Value Using Element Name"""
        select = Select(self.wait.until(EC.element_to_be_clickable((By.NAME, element_name))))
        select.select_by_value(value)

    def drop_down_by_text(self, element_id, text):
        """Selects Dropdown by Visible Text Using Element ID"""
        select = Select(self.wait.until(EC.element_to_be_clickable((By.ID, element_id))))
        select.select_by_visible_text(text.title())

    def drop_down_by_text_name(self, element_name, text):
        """Selects Dropdown by Visible Text Using Element Name"""
        select = Select(self.wait.until(EC.element_to_be_clickable((By.NAME, element_name))))
        select.select_by_visible_text(text.title())

    def drop_down_by_id(self, element_id, value):
        """Selects Dropdown by Element Value Using Element ID"""
        select = Select(self.wait.until(EC.element_to_be_clickable((By.ID, element_id))))
        select.select_by_value(value)

    def select_date(self, browser_instance, element_id, date):
        """Selects date from Calender"""
        date_element = self.wait.until(EC.element_to_be_clickable((By.ID, element_id)))
        browser_instance.execute_script(f"arguments[0].value = '{date}';", date_element)

    def get_element_value(self, element_name):
        """Get the value of an element"""
        return self.wait.until(EC.element_to_be_clickable((By.NAME, element_name))).get_attribute("value")

    def click_element_by_css(self, selector):
        """Click Element by CSS Selector"""
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()

    def click_element_by_xpath(self, xpath):
        """Click Element by XPATH"""
        self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

    def click_element_by_id(self, element_id):
        """Click Element by ID"""
        self.wait.until(EC.element_to_be_clickable((By.ID, element_id))).click()

    def click_element_by_name(self, element_name):
        """Click Element by Name"""
        self.wait.until(EC.element_to_be_clickable((By.ID, element_name))).click()

