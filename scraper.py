import requests
from bs4 import BeautifulSoup

# A few GitLab handbook pages to start with
URLS = [
    "https://handbook.gitlab.com/handbook/values/",
    "https://handbook.gitlab.com/handbook/company/culture/",
    "https://handbook.gitlab.com/handbook/communication/",
    "https://handbook.gitlab.com/handbook/people-group/",
    "https://handbook.gitlab.com/handbook/engineering/",
]

def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    # Remove nav, footer, scripts
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    # Clean up blank lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

def scrape_all():
    all_text = []
    for url in URLS:
        print(f"Scraping: {url}")
        text = scrape_page(url)
        all_text.append({"url": url, "text": text})
    return all_text

if __name__ == "__main__":
    data = scrape_all()
    for item in data:
        print(f"\n--- {item['url']} ---\n{item['text'][:300]}")
    print("\nDone! Scraped", len(data), "pages.")