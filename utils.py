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
        if months == 0 or months == 1:
            return datetime(today.year, today.month, 1)

        previous_date = today - timedelta(days=today.day)
        previous_date = previous_date.replace(day=1)
        previous_date -= timedelta(days=30 * (months-2))

        return previous_date

    
    def last_date(self):
        news_list = self.browser.find_elements(utilsloc.last_date_xpath)
        current_year = datetime.now().year

        for x in range(len(news_list)):
            if x == 0:
                x = 1
            last_new = news_list[-x].text
            last_date_str = re.search(r".*\n", last_new).group(0).replace("\n", "")

            try:
                last_date = datetime.strptime(last_date_str, "%b. %d, %Y")
                return last_date
            except ValueError:
                try:
                    last_date = datetime.strptime(last_date_str, "%b %d, %Y")
                    return last_date
                except ValueError:
                    try:
                        complete_date_str = f"{last_date_str}, {current_year}"
                        last_date = datetime.strptime(complete_date_str, "%b. %d, %Y")

                        return last_date
                    except ValueError:
                        pass  

        return True
    
    def download_images(self, df_infos):

        df_imagens = df_infos[['image_src','image_filename']]
        pictures_dir = "pictures"

        if not os.path.exists(pictures_dir):
            os.makedirs(pictures_dir)

        for index, row in df_imagens.iterrows():
            try:
                self.browser.go_to(row['image_src'])
                image_path = f"pictures/{(row['image_filename'])}.png"
                self.browser.capture_element_screenshot("tag:img",image_path)
            except Exception as e:
                logger.error(f"Failed to save image: {row['image_filename']}. Error: {e}") 
