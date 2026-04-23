from playwright.sync_api import sync_playwright
import pandas as pd
import time
import random
from urllib.parse import quote

# ==============================
# CONFIG
# ==============================
KEYWORD = "organic food"   # change this anytime
MAX_RESULTS = 10           # limit results (prevents timeout)


# ==============================
# UTILS
# ==============================
def delay():
    time.sleep(random.uniform(2, 3))


def matches(text, keyword):
    text = text.lower()
    words = keyword.lower().split()
    return any(w in text for w in words)


# ==============================
# SCRAPER
# ==============================
def scrape_facebook():
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        # load saved login session
        context = browser.new_context(storage_state="fb_state.json")
        page = context.new_page()

        encoded_keyword = quote(KEYWORD)
        url = f"https://www.facebook.com/search/top/?q={encoded_keyword}"

        print(f"🔍 Searching for: {KEYWORD}")
        page.goto(url, wait_until="networkidle")

        time.sleep(5)

        # scroll to load results
        for _ in range(5):
            page.mouse.wheel(0, 3000)
            delay()

        anchors = page.query_selector_all("a[href]")

        seen = set()

        for a in anchors:
            try:
                text = a.inner_text().strip()
                href = a.get_attribute("href")

                if not text or not href:
                    continue

                if "facebook.com" not in href:
                    continue

                if any(x in href for x in ["login", "recover", "help", "share"]):
                    continue

                if not matches(text, KEYWORD):
                    continue

                if href in seen:
                    continue
                seen.add(href)

                results.append({
                    "keyword": KEYWORD,
                    "name": text,
                    "link": href
                })

                # 🔥 LIMIT RESULTS
                if len(results) >= MAX_RESULTS:
                    break

            except:
                continue

        browser.close()

    return results


# ==============================
# SAVE CSV
# ==============================
def save_csv(data):
    df = pd.DataFrame(data, columns=["keyword", "name", "link"])

    df = df.drop_duplicates(subset=["link"])

    df.to_csv("facebook_data.csv", index=False)

    print(f"✅ Saved {len(df)} rows → facebook_data.csv")


# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    data = scrape_facebook()
    save_csv(data)