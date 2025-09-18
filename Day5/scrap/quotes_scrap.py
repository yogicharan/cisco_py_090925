import requests
from bs4 import BeautifulSoup # pip install bs4
import json

def scrape_quotes(base_url, pages=5):
    all_quotes = []

    for page in range(1, pages + 1):#1 2 3 4 5
        url = f"{base_url}/page/{page}/"
        print(f"Scraping {url} ...")

        response = requests.get(url)
        if response.status_code != 200:
            print(f" Failed to fetch {url}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        #
        quotes = soup.find_all("div", class_="quote")
        for quote in quotes:
            text = quote.find("span", class_="text").get_text(strip=True)
            author = quote.find("small", class_="author").get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in quote.find_all("a", class_="tag")]

            all_quotes.append({
                "quote": text,
                "author": author,
                "tags": tags
            })

    return all_quotes


if __name__ == "__main__":
    base_url = "http://quotes.toscrape.com"
    all_quotes = scrape_quotes(base_url, pages=3)  # scrape 3 pages

    # Save results into JSON file
    with open("quotes.json", "w", encoding="utf-8") as f:
        json.dump(all_quotes, f, ensure_ascii=False, indent=4)

    print(f"Scraping complete! Saved {len(all_quotes)} quotes into quotes.json")