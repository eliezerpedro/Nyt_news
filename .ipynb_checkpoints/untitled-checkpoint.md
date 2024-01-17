RPA Challenge
Overview
Our mission is to enable all people to do the best work of their lives—the first act in achieving that mission is to help companies automate tedious but critical business processes. This RPA challenge should showcase your ability to build a bot for purposes of process automation.

The Challenge
Your challenge is to automate the process of extracting data from the news site. Link to the news site: www.nytimes.com

You must have 3 configured variables (you can save them in the configuration file, but it is better to put them to the Robocorp Cloud Work Items):

search phrase

news category or section

number of months for which you need to receive news

Example of how this should work: 0 or 1 - only the current month, 2 - current and previous month, 3 - current and two previous months, and so on

The main steps:

Open the site by following the link
Enter a phrase in the search field
On the result page, apply the following filters:
select a news category or section

your automation should have the option to choose from none to any number of categories/sections. This should be specified via the config file or/and Robocorp Cloud Work Items

choose the latest (i.e., newest) news

Get the values: title, date, and description.
Store in an Excel file:
title

date

description (if available)

picture filename

count of search phrases in the title and description

True or False, depending on whether the title or description contains any amount of money

Possible formats: $11.1 | $111,111.11 | 11 dollars | 11 USD

Download the news picture and specify the file name in the Excel file
Follow steps 4-6 for all news that falls within the required time period
Specifically, we will be looking for the following in your submission:

Quality code Your code is clean, maintainable, and well-architected. The use of an object-oriented model is preferred.
Resiliency Your architecture is fault-tolerant and can handle failures both at the application level and website level.
Best practices Your implementation follows best RPA practices.
Please leverage pure Python

Please use pure Python (as demonstrated here) and pure Selenium (via rpaframework) without utilizing Robot Framework.

Focus on RPA
While APIs and Web Requests are possible, the focus is on RPA skillsets, so please do not use APIs or Web Requests for this exercise.

Bonus

Have fun with this challenge and express yourself. While the primary goal of this challenge is to assess your technical skills, we also love to see a sense of passion, creativity, and personality.