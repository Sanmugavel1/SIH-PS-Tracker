import requests
from bs4 import BeautifulSoup

# ====== CHANGE THESE ======
PS_URL = "https://www.sih.gov.in/sih2025PS/SIH25015"  # Replace PS_ID with your PS
BOT_TOKEN = "8367328861:AAF3b4iRpSj8damj-t_OA3fmAvGEsifwHBo"   # From Telegram BotFather
CHAT_ID = "7725408496"       # From getUpdates
COUNT_FILE = "count.txt"  # File to store last count
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

# ====== CHANGE THIS SELECTOR ======
# Find the first <td> that looks like "34/300"
element = soup.find('td', string=lambda text: text and "/" in text)

if element:
    current, total = element.get_text(strip=True).split("/")
    count = int(current)   # this will be 34
else:
    count = 0


# ==================================

# Compare and notify
if count > last_count:
    message = f"New submission detected! Total count: {count}"
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}")
    
# Save current count
with open(COUNT_FILE, "w") as f:
    f.write(str(count))
