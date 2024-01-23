from RPA.Robocorp.WorkItems import WorkItems

from time import sleep
from robot.api import logger
from datetime import timedelta

from utils import Utils

from locators import acess_infos_locators as infoloc

class AcessInfos():
    def __init__(self, browser):
        self.browser = browser
        self.utils = Utils(self.browser)
        self.wi = WorkItems()
    
    def load_infos(self):

        self.wi.get_input_work_item()
        search_term = self.wi.get_work_item_variable("search_term")
        sections = self.wi.get_work_item_variable("sections")
        months = self.wi.get_work_item_variable("months")
        
        try:
            self.browser.open_available_browser(infoloc.main_url)

            #reject terms
            self.browser.wait_until_element_is_visible(infoloc.reject_button_xpath)
            sleep(1)
            self.browser.click_button(infoloc.reject_button_xpath)

            #search term
            self.browser.wait_until_element_is_enabled(infoloc.search_button_xpath)
            self.browser.click_button(infoloc.search_button_xpath)

            self.browser.wait_until_element_is_enabled(infoloc.search_input_xpath)
            self.browser.input_text(infoloc.search_input_xpath, search_term)
            self.browser.press_keys(infoloc.search_input_xpath, "ENTER")

            #click in section
            self.browser.wait_until_element_is_enabled(infoloc.section_button_xpath)
            self.browser.click_button(infoloc.section_button_xpath)

            #choose section
            for section in sections:
                try:
                    self.browser.click_element(infoloc.section_xpath(section))
                except Exception as e:
                    logger.error(f"Failed to choose section {section}. Erro {e}")

            #choose Newest news
            self.browser.click_element(infoloc.newest_news_xpath)

            sleep(1)
            
            for x in range(200):
                last_date_value = self.utils.last_date()
                if isinstance(last_date_value, bool):
                    last_date_value = self.utils.last_date_months(months) + timedelta(days=1)
                if self.utils.last_date_months(months) < last_date_value:
                    self.browser.wait_until_element_is_visible(infoloc.show_more_xpath)
                    self.browser.scroll_element_into_view(infoloc.show_more_xpath)
                    if self.browser.is_element_visible(infoloc.show_more_xpath):
                        self.browser.click_button(infoloc.show_more_xpath)
                else:
                    break
        except Exception as e:
            logger.error(f"Failed to open the news page. Erro {e}")
