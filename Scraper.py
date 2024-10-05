import time
from bs4 import BeautifulSoup
import requests
import pandas as pd

all_quotes = []
all_authors = []


def scrape(page_number):

    page_num = str(page_number)
    url = "https://quotes.toscrape.com/page/" + page_num

    page_to_scrape = requests.get(url)
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")

    quotes = soup.findAll("span", attrs={"class":"text"})
    authors = soup.findAll("small", attrs={"class":"author"})

    for quote, author in zip(quotes, authors):
       # print(f"{quote.text} - {author.text}")  
        all_quotes.append(quote.text)
        all_authors.append(author.text)

    next_button = soup.find("li", class_="next")
    return bool(next_button)

page_number = 1
while True:
    has_next = scrape(page_number)
    if not has_next:
        break
    page_number += 1
    time.sleep(2)

df = pd.DataFrame({
    'Quote': all_quotes,
    'Authors': all_authors
})

df.to_csv('quotes.csv', index=False)