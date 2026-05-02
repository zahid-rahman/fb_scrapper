# Facebook Active Page Scraper (Playwright + Python)

A focused scraping tool to discover active Facebook business pages based on recent post activity and export them into CSV.

---

## 🚀 Features

- Keyword-based Facebook page discovery
- Filters only active pages (recent posts within last 1 year)
- Smart activity detection logic:
  - Relative time (e.g., 1h, 2d, yesterday)
  - Month + day (assumed current year)
  - Year-based validation (current year / last year)
- Ignores:
  - Personal profiles
  - Groups / irrelevant links
- Fast execution using:
  - Early exit logic
  - Limited timestamp checking (first 3 posts only)
- Saves clean data to CSV

---

## 🧠 How It Works

text 1. Search Facebook pages using keyword 2. Collect candidate page links 3. Visit each page 4. Scroll slightly to load posts 5. Extract first few timestamps 6. If ANY timestamp is recent → mark ACTIVE 7. Save only active pages 

👉 This ensures both speed and accuracy

---

## 📦 Installation

### 1. Create requirements.txt

txt playwright==1.44.0 pandas==2.2.2 beautifulsoup4==4.12.3 requests==2.31.0 

---

### 2. Install dependencies

pip install -r requirements.txt 

---

### 3. Install Playwright browser (IMPORTANT)

python3 -m playwright install chromium 

---

## 🔐 Step 1: Login Setup (Required)

Create login.py:

python from playwright.sync_api import sync_playwright  with sync_playwright() as p:     browser = p.chromium.launch(headless=False)     context = browser.new_context()     page = context.new_page()      page.goto("https://www.facebook.com")      print("👉 Login manually, then press ENTER...")     input()      context.storage_state(path="fb_state.json")      browser.close() 

Run:

bash python login.py 

👉 This creates fb_state.json for authenticated scraping.

---

## ▶️ Step 2: Run the Scraper

bash python scraper.py 

---

## ⚙️ Configuration

Modify inside scraper.py:

python KEYWORD = "ladies bag" LOCATION = "bangladesh" MAX_PAGES = 15 MAX_ACTIVE = 5 

### Examples:

- "salwar kameez"
- "sari"
- "organic food"
- "electronics"

---

## 📄 Output

text facebook_active_pages.csv 

Example:

text page_name,page_link,is_active Green Organic Shop,https://facebook.com/xyz,True Bag World BD,https://facebook.com/abc,True 

---

## 🔍 Activity Detection Logic (Important)

A page is considered ACTIVE if any of the first 3 timestamps matches:

### ✅ Valid signals:
- 1h, 2d, 30m
- yesterday, just now
- March 15 (no year → assumed current)
- 2025, 2026 (within last year range)

### ❌ Invalid:
- March 15, 2021
- Any year older than last year

### Rule Priority:

text 1. Year (highest priority) 2. Relative time 3. Month + day (only if no year) 

---

## ⚠️ Limitations

- Facebook DOM is dynamic → may break over time
- Some pages:
  - hide timestamps
  - show pinned posts first
- Accuracy ~80–90% (realistic expectation)
- Login session may expire

---

## 🧠 Tips for Better Results

- Keep MAX_PAGES low (10–20)
- Avoid running too frequently (prevents blocking)
- Use specific keywords (e.g., "ladies bag bd")

---

## 🛠 Troubleshooting

### ❌ No results

- Run login.py again
- Check fb_state.json exists

---

### ❌ Script opens login page

- Session expired → regenerate

---

### ❌ Wrong active/inactive

- Increase scroll iterations slightly
- Facebook UI variation may affect detection

---

## 📌 Disclaimer

This project is for educational and small-scale usage only.  
Respect Facebook’s policies and avoid aggressive scraping.

---

## 🚀 Future Improvements

- Detect and skip pinned posts
- Extract:
  - WhatsApp
  - Phone number
- Multi-keyword batch processing
- Activity scoring system (instead of boolean)

---

## 👨‍💻 Author

Md Zahid Rahman  
Software Engineer & Product Builder  
Focused on scalable data-driven systems