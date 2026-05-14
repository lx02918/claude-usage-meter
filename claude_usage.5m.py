#!/opt/homebrew/bin/python3
# <swiftbar.title>Claude Usage Meter</swiftbar.title>
# <swiftbar.version>1.1</swiftbar.version>
# <swiftbar.desc>Displays Claude.ai Pro usage in menu bar</swiftbar.desc>
# <swiftbar.refreshTime>5</swiftbar.refreshTime>

import json
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

ORG_CACHE = Path.home() / ".config" / "claudemeter" / "org_id.txt"

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://claude.ai",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
}

def get_browser_cookies():
    import browser_cookie3
    for loader in [browser_cookie3.chrome, browser_cookie3.safari]:
        try:
            jar = loader(domain_name="claude.ai")
            cookies = list(jar)
            if any(c.name == "sessionKey" for c in cookies):
                return "; ".join(f"{c.name}={c.value}" for c in cookies)
        except Exception:
            continue
    return None

def api_get(url, cookie_str):
    req = urllib.request.Request(url, headers={**HEADERS, "Cookie": cookie_str})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())

def get_org_id(cookie_str):
    if ORG_CACHE.exists():
        return ORG_CACHE.read_text().strip()
    orgs = api_get("https://claude.ai/api/organizations", cookie_str)
    org_id = orgs[0].get("uuid") or orgs[0].get("id") if orgs else None
    if org_id:
        ORG_CACHE.parent.mkdir(parents=True, exist_ok=True)
        ORG_CACHE.write_text(org_id)
    return org_id

def format_reset(iso_str):
    if not iso_str:
        return "?"
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        secs = max(0, int((dt - datetime.now(timezone.utc)).total_seconds()))
        h, m = divmod(secs // 60, 60)
        return f"{h}h {m}m" if h else f"{m}m"
    except Exception:
        return "?"

def bar(pct, w=10):
    f = round(pct / 100 * w)
    return "█" * f + "░" * (w - f)

def color(pct):
    return "red" if pct >= 90 else "orange" if pct >= 70 else "green"

def main():
    try:
        cookie_str = get_browser_cookies()
        if not cookie_str:
            print("⚠ Claude | color=orange")
            print("---")
            print("Log in to claude.ai in Chrome or Safari first")
            return

        org_id = get_org_id(cookie_str)
        if not org_id:
            raise ValueError("No org found")

        data = api_get(f"https://claude.ai/api/organizations/{org_id}/usage", cookie_str)

        s = data.get("five_hour", {})
        w = data.get("seven_day", {})
        sn = data.get("seven_day_sonnet")

        sp = round(s.get("utilization", 0))
        wp = round(w.get("utilization", 0))
        print(f"{bar(sp)} {sp}% | color={color(sp)} font=Menlo size=11")
        print("---")
        print(f"Session (5h)  {bar(sp, 8)} {sp:>3}% | color={color(sp)} font=Menlo")
        print(f"  Resets in {format_reset(s.get('resets_at'))} | color=gray size=11")
        print(f"Weekly  (7d)  {bar(wp, 8)} {wp:>3}% | color={color(wp)} font=Menlo")
        print(f"  Resets in {format_reset(w.get('resets_at'))} | color=gray size=11")

        if sn:
            snp = round(sn.get("utilization", 0))
            print(f"Sonnet  (7d)  {bar(snp, 8)} {snp:>3}% | color={color(snp)} font=Menlo")
            print(f"  Resets in {format_reset(sn.get('resets_at'))} | color=gray size=11")

        print("---")
        print(f"Updated {datetime.now().strftime('%H:%M')} | color=gray size=11")
        print("Refresh | refresh=true")

    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            ORG_CACHE.unlink(missing_ok=True)
        print(f"⚠ Claude {e.code} | color=orange")
        print("---")
        print("Refresh | refresh=true")
    except Exception as e:
        print("⚠ Claude | color=orange")
        print("---")
        print(f"{e}")
        print("Refresh | refresh=true")

if __name__ == "__main__":
    main()
