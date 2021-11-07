#! python3
# -*- encoding: utf-8 -*-

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class WaitUntil(object):
    def __init__(self):
        self._until_find = UntilFind(self)
        self._until_switch = UntilSwitch(self)

    @property
    def until_find(self):
        """
        :Returns:
            - UntilFind: an object containing all options for dynamically waiting and finding elements.

        :Usage:
            element = driver.until_find.element_by_id('#username')
            element.send_keys("admin")
        """
        return self._until_find

    @property
    def until_switch(self):
        """
        :Returns:
            - UntilSwitch: an object containing all options for dynamically waiting and switch locator.

        :Usage:
            driver.until_switch.to_window(-1)
        """
        return self._until_switch


class UntilFind(object):
    LOC = (By.CLASS_NAME, By.CSS_SELECTOR, By.ID, By.LINK_TEXT, By.NAME, By.PARTIAL_LINK_TEXT, By.TAG_NAME, By.XPATH)

    def __init__(self, driver):
        """
            element_by_xxx： only return one element
            elements_by_xxx:  only return the specified index element, default index=0
        """
        self._driver = driver
        self.element_by_class_name = self._element(By.CLASS_NAME)
        self.element_by_css_selector = self._element(By.CSS_SELECTOR)
        self.element_by_id = self._element(By.ID)
        self.element_by_link_text = self._element(By.LINK_TEXT)
        self.element_by_name = self._element(By.NAME)
        self.element_by_partial_link_text = self._element(By.PARTIAL_LINK_TEXT)
        self.element_by_tag_name = self._element(By.TAG_NAME)
        self.element_by_xpath = self._element(By.XPATH)

        self.elements_by_class_name = self._elements(By.CLASS_NAME)
        self.elements_by_css_selector = self._elements(By.CSS_SELECTOR)
        self.elements_by_id = self._elements(By.ID)
        self.elements_by_link_text = self._elements(By.LINK_TEXT)
        self.elements_by_name = self._elements(By.NAME)
        self.elements_by_partial_link_text = self._elements(By.PARTIAL_LINK_TEXT)
        self.elements_by_tag_name = self._elements(By.TAG_NAME)
        self.elements_by_xpath = self._elements(By.XPATH)

    def _element(self, by):
        if by not in self.LOC:
            raise Exception("unknown location {0}, should be {1}".format(by, self.LOC))

        def by_func(value, timeout=10, wait_displayed=False):
            try:
                if wait_displayed:
                    elm = WebDriverWait(self._driver, timeout).until(
                        lambda dr: dr.find_element(by, value) if dr.find_element(by, value).is_displayed() else None
                    )
                else:
                    elm = WebDriverWait(self._driver, timeout).until(
                        lambda dr: dr.find_element(by, value)
                    )
            except AttributeError as err:
                print("Web driver is not define.")
                raise err
            except Exception as err:
                print("Warning: Not found element(timeout: {0}, by: {1}, value: {2})".format(timeout, by, value))
                raise err

            return elm

        return by_func

    def _elements(self, by):
        if by not in self.LOC:
            raise Exception("unknown location {0}, should be {1}".format(by, self.LOC))

        def by_func(value, index=0, timeout=10):
            try:
                elms = WebDriverWait(self._driver, timeout).until(
                    lambda dr: dr.find_elements(by, value)
                )
            except AttributeError as err:
                print("Web driver is not define.")
                raise err
            except Exception as err:
                print("Warning: Not found element(timeout: {0}, by: {1}, value: {2})".format(timeout, by, value))
                raise err

            return elms[index]

        return by_func


class UntilSwitch(object):
    LOC = ("window", "frame")

    def __init__(self, driver):
        """
            switch_to_xxx： windows and iframe always load slowly, you can use these methods.
        """
        self._driver = driver
        self.to_window = self._switch_to("window")
        self.to_frame = self._switch_to("frame")

    def _switch_to(self, target):
        if target not in self.LOC:
            raise Exception("unknown target locator {}".format(target))

        def _target(index, timeout=10):
            if target == "window":
                win_handle = WebDriverWait(self._driver, timeout, ignored_exceptions=IndexError).until(
                    method=lambda dr: dr.window_handles[index] if dr.window_handles[index] else None,
                    message="Not found window(index: {0}, timeout: {1})".format(index, timeout)
                )
                self._driver.switch_to.window(win_handle)
            else:
                WebDriverWait(self._driver, timeout, ignored_exceptions=IndexError).until(
                    method=lambda dr: True if dr.find_elements_by_tag_name("iframe")[index] else None,
                    message="Not found iframe(index: {0}, timeout: {1})".format(index, timeout)
                )
                self._driver.switch_to.frame(index)

        return _target
