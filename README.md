# hackernews-scraper
Scrapes emails from the list of people who want to be hired on HackerNews (https://seisvelas.github.io/hn-candidates-search/).

Requires Selenium, Webdriver Manager, and Google Chrome:
```
pip install selenium
pip install webdriver-manager
```
Note: This script fails a crashes a few seconds in on very rare occasions. If this occurs, just rerun the script or increase the WAIT_TIME parameter near the top of the script.
