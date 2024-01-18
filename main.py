from RPA.Browser.Selenium import Selenium

from selenium.common.exceptions import ElementClickInterceptedException
from time import sleep
from robot.api import logger
from datetime import datetime, timedelta

import re
import pandas as pd
import os

# from utils import download_images
from utils import Utils
from get_infos import GetInfos
from access_infos import AcessInfos


class NtyInfos:
    def __init__(self):
        self.browser = Selenium()
        self.access_infos = AcessInfos(self.browser)
        self.get_infos = GetInfos(self.browser)
        self.utils = Utils(self.browser)
    
    def main(self):
        
        self.access_infos.load_infos()
        
        df_infos = self.get_infos.load_infos()

        self.utils.download_images(df_infos)
        df_infos.drop('image_src', axis=1, inplace=True)
        df_infos.to_excel("nyt_news_info.xlsx", index=False)
        
    
nyt = NtyInfos()
nyt.main()