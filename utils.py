from datetime import datetime, timedelta
from robot.api import logger
import re
import os

from locators import utils_locators as utilsloc

class Utils():
    def __init__(self, browser):
        self.browser = browser
    
    def last_date_months(self, months):
        today = datetime.now()
        target_month = today.month - months
        target_year = today.year

        while target_month < 1:
            target_month += 12
            target_year -= 1

        target_date = datetime(target_year, target_month, 1)
        last_day_of_previous_month = target_date - timedelta(days=1)

        return last_day_of_previous_month
    
    def parse_date(self, date_str, current_year):
        date_formats = ["%b. %d, %Y", "%b %d, %Y"]
        for date_format in date_formats:
            try:
                return datetime.strptime(date_str + f", {current_year}", date_format)
            except ValueError:
                pass
        raise ValueError(f"Failed to parse date: {date_str}")

    def last_date(self):
        news_list = self.browser.find_elements(utilsloc.last_date_xpath)
        current_year = datetime.now().year

        for x in range(len(news_list)):
            if x == 0:
                x = 1
            last_new = news_list[-x].text
            last_date_str = re.search(r".*\n", last_new).group(0).replace("\n", "")

            try:
                return self.parse_date(last_date_str, current_year)
            except ValueError as e:
                logger.error(f"Failed to parse date: {last_date_str}. Error: {e}")
                pass  

        return True

    def download_images(self, df_infos):
        df_imagens = df_infos[['image_src', 'image_filename']]
        pictures_dir = "pictures"

        if not os.path.exists(pictures_dir):
            os.makedirs(pictures_dir)

        for index, row in df_imagens.iterrows():
            try:
                self.browser.go_to(row['image_src'])
                image_path = f"output/{row['image_filename']}.png"
                self.browser.capture_element_screenshot("tag:img", image_path)
            except Exception as e:
                logger.error(f"Failed to save image: {row['image_filename']}. Error: {e}")
