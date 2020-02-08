import urllib
import time
import re
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, InvalidElementStateException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium import webdriver

#from web_util import wait, tree_from_string, css_select, Selector
from typing import List


def wait():
    time.sleep(2 + random.uniform(0,3))


def none_to_empty(obj):
    return obj if obj else ''


def empty_to_none(str):
    return str if len(str) > 0 else None


def parse_int(str) -> int:
    return int(str) if str else 0


def get_from_array(arr, idx):
    if idx >= len(arr):
        return None
    else:
        return empty_to_none(arr[idx])


class CollegeNet:
    def __init__(self, executable_path=None):
        self.selenium = \
            webdriver.Firefox(executable_path=executable_path) if executable_path else webdriver.Firefox()
        # go to signin page
        self.selenium.get('https://admit.applyweb.com/admit/shibboleth/northwestern')
        # wait for human to log in
        WebDriverWait(self.selenium, 99999).until(
            expected_conditions.url_contains('https://admit.applyweb.com/admit/gwt'))
        # click "admit" button
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "td.button"))
        )
        for button in self.selenium.find_elements_by_css_selector('td.button'):
            if button.text == 'Admit':
                button.click()
        # wait for contents to render
        WebDriverWait(self.selenium, 1).until(
            expected_conditions.text_to_be_present_in_element((By.ID, "isc_PoolTreeWindow_3_0_valueCell0"), 'MS')
        )


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.selenium.quit()

    def get_page(self, url):
        wait()
        self.selenium.get(url)

def main():
    # for some reason, running this in the IDE requires me to set the geckodriver path
    with CollegeNet('/usr/local/bin/geckodriver') as scholar:
        pass

if __name__ == '__main__':
    main()
