# acess_infos.py locators

main_url = "https://www.nytimes.com"
reject_button_xpath = "xpath://button[@data-testid='Reject all-btn']"
search_button_xpath = "xpath://button[@data-testid='search-button']"
search_input_xpath = "xpath://input[@data-testid='search-input']"
section_button_xpath = "xpath://div[@data-testid='section']//button"
newest_news_xpath = "xpath://option[contains(text(), 'Sort by Newest')]"
show_more_xpath = "xpath://button[@data-testid='search-show-more-button']"

def section_xpath(section):
    section_xpath = f"xpath:*//ul[@data-testid='multi-select-dropdown-list']//li//label//span[contains(text(), '{section}')]"
    return section_xpath
