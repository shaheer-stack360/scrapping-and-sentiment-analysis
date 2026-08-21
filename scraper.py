import requests
import json
import urllib.parse
import time
import csv
from datetime import datetime
from data_cleaner import clean_and_filter_review


# ── Constants ──────────────────────────────────────────────────────────────────

URL = "https://play.google.com/_/PlayStoreUi/data/batchexecute"

HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Referer": "https://play.google.com/",
    "Origin": "https://play.google.com",
}

COOKIES = {
    "__Secure-1PAPISID": "d30uCND8Q7aoMa7b/AixYK--QebWVB4ktp",
    "__Secure-1PSID": "g.a000BAk1JN3kJguRXSf0gJ-fKYjcOWD9yzSi6O9uQXL9Szt0hMENtSs1NIou-YavFL1xY26A3AACgYKAawSARISFQHGX2MiZMarOC75GaZ_T3tI8BYMKBoVAUF8yKpqbe6yDUCJfgUZ4D2PhtdF0076",
    "__Secure-1PSIDCC": "AKEyXzWOVbU331Zx53vLonZfVdm7OUgV4v0rjf6uAiAcRRrSU2M9EhSNFEJgI5XQz8t3YOZfzt9i",
    "__Secure-1PSIDTS": "sidts-CjEBXMw41aPyTUmSzS_dNqn0XapImd-MmJ5EuEDNPJ-Ty2zDqOSz3_F906dxI96Zw4H1EAA",
    "__Secure-3PAPISID": "d30uCND8Q7aoMa7b/AixYK--QebWVB4ktp",
    "__Secure-3PSID": "g.a000BAk1JN3kJguRXSf0gJ-fKYjcOWD9yzSi6O9uQXL9Szt0hMEN0Y888NYrjuFszouqFcYszgACgYKAVQSARISFQHGX2Mi_BORIMqg8tz5tRiw9KcLkRoVAUF8yKrf4sKG4YbKzR7hcT5mtM3V0076",
    "__Secure-3PSIDCC": "AKEyXzUrs-tkKMJkeauLSxvJln-fmT5OowtfbRERmZH7OKLMJwUzECQU77aJr3XOtpOBMV2LHMQb",
    "__Secure-3PSIDTS": "sidts-CjEBXMw41aPyTUmSzS_dNqn0XapImd-MmJ5EuEDNPJ-Ty2zDqOSz3_F906dxI96Zw4H1EAA",
    "__Secure-BUCKET": "CDM",
    "__Secure-OSID": "g.a000Bgk1JAKkLhGsXffxN_U-ZwBHNNk8cNd6Y4eiy2PHns2V9-McCE1dHBXS6N8-LS8Mo_ZUoAACgYKAUoSARISFQHGX2MitnzIcbe5tgNtfw9GFdU2QBoVAUF8yKpUWhgET2Dd-UWTGcmgPJfw0076",
    "__Secure-STRP": "ANmZwa2UOGf_DGcERIV3wGfFn26DEWLYL5jLzX1z6T9eGifTu_-LyeArW2388yvZnpr4HJObssMF2F1XjbyZGsTkuyEpbGJQ_KfZ",
    "AEC": "AdJVEavIVC9aFXzoNwFunqRihtYBVBYCTU9UuyD83tqOWjhvJKEAe6zvAuk",
    "APISID": "bY6H9uCSdXUT5WRj/ArCA5hD4n2yCy6vnW",
    "HSID": "AlKYApZpKqQaLBA7B",
    "NID": "534=ApauXenjbYSqlNZtptT3cuAHt7bvoOU5rlK9YDwPE26cIgeFGhj2qZwcCq1sv-cPCqmIdsu8ZiyztN8v0nplMbUEFMBWzeDJ2hQwvTNZ5TQFtwuDyDqfNg6aUmCTj8wfYe1_ZpvO4IKE7cBVIXiJBL8q1cmg4f4g8oPHb2g4zbfMxAvYYpe-OZeWsZ_aOzxdgDXuwjpDGv4fkgVkdRi3SzKqX-qM51rZxU34ThHWxDNlpyPRQiJyEGIIrYcJ8_SVh5JC3UWKQ0y0YkoNyIOQH8OeoNKvRGtGnFZ7CImZ3mozLyG2WXi9AJV6_CSq_wqymV59UbMiOQb-7DcKLIhvuNBvnvBlZCrfYhi6AuWDGYLjuUFGjUJip_98nCnga_-SNKPsEueQiEv9fivhiYOo_wzI0PP3HszB9vKxVUAdsz52HvSN4HHFqAySArsqxQ7FL-HA20N_B6AS1p0zyRfHbBKVpx8uIkT5d9zw_iCC9MzJBP5OFUvC__VCf5ExcRW8y6SyZsD885XweKijjWZM-_OhCCNCC9f_of7mTggPpYygdqmqrWpr19JWiMfDXRSsYn-xjWMSXd9VRghhM4VPElD-VA6njv79meGEqC2dHh9SmqMu-_tBmbvsy4qIUcl-crKyHVkMCRnJ1tl31aQDtzpWXStRcPX3Zz1uDa0Wp9yhwGLvvYaI70W-WLUomoF0cDDA7UxUxg1rY1bd0VR4f4_Ray3MkgqExCSPtn0",
    "OSID": "g.a000Bgk1JAKkLhGsXffxN_U-ZwBHNNk8cNd6Y4eiy2PHns2V9-Mc4JIaojXtOv8QXMbw6qBJzgACgYKAWcSARISFQHGX2MinrP55ckF7FErSVIg_N1lzxoVAUF8yKqUEm2DW44kTGbqfD3OUI0j0076",
    "OTZ": "8748840_36_36__36_",
    "PLAY_ACTIVE_ACCOUNT": "ICrt_XL61NBE_S0rhk8RpG0k65e0XwQVdDlvB6kxiQ8=authuser-0",
    "SAPISID": "d30uCND8Q7aoMa7b/AixYK--QebWVB4ktp",
    "SEARCH_SAMESITE": "CgQIw6EB",
    "SID": "g.a000BAk1JN3kJguRXSf0gJ-fKYjcOWD9yzSi6O9uQXL9Szt0hMEN8bBtreABklE8bAUyGo5GAAACgYKATwSARISFQHGX2MiHRX5Z8iMpdzhjaSr5HC2rBoVAUF8yKpzyNb8tgtQ4zMZWZA7_4S70076",
    "SIDCC": "AKEyXzX5LabUrtXxzruRWujM-1vJO5DGHMF6oSXJHKZ0uTaDeuVPjguKgbzQdSF1u6FJ9fj6Yxs",
    "SSID": "AozlJhhF-nGMijnRA",
}

