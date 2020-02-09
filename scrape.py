from time import sleep
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium import webdriver


class CollegeNet:
    def __init__(self, executable_path='geckodriver'):
        # Firefox options to download pdfs without asking
        options = Options()
        #options.set_preference("browser.download.folderList", 2);
        #options.set_preference("browser.download.dir", ".")
        #options.set_preference("browser.download.useDownloadDir", True)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf;application/zip")
        options.set_preference("pdfjs.disabled", True)

        self.selenium = webdriver.Firefox(executable_path=executable_path, options=options)
        # go to signin page
        self.selenium.get('https://admit.applyweb.com/admit/shibboleth/northwestern')
        # wait for human to log in
        WebDriverWait(self.selenium, 99999).until(
            expected_conditions.url_contains('https://admit.applyweb.com/admit/gwt'))
        # click "admit" button
        WebDriverWait(self.selenium, 20).until(
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

    def click_first_visible(self, selector, filter=None, sleep_time=1) -> bool:
        """return true if something was found to click."""
        while True:
            for e in self.selenium.find_elements_by_css_selector(selector):
                try:
                    if e.is_displayed():
                        if not filter or filter(e):
                            e.click()
                            sleep(sleep_time)
                            return True
                except WebDriverException:
                    print("WARNING: selenium exception")
                    sleep(sleep_time)
                    # try again
                    continue
            return False

    def open_pool(self, pool_name="Computer Engineering: MS"):
        for td in self.selenium.find_elements_by_css_selector('[eventproxy="isc_PoolTreeWindow_0"] td'):
            if td.text == pool_name:
                td.click()
                sleep(5)
                return

    def check_first_visible(self):
        return self.click_first_visible('tr[role="listitem"] span.checkboxFalse')

    def uncheck_first_visible(self):
        return self.click_first_visible('tr[role="listitem"] span.checkboxTrue')

    def click_download(self):
        self.click_actions()
        self.click_pdf()

    def click_actions(self):
        return self.click_first_visible('td.menuButton', filter=lambda e: e.text=="Actions")

    def click_pdf(self):
        return self.click_first_visible('td.menuTitleField nobr', filter=lambda e: e.text=="PDF")

    def sort_submission_date(self):
        return self.click_first_visible('td.headerButton div div', filter=lambda e: e.text == "Submission Date",
                                        sleep_time=5)

    def scroll_down_one(self):
        return self.click_first_visible('td.vScrollEnd')

    def download_first(self):
        self.check_first_visible()
        self.click_download()
        self.uncheck_first_visible()

    def download_all(self):
        at_bottom = False
        while True:
            rows = 0
            while self.check_first_visible():
                rows += 1
            self.click_download()
            while self.uncheck_first_visible(): pass
            sleep(5*60)  # wait for download to finish
            if at_bottom:
                break
            # scroll down
            for i in range(rows):
                if not self.scroll_down_one():
                    at_bottom = True


def main():
    # for some reason, running this in the IDE requires me to set the absolute geckodriver path
    with CollegeNet('/usr/local/bin/geckodriver') as cn:
        cn.open_pool("Electrical Engineering: MS")
        cn.sort_submission_date()
        cn.download_all()
        pass

if __name__ == '__main__':
    main()
