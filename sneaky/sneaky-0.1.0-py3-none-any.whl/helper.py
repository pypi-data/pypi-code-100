from undetected_chromedriver.v2 import Chrome as _Chrome
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from html import escape, unescape
from lxml import html, etree
from scipy import interpolate
import numpy as np
from typing import List
import random
import math
import time


class Chrome(_Chrome):
    cursor_pos = [0, 0]

    @staticmethod
    def is_xpath(s):
        return s[0] in [".", "/"]

    def exist(self, path_or_selector):
        try:
            if self.is_xpath(path_or_selector):
                self.find_element(By.XPATH, path_or_selector)
            else:
                self.find_element(By.CSS_SELECTOR, path_or_selector)
            return True
        except:
            return False

    def expand_shadow_dom(self, element) -> WebElement:
        return self.execute_script("return arguments[0].shadowRoot", element)

    def xpath(self, xpath) -> List[WebElement]:
        return WebDriverWait(self, 5).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

    def querySelectorAll(self, selector) -> List[WebElement]:
        return WebDriverWait(self, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))

    def move_by_offset(self, x, y, delay: int = 250):
        x = int(x)
        y = int(y)
        self.cursor_pos[0] += x
        self.cursor_pos[1] += y
        actions = ActionChains(self, delay)
        actions.move_by_offset(x, y)
        return actions.perform()

    def move_to_xy(self, x, y, delay: int = 250):
        _ = self.get_window_size()
        _x = _["width"]
        _y = _["height"]
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x > _x:
            x = _x
        if y > _y:
            y = _y
        actions = ActionChains(self, delay)
        actions.w3c_actions.pointer_action.move_to_location(x, y)
        self.cursor_pos[0] = x
        self.cursor_pos[1] = y
        return actions.perform()

    def bezier_curve_coords_from_xy(
            self,
            x2, y2,
            control_points: int = random.SystemRandom().randint(3, 5),
            steps = None,
    ):
        x2 = int(x2)
        y2 = int(y2)
        x1, y1 = self.cursor_pos
        if x1 == x2 and y1 == y2:
            return None
        degree = 3 if control_points > 3 else control_points - 1
        x = np.linspace(x1, x2, num=control_points, dtype="int")
        y = np.linspace(y1, y2, num=control_points, dtype="int")
        offsetx = int(abs(x1-x2)/(control_points+1))
        offsety = int(abs(y1-y2)/(control_points+1))
        def rand(a):
            while True:
                b = random.SystemRandom().randint(-a, a)
                if abs(b/a) > 0.2:
                    return b
        xr = [0 if i == 0 or i == control_points-1 or offsetx == 0 else rand(offsetx) for i in range(control_points)]
        yr = [0 if i == 0 or i == control_points-1 or offsety == 0 else rand(offsety) for i in range(control_points)]
        xr[0] = yr[0] = xr[-1] = yr[-1] = 0
        x += xr
        y += yr
        tck, u = interpolate.splprep([x, y], k=degree)
        u = np.linspace(0, 1, num=steps)
        return interpolate.splev(u, tck)

    def mimic_move_to_random_xy(self, x_range: list = None, y_range: list = None, duration: float = None, steps: int = None):
        if not x_range:
            x_range = [400, 800]
        if not y_range:
            y_range = [400, 800]
        x = random.SystemRandom().randint(*x_range)
        y = random.SystemRandom().randint(*y_range)
        return self.mimic_move_to_xy(x, y, duration, steps)

    def mimic_move_to_xy(self, x: int, y: int, duration: float = None, steps: int = None):
        if not steps or not duration:
            steps = math.sqrt(abs(x-self.cursor_pos[0])**2+abs(y-self.cursor_pos[1])**2)/4
            duration = steps/283*2
            steps = int(steps)
        coords = self.bezier_curve_coords_from_xy(x, y, steps=steps)
        if not coords:
            return
        for coord in zip(*(i.astype(int) for i in coords)):
            self.move_to_xy(*coord, 0)
            self.wait(duration/steps)
        return True

    def mimic_move_to_element(self, path_or_selector_or_webelement, duration: float = None, steps: int = None):
        if not isinstance(path_or_selector_or_webelement, WebElement):
            if self.is_xpath(path_or_selector_or_webelement):
                path_or_selector_or_webelement = self.xpath(path_or_selector_or_webelement)[0]
            else:
                path_or_selector_or_webelement = self.querySelectorAll(path_or_selector_or_webelement)[0]
        x = path_or_selector_or_webelement.location["x"]+(path_or_selector_or_webelement.rect["width"])/2
        y = path_or_selector_or_webelement.location["y"]+(path_or_selector_or_webelement.rect["height"])/2
        return self.mimic_move_to_xy(
            x,
            y,
            duration=duration,
            steps=steps,
        )

    def _mimic_click(self):
        actions = ActionChains(self, random.SystemRandom().randint(100, 250))
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pointer_up()
        actions.perform()

    def mimic_click_xy(self, x, y, duration: float = None, steps: int = None):
        self.mimic_move_to_xy(x, y, duration, steps)
        self._mimic_click()

    def mimic_click(self, path_or_selector_or_webelement = None, duration: float = None, steps: int = None):
        if path_or_selector_or_webelement:
            self.mimic_move_to_element(path_or_selector_or_webelement, duration, steps)
        self._mimic_click()

    def move_to_element(self, path_or_selector_or_webelement, delay: int = 250):
        if not isinstance(path_or_selector_or_webelement, WebElement):
            if self.is_xpath(path_or_selector_or_webelement):
                path_or_selector_or_webelement = self.xpath(path_or_selector_or_webelement)[0]
            else:
                path_or_selector_or_webelement = self.querySelectorAll(path_or_selector_or_webelement)[0]
        actions = ActionChains(self, delay)
        actions.move_to_element(path_or_selector_or_webelement)
        self.cursor_pos = [
            path_or_selector_or_webelement.location["x"],
            path_or_selector_or_webelement.location["y"],
        ]
        return actions.perform()

    def click(self, path_or_selector_or_webelement = None, delay: int = 250):
        if path_or_selector_or_webelement:
            if not isinstance(path_or_selector_or_webelement, WebElement):
                if self.is_xpath(path_or_selector_or_webelement):
                    path_or_selector_or_webelement = self.xpath(path_or_selector_or_webelement)[0]
                else:
                    path_or_selector_or_webelement = self.querySelectorAll(path_or_selector_or_webelement)[0]
            self.move_to_element(path_or_selector_or_webelement)
        actions = ActionChains(self, delay)
        actions.click()
        return actions.perform()

    def send_input(self, path_or_selector_or_webelement, input, delay: int = 250):
        if not isinstance(path_or_selector_or_webelement, WebElement):
            if self.is_xpath(path_or_selector_or_webelement):
                path_or_selector_or_webelement = self.xpath(path_or_selector_or_webelement)[0]
            else:
                path_or_selector_or_webelement = self.querySelectorAll(path_or_selector_or_webelement)[0]
        actions = ActionChains(self, delay)
        actions.send_keys_to_element(path_or_selector_or_webelement, input)
        return actions.perform()

    @staticmethod
    def wait(s):
        time.sleep(s)

    @staticmethod
    def sleep_random():
        time.sleep(random.SystemRandom().uniform(0.5, 1))

    def format_element(self, e: WebElement):
        if not isinstance(e, WebElement):
            raise ValueError("'{}' is not WebElement".format(e))
        attributes = self.execute_script("var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value } return items;", e)
        attributes = " ".join("{}='{}'".format(k, escape(v)) for k, v in attributes.items())
        if attributes:
            attributes = " "+attributes
        return "<{tag}{}>...</{tag}>".format(attributes, tag=e.tag_name)

    def print_element(self, e: WebElement):
        print(self.format_element(e), flush=True)

    def pretty_format_element(self, e: WebElement):
        if not isinstance(e, WebElement):
            raise ValueError("'{}' is not WebElement".format(e))
        return etree.tostring(html.fromstring(e.get_attribute("outerHTML")), method="html", pretty_print=True).decode()

    def pretty_print_element(self, e: WebElement):
        print(self.pretty_format_element(e), flush=True)

    def get_console_log(self, level: str = None):
        log = self.get_log("browser")
        if not level:
            return log
        else:
            return [_ for _ in log if _["level"].lower() == level.lower()]
