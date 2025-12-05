from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time, json
from bs4 import BeautifulSoup

QUERY = "JF Advisory Group Stitches Africa"

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://www.google.com")
time.sleep(2)

search = driver.find_element(By.NAME, "q")
search.send_keys(QUERY)
search.send_keys(Keys.RETURN)
time.sleep(3)

# scroll to load more results
for _ in range(2):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

results = []
seen = set()

for div in soup.select("div.g"):
    title_tag = div.find("h3")
    link_tag = div.find("a")
    if not title_tag or not link_tag:
        continue

    title = title_tag.text
    link = link_tag["href"]

    if link in seen:
        continue
    seen.add(link)

    img = "https://source.unsplash.com/600x400/?news"
    img_tag = div.find("img")
    if img_tag:
        img = img_tag.get("src", img)

    source = link.split("/")[2] if "://" in link else "Unknown"

    results.append({
        "title": title,
        "link": link,
        "source": source,
        "image": img
    })

print(json.dumps(results, indent=4))
