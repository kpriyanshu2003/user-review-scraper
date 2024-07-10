from random import uniform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import os

baseURL = "https://www.flipkart.com/intel-core-i3-4130t-2-9-ghz-lga-1150-socket-2-cores-4-threads-3-mb-smart-cache-desktop-processor/p/itm8f67aefba0795?pid=PSRFGWFWMZHGQYAZ&marketplace=FLIPKART&q=intel&srno=s_7_280&fm=organic&ppt=sp&ppn=sp&qH=4e5bbaeafc82ab7a"
product_fullName = baseURL.split("/")[3]
product_id = baseURL.split("/")[5].split("?")[0]

product_url = (
    "https://www.flipkart.com/"
    + product_fullName
    + "/product-reviews/"
    + product_id
    + "?page={}"
)
path = "./chromedriver.exe"
chrome_options = Options()
service = Service(path)
driver = webdriver.Chrome(service=service, options=chrome_options)


reviews_dict = {
    "product_id": [],
    "product_fullName": [],
    "product_url": [],
    "product_name": [],
    "product_cost": [],
    "review_title": [],
    "review_content": [],
    "review_rating": [],
    "review_date": [],
    "review_location": [],
    "review_likes": [],
    "review_dislikes": [],
}

start_page = 1
end_page = None

try:
    if end_page is None:
        driver.get(product_url.format(1))
        no_page = driver.find_element(By.CSS_SELECTOR, "._1G0WLw.mpIySA")
        page_html = BeautifulSoup(no_page.get_attribute("outerHTML"), "html.parser")
        page_content = (
            page_html.find("div", class_="_1G0WLw mpIySA")
            .find_all("span")[0]
            .get_text()
            .split(" ")[-1]
        )
        end_page = int(page_content)
except Exception as e:
    print(e)
    end_page = 1

try:
    for j in range(start_page, end_page + 1):

        driver.get(product_url.format(j))
        content_div = driver.find_element(By.CSS_SELECTOR, ".DOjaWF.gdgoEp.col-9-12")

        content_html = content_div.get_attribute("outerHTML")
        result = BeautifulSoup(content_html, "html.parser")

        reviews = result.find_all("div", class_="cPHDOP col-12-12")

        product_name = " ".join(
            result.find("div", class_="Vu3-9u eCtPz5")
            .contents[0]
            .strip()
            .split(" ")[:2]
        )

        product_cost = driver.find_element(By.CLASS_NAME, "yRaY8j").text.replace(
            "₹", ""
        )

        for i in reviews:
            main = i.find("div", class_="col EPCmJX Ma1fCG")

            extract_review_title = lambda i: (
                i.find("p", class_="z9E0IG").get_text().strip()
                if i.find("p", class_="z9E0IG")
                else None
            )

            if extract_review_title(i) == None:
                continue

            extract_review_content = lambda i: (
                re.sub(r"\s+", " ", i.find("div", class_="ZmyHeo").get_text())
                .replace("READ MORE", "")
                .strip()
                if i.find("div", class_="ZmyHeo")
                else " "
            )

            extract_review_rating = lambda i: (
                i.find("div", class_="XQDdHH Ga3i8K").get_text().strip().split()[0]
                if i.find("div", class_="XQDdHH Ga3i8K")
                else " "
            )

            extract_review_date = lambda i: (
                i.find_all("p", class_="_2NsDsF")[1].get_text().strip()
                if i.find_all("p", class_="_2NsDsF")[1]
                else " "
            )

            extract_review_location = lambda i: (
                i.find("p", class_="MztJPv").get_text().strip().split(",")[1]
                if i.find("p", class_="MztJPv")
                else " "
            )

            extract_likes_dislikes = lambda i: [
                i.find_all("span", class_="tl9VpF")[0].get_text().strip(),
                i.find_all("span", class_="tl9VpF")[1].get_text().strip(),
            ]

            review_title = extract_review_title(i)
            review_content = extract_review_content(i)
            review_rating = extract_review_rating(i)
            review_date = extract_review_date(i)
            review_location = extract_review_location(i)
            review_likes = extract_likes_dislikes(i)[0]
            review_dislikes = extract_likes_dislikes(i)[1]

            reviews_dict["product_id"].append(product_id)
            reviews_dict["product_fullName"].append(product_fullName)
            reviews_dict["product_url"].append(product_url.format(j))
            reviews_dict["product_name"].append(product_name)
            reviews_dict["product_cost"].append(product_cost)
            reviews_dict["review_title"].append(review_title)
            reviews_dict["review_content"].append(review_content)
            reviews_dict["review_rating"].append(review_rating)
            reviews_dict["review_date"].append(review_date)
            reviews_dict["review_location"].append(review_location)
            reviews_dict["review_likes"].append(review_likes)
            reviews_dict["review_dislikes"].append(review_dislikes)

finally:
    df = pd.DataFrame(reviews_dict)
    while True:
        if os.path.isfile(f"./flipkart/{product_id}.csv"):
            product_id = product_id + "-" + str(int(uniform(1, 100)))
        else:
            break
    csv_filename = f"./flipkart/{product_id}.csv"
    df.to_csv(csv_filename, index=False)
    print(f"Data saved to {csv_filename}")
    driver.quit()
