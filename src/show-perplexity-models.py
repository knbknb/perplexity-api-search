#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup

# Fetch the HTML
response = requests.get('https://docs.perplexity.ai/guides/model-cards')
#response = requests.get('https://docs.perplexity.ai/guides/pricing')

# Parse the HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Find the first and second tables
card_headers = soup.find_all('h2', attrs={'contenteditable': 'false'})
card_headers_clean = [ h.get_text().strip() for h in card_headers]

card_texts =  soup.select('h2 ~ div > p')
card_texts_clean = [ t.get_text().replace("Learn more →", "").strip() for t in card_texts]

print(f"{len(card_headers)} model cards found")

# zip the two lists together
try:
    assert len(card_headers_clean) == len(card_texts_clean)
except AssertionError:
    print(f"Error: {len(card_headers_clean)} != {len(card_texts_clean)}")
    print("Cannot zip the two lists together, they are not the same length.")
    print("Please check the HTML structure of the page.")
    exit(1)

model_cards = list(zip(card_headers_clean, card_texts_clean))

for model_card in model_cards:
    print(f"{model_card[0]}: {model_card[1]}")
