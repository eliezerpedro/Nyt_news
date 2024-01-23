# Nyt_news

## Overview

This project uses RPA to fetch information from the website www.nytimes.com and stores the obtained data in an excel file.


## Configured Variables

 

- Search phrase
- News category or section
- Number of months for which news is to be received

  

## Challenge

  

This challenge only uses Python with the RPA Framework's Selenium library. I divide this challenge into the following steps:

  

1. Open the New York Times website using Selenium.
2. Reject the cookies.
3. Type the search phrase in the search field and press enter.
4. Select the categories provided and filter by the most recent news.
5. Navigate to the latest news in the given date range.
6. Extract the news info, including title, date, description, and picture filename.
7. Count  occurrences of search  terms in titles  and  descriptions.
8. Checks whether the title or description contains an amount in the specified format.
9. Save all the the extracted data in an Excel file.
10. Download all the pictures from the news and store in a picture folder.

  

## Requirements

  



- Python 3.x
- RPA Framework
- Pandas

  

## How to Use

  

1. Clone the repository.
2. Install the dependencies using pip

  

```bash

pip  install  rpaframework

```

  

3. Change the work-items.json file with the desired values for the search term, news category, and number of months.

4. Run the Python script 

  

```bash

python  tasks.py

```


5. After  the  script  has  finished  running, you  can  find  the  extracted  news  data in the `nyt_news_info.xlsx` file and the pictures in the pictures folder.


---