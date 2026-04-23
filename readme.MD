# Facebook Scraper (Playwright + Python)

A simple script to collect Facebook search results (e.g. *salwar kameez*, *organic food*, *electric gadgets*) and export them to CSV.

---

## 🚀 Features

* Keyword-based Facebook search
* Saves results (name + link) to CSV
* Result limit (default: 10) to avoid timeout
* Uses saved login session (stable)

---

## 📦 Installation

### 1. Create `requirements.txt`

```txt
playwright==1.44.0
pandas==2.2.2
beautifulsoup4==4.12.3
requests==2.31.0
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Install Playwright browser (IMPORTANT)

```bash
playwright install chromium
```

👉 Without this step, the script will fail.

---

## 🔐 Step 1: Login Setup (Required)

Create `login.py`:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.facebook.com")

    print("👉 Login manually, then press ENTER...")
    input()

    context.storage_state(path="fb_state.json")

    browser.close()
```

Run:

```bash
python login.py
```

👉 This creates: `fb_state.json`

---

## ▶️ Step 2: Run the Scraper

```bash
python scraper.py
```

---

## ⚙️ Configuration

Edit inside `scraper.py`:

```python
KEYWORD = "organic food"
MAX_RESULTS = 10
```

Examples:

* `"salwar kameez"`
* `"sari"`
* `"electronics"`
* `"organic shampoo"`

---

## 📄 Output

```text
facebook_data.csv
```

Example:

```text
keyword,name,link
organic food,Green Organic Shop,https://facebook.com/xyz
```

---

## ⚠️ Notes & Limitations

* Facebook login session expires → rerun `login.py`
* Results depend on account & region
* Not suitable for large-scale scraping
* Facebook DOM may change → script may need updates

---

## 🧠 Tips

* Keep result limit low (10–30)
* Avoid frequent runs (prevents blocking)
* Use clear keywords

---

## 🛠 Troubleshooting

### Empty results

* Run `login.py` again
* Ensure session file exists (`fb_state.json`)

### Script opens login page

* Session expired → regenerate

### Slow performance

* Reduce `MAX_RESULTS`
* Reduce scroll iterations

---

## 📌 Disclaimer

For learning and small-scale usage only. Respect platform policies and avoid aggressive automation.

---

## ✅ Future Improvements

* Multi-keyword support
* Extract phone / WhatsApp from pages
* Store data in database instead of CSV

---

## 👨‍💻 Author

Built for experimentation and learning.
