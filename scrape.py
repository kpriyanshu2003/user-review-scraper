import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

# Set up Chrome options and service
path = "./chromedriver.exe"
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox")
service = Service(path)
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://www.nykaa.com/best-offer-pages/luxe-favourites-at-buy-2-get-1/c/53727?transaction_id=2f8c40a75a4ad4aee7471c70e33c1b2a&intcmp=nykaa:hp:desktop-homepage:default:Brand_Days_1_Strip:CAROUSEL_V2:12:Clinique;Too%20Faced;M.A.C;Smashbox;Estee%20Lauder;Bobbi%20Brown:12808;3899;4130;5108;3814;997:2f8c40a75a4ad4aee7471c70e33c1b2a&transaction_id=246c036072aeac514c2185cc1dc54487&intcmp=nykaa:hp:desktop-homepage:default:top_brands:SLIDING_WIDGET_V2:8:12808;3814;3899;4130;5108;8457;997:12808;3814;3899;4130;5108;8457;997:246c036072aeac514c2185cc1dc54487"

wait_time = 0.1  # keep it between 0 to 0.1
url_df = {
    "url": [],
}
driver.get(url)

total_height = int(driver.execute_script("return document.body.scrollHeight"))

for i in range(1, total_height, 5):
    time.sleep(wait_time)
    driver.execute_script("window.scrollTo(0, {});".format(i))

content_div = driver.find_element(By.ID, "product-list-wrap")
page_html = BeautifulSoup(content_div.get_attribute("outerHTML"), "html.parser")
page_content = page_html.findAll("img")

print(f"Number of images found: {len(page_content)}")
for img in page_content:
    img_src = img["src"]
    url_df["url"].append(img_src)

df = pd.DataFrame(url_df, columns=["url"])
df.to_csv("nykaa_images.csv", index=False)
