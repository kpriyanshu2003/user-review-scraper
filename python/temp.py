from email.mime import base
from random import uniform
from exceptiongroup import catch
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import os
import csv

path = "./chromedriver.exe"
chrome_options = Options()
service = Service(path)
driver = webdriver.Chrome(service=service, options=chrome_options)

with open("userbench-urls.csv", mode="r") as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        baseUrl = row["url"]
        product_name = baseUrl.split("/")[3]
        product_id = baseUrl.split("/")[5].split("?")[0]

        reviews_dict = {
            "product_id": [],
            "product_url": [],
            "product_name": [],
            "review_title": [],
            "review_content": [],
            "review_date": [],
        }

        driver.get(baseUrl)

        try:
            content_div = driver.find_element(By.ID, "wikiForm").get_attribute(
                "outerHTML"
            )
            page_html = BeautifulSoup(content_div, "html.parser")
            page_content = page_html.find_all("div", class_="row showchildlinkonhover")

            for i in page_content:
                review_title = ""
                review_date = ""
                review_content = ""
                content = i.find("div", class_="col-xs-9 fancyfont")
                if content:
                    review_header = content.find("h4", class_="lighterblacktext")
                    if review_header:
                        review_title = review_header.get_text()

                    review_date = content.find("span", class_="wiki-ts")
                    if review_date:
                        review_date = review_date.get_text()

                    review_content = content.find("p", class_="medp")
                    if review_content:
                        review_content = review_content.get_text().strip()
                        review_content = " ".join(review_content.split())

                reviews_dict["product_id"].append(product_id)
                reviews_dict["product_url"].append(baseUrl)
                reviews_dict["product_name"].append(product_name)
                reviews_dict["review_title"].append(review_title)
                reviews_dict["review_content"].append(review_content)
                reviews_dict["review_date"].append(review_date)

        finally:
            df = pd.DataFrame(reviews_dict)
            while True:
                if os.path.isfile(f"./cpu-userbench/{product_id}.csv"):
                    product_id = product_id + "-" + str(int(uniform(1, 100)))
                else:
                    break
            csv_filename = f"./cpu-userbench/{product_id}.csv"
            df.to_csv(csv_filename, index=False)
            print(f"Data saved to {csv_filename}")
            driver.quit()
