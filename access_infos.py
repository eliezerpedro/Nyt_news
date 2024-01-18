# from RPA.Robocorp.WorkItems import WorkItems

from time import sleep
from robot.api import logger
from datetime import timedelta

from utils import Utils
import config

class AcessInfos():
    def __init__(self, browser):
        self.browser = browser
        self.utils = Utils(self.browser)
        # self.wi = WorkItems()
    
    def load_infos(self):

        # self.wi.get_input_work_item()
        # search_term = wi.get_work_item_variable("search_term")
        # sections = wi.get_work_item_variable("sections")
        # months = wi.get_work_item_variable("months")
        
        try:
            self.browser.open_available_browser("https://www.nytimes.com")

            #reject terms
            reject_button_xpath = "xpath://button[@data-testid='Reject all-btn']"
            self.browser.wait_until_element_is_visible(reject_button_xpath)
            sleep(1)
            self.browser.click_button(reject_button_xpath)

            #search term
            search_button_xpath = "xpath://button[@data-testid='search-button']"
            self.browser.wait_until_element_is_enabled(search_button_xpath)
            self.browser.click_button(search_button_xpath)

            search_input_xpath = "xpath://input[@data-testid='search-input']"
            self.browser.wait_until_element_is_enabled(search_input_xpath)
            self.browser.input_text(search_input_xpath, config.search_term)
            # self.browser.input_text(search_input_xpath, search_term)
            self.browser.press_keys(search_input_xpath, "ENTER")

            #click in section
            section_button_xpath = "xpath://div[@data-testid='section']//button"
            self.browser.wait_until_element_is_enabled(section_button_xpath)
            self.browser.click_button(section_button_xpath)

            #choose section
            for section in config.sections:
            # for section in sections:
                section_xpath = f"xpath:*//ul[@data-testid='multi-select-dropdown-list']//li//label//span[contains(text(), '{section}')]"
                try:
                    self.browser.click_element(section_xpath)
                except Exception as e:
                    logger.error(f"Failed to choose section {section}. Erro {e}")

            #choose Newest news
            newest_news_xpath = "xpath://option[contains(text(), 'Sort by Newest')]"
            self.browser.click_element(newest_news_xpath)

            sleep(1)
            
            for x in range(200):
                last_date_value = self.utils.last_date()
                if isinstance(last_date_value, bool):
                    last_date_value = self.utils.last_date_months(config.months) + timedelta(days=1)
                if self.utils.last_date_months(config.months) < last_date_value:
                #     last_date_value = self.utils.last_date_months(months) + timedelta(days=1)
                # if self.utils.last_date_months(months) < last_date_value:
                    show_more_xpath = "xpath://button[@data-testid='search-show-more-button']"
                    self.browser.wait_until_element_is_visible(show_more_xpath)
                    self.browser.scroll_element_into_view(show_more_xpath)
                    if self.browser.is_element_visible(show_more_xpath):
                        self.browser.click_button(show_more_xpath)
                else:
                    break
        except Exception as e:
            logger.error(f"Failed to open the news page. Erro {e}")
