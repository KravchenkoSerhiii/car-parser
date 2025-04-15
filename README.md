# 🚗 Otomoto Car Paraser

This Python script scrapes car listings from the [Otomoto.pl](https://www.otomoto.pl/osobowe/) website and save car details to CSV file

---

## 📌 Features

- Scrapes multiple pages (up to a defined limit)
- Extracts links to individual car offers
- Visits each car's page and collects detailed information
- Uses multithreading (`ThreadPoolExecutor`) for faster execution
- Saves all results to a CSV file (`cars_multithreading.csv`)
- Includes randomized headers and delays to reduce blocking risks

---

## 📁 Extracted Data

For each car listing, the script collects:

- Link
- Name (title)
- Price
- Condition
- Year
- Additional details from the specifications section (e.g. fuel type, mileage, transmission)

---

## ⚙️ Requirements

- Python 3.7+
- Libraries:
  - `requests`
  - `beautifulsoup4`

Install the required packages:

```bash
pip install requirements.txt
```

---

## 🚀 How to Run

1. Clone or download this repository
2. Run the script:

```bash
python main.py
```

3. After execution, the file `cars_multithreading.csv` will be created in the same directory.

---

## ⚙️ Configuration

You can adjust the following parameters inside the script:

- `NEEDED_URL` – target car model URL  
  (currently set to `https://www.otomoto.pl/osobowe/mazda/2`)
- `MAX_PAGES` – how many pages to scrape (default: 10)

---

## 🧠 Notes

- The script uses random `User-Agent` headers and delays between requests to mimic human behavior.
- If the site returns a **403 Forbidden** error, the scraper will retry after a short delay.
- This scraper is for educational purposes only. Respect the website's `robots.txt` and terms of service.

---

## 🛠️ Future Improvements

- Add command-line arguments for dynamic URL and page limits
- Integrate logging
- Add proxy rotation for more robust anti-blocking

---
