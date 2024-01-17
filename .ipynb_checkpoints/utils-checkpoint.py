from datetime import datetime, timedelta
import re

def last_date_months(months):
    today = datetime.now()
    if months == 0 or months == 1:
        return datetime(today.year, today.month, 1)

    previous_date = today - timedelta(days=today.day)
    previous_date = previous_date.replace(day=1)
    previous_date -= timedelta(days=30 * (months-2))

    return previous_date


def last_date(browser):
    last_date_xpath = "xpath://ol[@data-testid='search-results']//li"
    news_list = browser.find_elements(last_date_xpath)
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
