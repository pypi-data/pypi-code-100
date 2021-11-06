import time
from urllib.parse import quote

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, \
                                       ElementNotInteractableException, UnexpectedAlertPresentException, \
                                       NoSuchWindowException, InvalidSessionIdException

from autoselenium.driver import Driver


class WhapBot(Driver):
    _URL = "https://web.whatsapp.com/"
    XPATH_SELECTORS = {  # THESE PATHS ARE SUBJECT TO CHANGE!!
        "send_button": '//*[@id="main"]/footer/div[1]/div[3]/button',
        "all_messages": '//*[@role="region"]',
        "last_message": '//*[@role="region"]/div[last()]',
        "message_check": '//*[@data-testid="msg-dblcheck"]|//*[@data-testid="msg-time"]'
    }
    CSS_SELECTORS = {
        "main_page": '.two',
        "qr_code": 'canvas',
        "chat_bar": 'div.input',
        "message_meta": 'div[data-testid="msg-meta"]',
        "qr_reloader": 'div[data-ref] > span > div'
    }
    STATUS = {
        'pending': ['pending', 'pendiente'],
        'read': ['read', 'leído'],
        'received': ['received', 'entregado']
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._logged = True if self._cookies_path.exists() else False

    @property
    def is_logged(self):
        return self._logged

    def login_required(func):
        def logged_checker(self, *args, **kwargs):
            if not self.is_logged:
                self.log()
            return func(self, *args, **kwargs)

        return logged_checker

    def log(self, url=_URL, timeout=15, retries=0):
        self.get(url)

        while not self.is_logged:
            try:
                WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, f'{self.CSS_SELECTORS["main_page"]}, {self.CSS_SELECTORS["qr_code"]}')))
                self._logged = True
                self._save_local_storage()
            except NoSuchElementException:
                self._logged = False
            except (UnexpectedAlertPresentException, TimeoutException) as e:
                if not retries:
                    raise RuntimeError(f"Number of retries exceeded: {e}")
                self.retry(self.log, url, retries=retries - 1)

    @login_required
    def send(self, phone, message, retries=5):
        try:
            self.get(url=f"{self._URL}send?phone={phone}&text={quote(message)}")
            self.click_send_button()
            while not self.check_message_is_sent(message):
                self.click_send_button()
                time.sleep(1)  # Used to avoid most of the exceptions

        except (ElementNotInteractableException, UnexpectedAlertPresentException, TimeoutException) as e:
            if not retries:
                raise RuntimeError(f"Number of retries exceeded: {e}")
            self.retry(self.send, phone, message, retries=retries - 1)

    @login_required
    def open_chat_by_phone(self, phone, timeout=20, retries=5):
        self.get(url=f"{self._URL}send?phone={phone}")
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, self.XPATH_SELECTORS["all_messages"]))
            )
        except TimeoutException as e:
            if not retries:
                raise RuntimeError(f"Number of retries exceeded: {e}")
            self.retry(self.open_chat_by_phone, phone, retries - 1)

    @login_required
    def click_send_button(self, retries=5):
        try:
            send_button = self.driver.find_elements_by_tag_name('button')[-1]
            send_button.click()
        except NoSuchElementException as e:
            if not retries:
                raise RuntimeError(f"Cannot get last message status: {e}")
            self.retry(self.click_send_button, retries - 1)

    @login_required
    def check_message_is_sent(self, message):
        text, status = self.get_last_message()
        if text == message and status not in self.STATUS['pending']:
            return True
        return False

    @login_required
    def get_last_message_status(self, last_msg, retries=10):
        try:
            msg_meta = last_msg.find_element_by_css_selector(self.CSS_SELECTORS['message_meta'])
            last_msg = msg_meta.find_element_by_xpath(self.XPATH_SELECTORS['message_check'])
            status = last_msg.get_attribute("aria-label").strip().lower()
            return status

        except (NoSuchElementException, IndexError) as e:
            if not retries:
                raise RuntimeError(f"Cannot get last message status: {e}")
            self.retry(self.get_last_message_status, retries - 1)

    @login_required
    def get_last_message(self, retries=20):
        try:
            last_msg = WebDriverWait(self.driver, 100).until(
                EC.visibility_of_element_located((By.XPATH, self.XPATH_SELECTORS["last_message"]))
            )
            text = str(last_msg.text.split('\n')[0])
            status = self.get_last_message_status(last_msg)
            return text, status

        except NoSuchElementException as e:
            if not retries:
                raise RuntimeError(f"Number of retries exceeded: {e}")
            self.retry(self.get_last_message, retries - 1)

    def reload_qr(self):
        self.driver.find_element_by_css_selector(self.CSS_SELECTORS["qr_reloader"]).click()
