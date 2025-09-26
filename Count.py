import requests
from bs4 import BeautifulSoup

# ====== CHANGE THESE ======
PS_URL = "https://www.sih.gov.in/sih2025PS/SIH25015"
BOT_TOKEN = "8367328861:AAF3b4iRpSj8damj-t_OA3fmAvGEsifwHBo"
CHAT_ID = "7725408496"
COUNT_FILE = "count.txt"
# ==========================

# Read last count
try:
    with open(COUNT_FILE, "r") as f:
        last_count = int(f.read())
except:
    last_count = 0

# Fetch current count
response = requests.get(PS_URL)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the first <td> that looks like "34/300"
element = soup.find('td', string=lambda text: text and "/" in text)

if element:
    current, total = element.get_text(strip=True).split("/")
    count = int(current)
else:
    count = 0

# Compare and notify
if count > last_count:
    message = f"✅ New submission detected! Total count: {count}"
else:
    message = f"ℹ️ No new submissions. Count remains {count}"

# Send Telegram message with error logging
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
params = {"chat_id": CHAT_ID, "text": message}
resp = requests.get(url, params=params)
print("Telegram response:", resp.status_code, resp.text)

# Save current count
with open(COUNT_FILE, "w") as f:
    f.write(str(count))