SORT_OPTIONS = {
    "relevant": 1,
    "newest":   2,
    "rating":   3,
}


# ── Payload Builder ────────────────────────────────────────────────────────────

XSRF_TOKEN = "AGWv4bf8cPC6peITUfCjbFPdkgFF:1787299486872"

def build_payload(app_id: str, sort: int, count: int, token: str | None = None) -> dict:
    # Google's strict UsvDTd structural array layout
    inner = json.dumps(
        [
            None, 
            None, 
            [2, sort, [count, None, token]], # [Type, SortMode, [Count, None, PaginationToken]]
            [app_id, 7]                      # [PackageName, AppStoreType]
        ],
        separators=(",", ":")
    )
    
    # Outer request wrapping the stringified payload
    outer = json.dumps([[["UsvDTd", inner, None, "generic"]]], separators=(",", ":"))
    
    return {
        "f.req": outer,
        "at": XSRF_TOKEN,
    }



# ── Response Parser ────────────────────────────────────────────────────────────

def parse_response(text: str) -> tuple[list[dict], str | None]:
    # Dropping header prefixes
    lines = text.splitlines()
    start = 0
    for i, line in enumerate(lines):
        if line.strip().startswith(")]}"):
            start = i + 1
            break

    outer = None
    for i in range(start, len(lines)):
        line = lines[i].strip()
        if line.isdigit() or not line.startswith("[["):
            continue
        try:
            outer = json.loads(line)
            break
        except json.JSONDecodeError:
            pass

    if not outer or not outer[0] or len(outer[0]) < 3:
        return [], None

    # The payload data string sits at index slot 2 inside the outer execution array
    inner_str = outer[0][2]
    if not inner_str:
        return [], None

    inner = json.loads(inner_str)
    
    # In UsvDTd, raw reviews reside inside nested array slot [0]
    reviews_raw = inner[0] if (inner and len(inner) > 0) else []
    reviews = []

    for r in reviews_raw:
        if not r or len(r) < 5:
            continue
        try:
            # Safe timestamp unpacking from internal serialization structure
            # Inside your parse_response() for loop:
            raw_review_text = r[4]
            analysis = clean_and_filter_review(raw_review_text)

            # Choose whether to drop non-English data entirely for your Sentiment Models
            if not analysis["is_english"]:
                continue # Skips non-English reviews entirely from your final CSV array

            reviews.append({
                "review_id":   r[0],
                "name":        r[1][0],
                "rating":      r[2],
                "text":        analysis["text_only"],  # Cleaned, readable text strings
                "emojis":      analysis["emojis"],     # Extracted symbols kept separate
            })

        except (IndexError, TypeError):
            continue

    # Extracting the next token safely out of index slot [1][1]
    next_token = None
    try:
        if len(inner) > 1 and inner[1]:
            next_token = inner[1][1]
    except (IndexError, TypeError):
        pass

    return reviews, next_token


