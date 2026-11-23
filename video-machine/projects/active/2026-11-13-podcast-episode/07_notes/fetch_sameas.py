"""Print the ld+json sameAs links and every social href on the guest company's pages (read only).
Run: ./run.sh --no-secrets python <this file>"""
import json
import re
import urllib.request

PAGES = ["https://www.allaboutsepticservices.com", "https://www.allaboutsepticservices.com/contact-us",
         "https://www.allaboutsepticservices.com/about-us"]
SOCIAL = re.compile(r'https?://[^"\'\s<>)]*(?:facebook|instagram|tiktok|youtube|youtu\.be|twitter|x\.com|linkedin)[^"\'\s<>)]*', re.I)
for url in PAGES:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001
        print(url, "->", e)
        continue
    print("==", url, len(html), "bytes")
    for m in re.finditer(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', html, re.S | re.I):
        try:
            data = json.loads(m.group(1))
        except Exception:  # noqa: BLE001
            print("  (unparsable ld+json)", m.group(1)[:200])
            continue
        stack = [data]
        while stack:
            d = stack.pop()
            if isinstance(d, dict):
                if "sameAs" in d:
                    print("  sameAs:", d["sameAs"], "| name:", d.get("name"), "| type:", d.get("@type"))
                stack.extend(d.values())
            elif isinstance(d, list):
                stack.extend(d)
    print("  social hrefs:", sorted(set(SOCIAL.findall(html))))
