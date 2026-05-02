from playwright.sync_api import sync_playwright
import pandas as pd
import time
import random
from urllib.parse import quote
import re
from datetime import datetime

# ==============================
# CONFIG
# ==============================
KEYWORD = "ladies bag"
LOCATION = "bangladesh"
MAX_PAGES = 15
MAX_ACTIVE = 5

CURRENT_YEAR = datetime.now().year
LAST_YEAR = CURRENT_YEAR - 1

MONTHS = [
    "january","february","march","april","may","june",
    "july","august","september","october","november","december",
    "jan","feb","mar","apr","jun","jul","aug","sep","oct","nov","dec"
]

# ==============================
# UTILS
# ==============================
def delay(a=2, b=4):
    time.sleep(random.uniform(a, b))


def clean_url(url):
    return url.split("?")[0].rstrip("/")


def is_valid_page_link(href):
    if not href:
        return False

    if "facebook.com" not in href:
        return False

    # ❌ remove profiles
    if "profile.php" in href:
        return False

    # ❌ remove query garbage
    if "?" in href:
        return False

    bad = [
        "/groups/", "/posts/", "/photos/", "/videos/",
        "login", "recover", "help", "friends", "people"
    ]

    if any(x in href for x in bad):
        return False

    return True


# ==============================
# STEP 1: SEARCH
# ==============================
def search_pages(context):
    page = context.new_page()

    query = quote(f"{KEYWORD} {LOCATION}")
    url = f"https://www.facebook.com/search/pages/?q={query}"

    print(f"🔍 Searching: {KEYWORD}")
    page.goto(url, wait_until="networkidle")
    page.wait_for_timeout(4000)

    for _ in range(4):
        page.mouse.wheel(0, 4000)
        delay()

    anchors = page.locator("a[href*='facebook.com']").all()

    links = []
    seen = set()

    for a in anchors:
        href = a.get_attribute("href")

        if not is_valid_page_link(href):
            continue

        href = clean_url(href)

        if href in seen:
            continue

        seen.add(href)
        links.append(href)

        if len(links) >= MAX_PAGES:
            break

    page.close()
    print(f"✅ Candidate pages: {len(links)}")

    return links


# ==============================
# CORE LOGIC
# ==============================
def is_active_text(text):
    t = text.strip().lower()

    # 🔥 1. YEAR (highest priority)
    year_match = re.search(r"\b(20\d{2})\b", t)
    if year_match:
        year = int(year_match.group(1))
        return year >= LAST_YEAR

    # 🔥 2. RELATIVE TIME
    if re.search(r"\b\d+\s*(h|hr|hrs|hour|hours)\b", t):
        return True

    if re.search(r"\b\d+\s*(m|min|mins|minute|minutes)\b", t):
        return True

    if re.search(r"\b\d+\s*(d|day|days)\b", t):
        return True

    if "just now" in t or "yesterday" in t:
        return True

    # 🔥 3. MONTH + DAY (only if NO year)
    if any(month in t for month in MONTHS):
        if re.search(r"\b\d{1,2}\b", t):
            return True

    return False


# ==============================
# 🔥 YOUR FINAL RULE IMPLEMENTATION
# ==============================
def check_latest_post(page):
    try:
        elements = page.locator("span, a")
        texts = elements.all_inner_texts()

        CHECK_LIMIT = 3
        checked = 0

        for text in texts:
            t = text.strip().lower()

            if len(t) < 2:
                continue

            # timestamp-like filter
            if not (
                re.search(r"\b(20\d{2})\b", t)
                or re.search(r"\b\d+\s*(h|hr|m|min|d|day)\b", t)
                or "ago" in t
                or "just now" in t
                or "yesterday" in t
                or re.search(r"\b\d{1,2}\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)", t)
            ):
                continue

            checked += 1

            # 🔥 CRITICAL RULE
            if is_active_text(t):
                return True   # ✅ ANY recent → ACTIVE

            if checked >= CHECK_LIMIT:
                break

        return False  # ❌ none matched

    except:
        return False


# ==============================
# PROCESS PAGE
# ==============================
def check_page(context, url):
    page = context.new_page()

    try:
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(4000)

        page_name = ""
        try:
            h1 = page.locator("h1").first
            if h1:
                page_name = h1.inner_text().strip()
        except:
            pass

        # small scroll (avoid pinned)
        for _ in range(3):
            page.mouse.wheel(0, 5000)
            delay()

        if check_latest_post(page):
            page.close()
            return {
                "page_name": page_name,
                "page_link": url,
                "is_active": True
            }

        page.close()
        return None

    except:
        page.close()
        return None


# ==============================
# MAIN
# ==============================
def run():
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="fb_state.json")

        links = search_pages(context)

        for link in links:
            print(f"➡️ Checking: {link}")

            data = check_page(context, link)

            if data:
                print("   ✅ ACTIVE")
                results.append(data)
            else:
                print("   ❌ INACTIVE")

            if len(results) >= MAX_ACTIVE:
                break

            delay(2, 4)

        browser.close()

    return results


# ==============================
# SAVE CSV
# ==============================
def save_csv(data):
    df = pd.DataFrame(data)
    df = df.drop_duplicates(subset=["page_link"])

    df.to_csv("facebook_active_pages.csv", index=False)
    print(f"\n✅ Saved {len(df)} active pages")


# ==============================
# ENTRY
# ==============================
if __name__ == "__main__":
    data = run()
    save_csv(data)