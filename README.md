# A web Scraper - lankabd1
A web scraper to scrape Company info links from multiple site-pages at once

This is fairly a large project for me -- this is a part of my *MBA research project paper*. Still in its initial stage. hopefully will get to the end of the line soon.
Any help regarding `scrapy` or `python` is highly appreciated.

## About
The scraper fetches the stock info of the listed stocks in DSE which is collected and maintained by the company called [Lanka Bangla](http://lankabd.com).
The scraper has a three-tier structure: 
  - initial fetching of a link of the site for preliminary data about each company
  - fetching the secondary link for the selected company to get more company data
  - from the same page, through a differnt 'menu-link' collecting the financials from the tables included and sending them to spreadsheet by spreadsheet on an excel workbook
  
## How to run
Assuming you have all the necessary requirements for running ***Scrapy***, just run the following on your *terminal.app*:
```shell-script
    $ scrapy crawl lanka -o $(date +%Y%m%d-%H%M%S)_csv.csv --logfile $(date +%Y%m%d-%H%M%S).log
```
The instruction will scrape data into the `.csv` file and log all the DEBUG info in the `.log` file.