# ── Main Scraper ───────────────────────────────────────────────────────────────

def scrape_reviews(app_id: str, total: int = 100, sort: str = "newest") -> list[dict]:
    sort_int   = SORT_OPTIONS.get(sort, 2)
    batch_size = min(total, 100)
    all_reviews = []
    token = None

    params = {
        "rpcids":       "UsvDTd",
        "source-path":  "/store/apps/details",
        "f.sid":        "-1694966614209196078",
        "bl":           "boq_playuiserver_20260819.09_p0",
        "hl":           "en",
        "authuser":     "0",
        "soc-app":      "121",
        "soc-platform": "1",
        "soc-device":   "1",
        "_reqid":       "246583",
        "rt":           "c",
    }

    print(f"Scraping reviews for: {app_id}  |  sort={sort}  |  target={total}")

    while len(all_reviews) < total:
        payload = build_payload(app_id, sort_int, batch_size, token)

        resp = requests.post(URL, headers=HEADERS, params=params, data=payload, cookies=COOKIES)
        print("RAW RESPONSE:", resp.text[:100])
        if resp.status_code != 200:
            print("HTTP Error:", resp.status_code)
            print("Response body:", resp.text[:100])
            break

        reviews, token = parse_response(resp.text)

        if not reviews:
            print("No more reviews returned.")
            break

        all_reviews.extend(reviews)
        print(f"  Fetched {len(all_reviews)} / {total}")

        if not token:
            print("No pagination token — reached the end.")
            break

        time.sleep(1.5)  # be polite to Google

    return all_reviews[:total]


# ── Save to CSV ────────────────────────────────────────────────────────────────

def save_to_csv(reviews: list[dict], filename: str = "reviews.csv") -> None:
    if not reviews:
        print("Nothing to save.")
        return

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=reviews[0].keys())
        writer.writeheader()
        writer.writerows(reviews)

    print(f"Saved {len(reviews)} reviews to {filename}")


# ── Entry Point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    APP_ID   = "com.instagram.android"
    TOTAL    = 8000          # how many reviews you want
    SORT     = "newest"     # "newest" | "relevant" | "rating"
    OUTFILE  = "instagram_reviews.csv"

    reviews = scrape_reviews(APP_ID, total=TOTAL, sort=SORT)
    save_to_csv(reviews, OUTFILE)