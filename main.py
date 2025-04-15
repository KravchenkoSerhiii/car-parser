import requests
import csv
import time
import random

from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

BASE_URL = "https://www.otomoto.pl/osobowe/" # Required link
NEEDED_URL = BASE_URL + "mazda/2" # Link to special model of car

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0"
]

# Count of parsed pages
MAX_PAGES = 10

def get_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9,uk;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": NEEDED_URL,
    }
# Function for parsed and getting links in main pages
def get_car_links(page):
    url = f"{NEEDED_URL}?page={page}"
    try:
        headers = get_headers()
        response = requests.get(url, headers=headers)
        time.sleep(5)  # Delay

        if response.status_code != 200:
            print(f"❌ Page error {page}: {response.status_code}")
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        links = []

        # Get the correct links
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "/osobowe/oferta/" in href:
                if not href.startswith("http"):
                    href = "https://www.otomoto.pl" + href
                links.append(href)

        print(f"✅ Page {page}: {len(links)} links")
        return list(set(links))
    except Exception as e:
        print(f"⚠️ Error on page {page}: {e}")
        return []

# Get car details from required page
def parse_car_details(url):
    try:
        headers = get_headers()
        response = requests.get(url, headers=headers)
        time.sleep(5)  # Delay

        # 10 secs delay for correct parsing of many pages
        while True:
            if response.status_code == 403:
                time.sleep(10)
                response = requests.get(url, headers=headers)
            else:
                break

        soup = BeautifulSoup(response.content, "html.parser")
        data = {"Link": url}

        title_tag = soup.find("h1", class_="offer-title")
        if title_tag:
            data["Name"] = title_tag.get_text(strip=True)

        price_number = soup.find("span", class_="offer-price__number")
        price_currency = soup.find("span", class_="offer-price__currency")
        if price_number and price_currency:
            data["Price"] = f"{price_number.get_text(strip=True)} {price_currency.get_text(strip=True)}"


        condition_year_tag = soup.find("p", class_="e1kkw2jt0 ooa-vy37q4")
        if condition_year_tag:
            parts = [part.strip() for part in condition_year_tag.get_text(strip=True).split("·")]
            if len(parts) >= 2:
                data["Condition"] = parts[0]
                data["Year"] = parts[1]

        details_section = soup.find("div", {"data-testid": "main-details-section"})
        if details_section:
            for detail in details_section.find_all("div", {"data-testid": "detail"}):
                key_tag = detail.find("p", class_="e127x9ub3")
                value_tag = detail.find("p", class_="e127x9ub2")
                if key_tag and value_tag:
                    key = key_tag.get_text(strip=True)
                    value = value_tag.get_text(strip=True)
                    data[key] = value

        return data
    except Exception as e:
        print(f"⚠️ Error in {url}: {e}")
        return None

def main():
    links = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        links = list(executor.map(get_car_links, range(1, MAX_PAGES + 1)))

    all_links = set()
    for page_links in links:
        all_links.update(page_links)

    print(f"🔗 Total collected: {len(all_links)} links")

    # Parsing details
    car_data = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        car_data = list(executor.map(parse_car_details, all_links))

    # Save to CSV file
    with open("cars_multithreading.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        header_written = False

        for car in car_data:
            if car:
                if not header_written:
                    writer.writerow(car.keys())
                    header_written = True
                writer.writerow(car.values())

if __name__ == "__main__":
    main()
