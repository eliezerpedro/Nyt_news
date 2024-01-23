from RPA.Browser.Selenium import Selenium
from robocorp.tasks import task

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
        df_infos.to_excel("output/nyt_news_info.xlsx", index=False)
        
@task
def main():  
    nyt = NtyInfos()
    nyt.main()

if __name__ == "__main__":
    main()