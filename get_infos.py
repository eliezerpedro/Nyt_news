from RPA.Robocorp.WorkItems import WorkItems

import pandas as pd
import re

from robot.api import logger
from datetime import datetime, timedelta

from utils import Utils
from locators import get_infos_locators as getloc

class GetInfos():
    def __init__(self, browser):
        self.browser = browser
        self.utils = Utils(self.browser)
        self.wi = WorkItems()

    def load_infos(self):

        self.wi.get_input_work_item()
        search_term = self.wi.get_work_item_variable("search_term")
        months = self.wi.get_work_item_variable("months")

        current_year = datetime.now().year
        aux = 1

        news_dict = {
            "title":[],
            "date":[],
            "description":[],
            "picture_filename":[],
            "amount_search_phrases":[],
            "amount_of_money":[],
            "image_src":[],
            "image_filename":[]
        }

        for x in self.browser.find_elements(getloc.list_news_xpath):
            news_html = x.get_attribute("outerHTML")
            if re.search(r'SKIP ADVERTISEMENT', news_html):
                continue

            try:
                date = x.text
                data_str = re.search(r".*\n", date).group(0).replace("\n", "")
                if 'ago' in data_str:
                    time_ago = int(re.search(r'(\d+)(m|h) ago', data_str).group(1))
                    if re.search(r'(\d+)(m|h) ago', data_str).group(2) == "m":
                        data_obj = datetime.now() - timedelta(minutes=time_ago)
                    else:
                        data_obj = datetime.now() - timedelta(hours=time_ago)
                else:
                    try:
                        data_obj = datetime.strptime(data_str, "%b. %d, %Y")
                    except ValueError:
                        try:
                            complete_date_str = f"{data_str}, {current_year}"
                            data_obj = datetime.strptime(complete_date_str, "%b. %d, %Y")
                        except Exception as e:
                            logger.error(f"Failed to load this News. erro {e}")

                if self.utils.last_date_months(months) > data_obj:
                    break

            except Exception as e:
                logger.error(f"Failed to load this News. Erro: {e}")

            title = re.search(r'<h4.*?>(.*?)<\/h4>', news_html).group(1)
            description = re.search(r'<\/h4><p.*?>(.*?)<\/p>', news_html).group(1)
            try:
                image_name =  re.search(r'<img alt="(.*?)"', news_html).group(1)
                if image_name == "":
                    image_name = "image_name_not_found"
            except Exception as e:
                image_name = "image_name_not_found"
                logger.error(f"Image name not found. Erro: {e}")

            try:
                src_image =  re.search(r'src="(.*?)"', news_html).group(1)
            except AttributeError:
                src_image = "link_not_found"

            phrase_to_count = title + description
            phrase_to_count = phrase_to_count.lower()
            count_search_phrase = phrase_to_count.count(search_term.lower())
            regex_coin = re.compile(r'\$(\d+\.\d+|\d+(,\d+)*(\.\d+)?)|(\d+)\s*dollars|\d+\s*USD')
            amount_money = bool(re.search(regex_coin, phrase_to_count))

            news_dict['title'].append(title)
            news_dict['date'].append(data_str)
            news_dict['description'].append(description)
            news_dict['picture_filename'].append(image_name)
            news_dict['amount_search_phrases'].append(count_search_phrase)
            news_dict['amount_of_money'].append(amount_money)
            news_dict['image_src'].append(src_image)
            news_dict['image_filename'].append(f"image_{aux}")
            aux +=1

        news_information = pd.DataFrame(news_dict)

        return news_information