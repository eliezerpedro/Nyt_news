from RPA.Robocorp.WorkItems import WorkItems
from time import sleep
from robot.api import logger
from datetime import timedelta

from locators import acess_infos_locators as infoloc

class AcessInfos:
    def __init__(self, browser, utils):
        self.browser = browser
        self.utils = utils
        self.wi = WorkItems()

    def load_infos(self):
        try:
            self.setup()
            self.navigate_to_search_page()
            self.search_for_term()
            self.select_sections()
            self.select_newest_news()
            self.load_more_news()
        except Exception as e:
            logger.error(f"Failed to load news information. Error: {e}")

    def setup(self):
        self.wi.get_input_work_item()
        self.sections = self.wi.get_work_item_variable("sections")
        self.search_term = self.wi.get_work_item_variable("search_term")
        self.months = self.wi.get_work_item_variable("months")
        self.browser.open_available_browser(infoloc.main_url)
        self.reject_terms()

    def reject_terms(self):
        self.browser.wait_until_element_is_visible(infoloc.reject_button_xpath)
        sleep(1)
        self.browser.click_button(infoloc.reject_button_xpath)

    def navigate_to_search_page(self):
        self.browser.wait_until_element_is_enabled(infoloc.search_button_xpath)
        self.browser.click_button(infoloc.search_button_xpath)
        self.browser.wait_until_element_is_enabled(infoloc.search_input_xpath)
        self.browser.input_text(infoloc.search_input_xpath, self.search_term)
        self.browser.press_keys(infoloc.search_input_xpath, "ENTER")

    def search_for_term(self):
        pass

    def select_sections(self):
        self.browser.wait_until_element_is_enabled(infoloc.section_button_xpath)
        self.browser.click_button(infoloc.section_button_xpath)
        for section in self.sections:
            try:
                self.browser.click_element(infoloc.section_xpath(section))
            except Exception as e:
                logger.error(f"Failed to choose section {section}. Error: {e}")

    def select_newest_news(self):
        self.browser.click_element(infoloc.newest_news_xpath)
        sleep(1)

    def load_more_news(self):
        while True:
            last_date_value = self.utils.last_date()
            if isinstance(last_date_value, bool):
                last_date_value = self.utils.last_date_months(self.months) + timedelta(days=1)
            if self.utils.last_date_months(self.months) < last_date_value:
                self.browser.wait_until_element_is_visible(infoloc.show_more_xpath)
                self.browser.scroll_element_into_view(infoloc.show_more_xpath)
                if self.browser.is_element_visible(infoloc.show_more_xpath):
                    self.browser.click_button(infoloc.show_more_xpath)
            else:
                break
