following google_scholar.py approach in https://github.com/starzia/bibliometrics

PREREQUISITES
-------------

Download the Firefox driver from:
https://github.com/mozilla/geckodriver/releases

Install it to /usr/local/bin/geckodriver or put it somewhere else and edit the path in main() of scraper.py

If you update Firefox, then you might have to re-download the latest geckodriver.

Setup your Python environment:

python3 -m venv ~/virtualenv/collegenet-scrape
. ~/virtualenv/collegenet-scrape/bin/activate
pip install selenium

RUNNING IT
----------
If necessary, change the application pool string in main() function of scraper.py.  Then run:

python3 scrape.py
