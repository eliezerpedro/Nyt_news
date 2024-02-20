from RPA.Robocorp.WorkItems import WorkItems
from robot.api import logger
import pandas as pd
import re

from datetime import datetime, timedelta
from locators import get_infos_locators as getloc

class GetInfos:
    def __init__(self, browser, utils):
        self.browser = browser
        self.utils = utils
        self.wi = WorkItems()

    def load_infos(self):
        self.wi.get_input_work_item()
        search_term = self.wi.get_work_item_variable("search_term")
        months = self.wi.get_work_item_variable("months")
        current_year = datetime.now().year
        news_dict = self.extract_news_data(search_term, months, current_year)
        return pd.DataFrame(news_dict)

    def extract_news_data(self, search_term, months, current_year):
        news_dict = {
            "title": [],
            "date": [],
            "description": [],
            "picture_filename": [],
            "amount_search_phrases": [],
            "amount_of_money": [],
            "image_src": [],
            "image_filename": []
        }
        aux = 1

        for news_element in self.browser.find_elements(getloc.list_news_xpath):
            news_html = news_element.get_attribute("outerHTML")
            if re.search(r'SKIP ADVERTISEMENT', news_html):
                continue

            try:
                date_str = self.extract_date(news_element.text, current_year)
                if 'ago' in date_str:
                    time_ago = int(re.search(r'(\d+)(m|h) ago', date_str).group(1))
                    if re.search(r'(\d+)(m|h) ago', date_str).group(2) == "m":
                        date_obj = datetime.now() - timedelta(minutes=time_ago)
                    else:
                        date_obj = datetime.now() - timedelta(hours=time_ago)
                else:
                    date_obj = datetime.strptime(date_str, "%b. %d, %Y")

                if self.utils.last_date_months(months) > date_obj:
                    break

            except Exception as e:
                logger.error(f"Failed to load this News. Error: {e}")
                continue

            title = re.search(r'<h4.*?>(.*?)<\/h4>', news_html).group(1)
            description = re.search(r'<\/h4><p.*?>(.*?)<\/p>', news_html).group(1)
            image_name = self.extract_image_name(news_html)
            src_image = self.extract_image_source(news_html)
            count_search_phrase = self.count_search_phrase(title, description, search_term)
            amount_money = self.check_money(title, description)

            news_dict['title'].append(title)
            news_dict['date'].append(date_str)
            news_dict['description'].append(description)
            news_dict['picture_filename'].append(image_name)
            news_dict['amount_search_phrases'].append(count_search_phrase)
            news_dict['amount_of_money'].append(amount_money)
            news_dict['image_src'].append(src_image)
            news_dict['image_filename'].append(f"image_{aux}")
            aux += 1

        return news_dict

    def extract_date(self, text, current_year):
        date_str = re.search(r".*\n", text).group(0).replace("\n", "")
        if 'ago' in date_str:
            return date_str
        try:
            date_obj = datetime.strptime(date_str, "%b. %d, %Y")
        except ValueError:
            complete_date_str = f"{date_str}, {current_year}"
            date_obj = datetime.strptime(complete_date_str, "%b. %d, %Y")
        return date_obj.strftime("%b. %d, %Y")

    def extract_image_name(self, html):
        try:
            image_name = re.search(r'<img alt="(.*?)"', html).group(1)
            return image_name if image_name else "image_name_not_found"
        except Exception as e:
            logger.error(f"Image name not found. Error: {e}")
            return "image_name_not_found"

    def extract_image_source(self, html):
        try:
            return re.search(r'src="(.*?)"', html).group(1)
        except AttributeError:
            return "link_not_found"

    def count_search_phrase(self, title, description, search_term):
        phrase_to_count = (title + description).lower()
        return phrase_to_count.count(search_term.lower())

    def check_money(self, title, description):
        regex_coin = re.compile(r'\$(\d+\.\d+|\d+(,\d+)*(\.\d+)?)|(\d+)\s*dollars|\d+\s*USD')
        phrase_to_check = (title + description).lower()
        return bool(re.search(regex_coin, phrase_to_check))
