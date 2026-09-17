import json
import os
import time
import requests

TOKEN = os.environ.get("CF_API_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

# دنیا کے تمام بڑے اور اہم ممالک کی فہرست
COUNTRIES = [
    {"code": "GLOBAL", "name": "Worldwide (Global)"},
    {"code": "US", "name": "United States"},
    {"code": "GB", "name": "United Kingdom"},
    {"code": "CA", "name": "Canada"},
    {"code": "AU", "name": "Australia"},
    {"code": "DE", "name": "Germany"},
    {"code": "FR", "name": "France"},
    {"code": "IT", "name": "Italy"},
    {"code": "ES", "name": "Spain"},
    {"code": "NL", "name": "Netherlands"},
    {"code": "PK", "name": "Pakistan"},
    {"code": "IN", "name": "India"},
    {"code": "BD", "name": "Bangladesh"},
    {"code": "AE", "name": "United Arab Emirates"},
    {"code": "SA", "name": "Saudi Arabia"},
    {"code": "EG", "name": "Egypt"},
    {"code": "TR", "name": "Turkey"},
    {"code": "ID", "name": "Indonesia"},
    {"code": "MY", "name": "Malaysia"},
    {"code": "PH", "name": "Philippines"},
    {"code": "VN", "name": "Vietnam"},
    {"code": "TH", "name": "Thailand"},
    {"code": "BR", "name": "Brazil"},
    {"code": "MX", "name": "Mexico"},
    {"code": "AR", "name": "Argentina"},
    {"code": "CO", "name": "Colombia"},
    {"code": "ZA", "name": "South Africa"},
    {"code": "NG", "name": "Nigeria"},
    {"code": "KE", "name": "Kenya"},
    {"code": "JP", "name": "Japan"},
    {"code": "KR", "name": "South Korea"},
    {"code": "SG", "name": "Singapore"},
    {"code": "RU", "name": "Russia"},
    {"code": "UA", "name": "Ukraine"},
    {"code": "PL", "name": "Poland"},
    {"code": "SE", "name": "Sweden"},
    {"code": "NO", "name": "Norway"},
    {"code": "CH", "name": "Switzerland"},
]

result_data = {
    "updated_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
    "countries": [],
    "rankings": {},
}

for item in COUNTRIES:
    code = item["code"]
    name = item["name"]
    result_data["countries"].append({"code": code, "name": name})

    # گلوبل یا کنٹری وائز اینڈ پوائنٹ
    if code == "GLOBAL":
        url = "https://api.cloudflare.com/client/v4/radar/ranking/top?limit=100"
    else:
        url = f"https://api.cloudflare.com/client/v4/radar/ranking/top?limit=100&location={code}"

    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        if res.status_code == 200:
            domains = res.json().get("result", {}).get("top_0", [])
            result_data["rankings"][code] = [
                {"rank": idx + 1, "domain": d.get("domain")}
                for idx, d in enumerate(domains)
            ]
            print(f"Successfully fetched {name} ({len(domains)} domains)")
        else:
            print(f"Failed for {code}: {res.status_code}")
            result_data["rankings"][code] = []
    except Exception as e:
        print(f"Error fetching {code}: {e}")
        result_data["rankings"][code] = []

    time.sleep(0.2)  # کلاؤڈ فلیئر ریٹ لمٹ سے بچاؤ کے لیے ہلکا سا وقفہ

# ڈیٹا کو JSON میں محفوظ کریں
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(result_data, f, ensure_ascii=False, indent=2)

print("Finished writing data.json")
