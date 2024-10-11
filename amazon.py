import math
from random import uniform
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
import os
import csv

# Set up Chrome options and service
path = "./chromedriver.exe"
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox")
service = Service(path)
driver = webdriver.Chrome(service=service, options=chrome_options)

with open("amazon_urls.csv", mode="r") as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        baseUrl = row["URL"]

        product_id = baseUrl.split("/")[5]
        product_review_url = (
            "https://www."
            + "amazon.in"
            + "/dp/product-reviews/"
            + product_id
            + "?pageNumber={}"
        )

        reviews_dict = {
            "product_id": [],
            "product_fullName": [],
            "product_review_url": [],
            "product_url": [],
            "product_name": [],
            "product_cost": [],
            "product_average_rating": [],
            "review_title": [],
            "review_content": [],
            "review_rating": [],
            "review_date": [],
            "review_location": [],
        }

        start_page = 1
        end_page = None

        try:
            if end_page is None:
                driver.get(product_review_url.format(1))
                no_reviews = driver.find_element(
                    By.XPATH, '//div[@data-hook="cr-filter-info-review-rating-count"]'
                )
                end_page = math.ceil(
                    int(no_reviews.text.split(" ")[3].replace(",", "")) / 10
                )
        except Exception as e:
            print(f"Error determining the number of pages: {e}")
            end_page = 1

        try:
            for j in range(start_page, end_page + 1):
                driver.get(product_review_url.format(j))

                product_fullName = driver.find_element(
                    By.CSS_SELECTOR, 'a[data-hook="product-link"]'
                ).text
                product_url = driver.find_element(
                    By.CSS_SELECTOR, 'a[data-hook="product-link"]'
                ).get_attribute("href")
                product_average_rating = driver.find_element(
                    By.CSS_SELECTOR, 'span[data-hook="rating-out-of-text"]'
                ).text.split(" ")[0]

                try:
                    shall_break = driver.find_element(
                        By.CSS_SELECTOR, ".a-disabled.a-last"
                    ).text

                except NoSuchElementException:
                    shall_break = False

                print(f"Scraping page: {product_review_url.format(j)}")
                content_div = driver.find_element(
                    By.CSS_SELECTOR, ".a-section.a-spacing-none.review-views.celwidget"
                )
                content_html = content_div.get_attribute("outerHTML")
                result = BeautifulSoup(content_html, "html.parser")

                for review_div in result.find_all("div", {"data-hook": "review"}):
                    title, review, attribute, rating, date, country = (
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                    )

                    title_span = review_div.find("a", {"data-hook": "review-title"})
                    if title_span:
                        title = title_span.find_all("span")[-1].text.strip()

                    attribute_span = review_div.find(
                        "span", {"class": "a-profile-name"}
                    )
                    if attribute_span:
                        attribute = attribute_span.text.strip()

                    rating_span = review_div.find(
                        "i", {"data-hook": "review-star-rating"}
                    )
                    if rating_span:
                        rating = rating_span.find("span").text.strip().split(" ")[0]

                    date_span = review_div.find("span", {"data-hook": "review-date"})
                    if date_span:
                        date_text = date_span.text.strip()
                        date_parts = date_text.split(" ")
                        country = date_parts[2]
                        date = " ".join(date_parts[-3:])

                    review_span = review_div.find("span", {"data-hook": "review-body"})
                    if review_span:
                        review = review_span.text.strip()

                    reviews_dict["product_id"].append(product_id)
                    reviews_dict["product_fullName"].append(product_fullName)
                    reviews_dict["product_url"].append(product_url)
                    reviews_dict["product_name"].append(
                        (" ").join(product_fullName.split(" ")[:4])
                    )
                    reviews_dict["product_review_url"] = product_review_url.format(j)
                    reviews_dict["product_cost"].append("")
                    reviews_dict["review_title"].append(title)
                    reviews_dict["review_content"].append(review)
                    reviews_dict["review_rating"].append(rating)
                    reviews_dict["review_date"].append(date)
                    reviews_dict["review_location"].append(country)
                    reviews_dict["product_average_rating"].append(
                        product_average_rating
                    )
                if shall_break:
                    break
            time.sleep(5)

        finally:
            df = pd.DataFrame(reviews_dict)
            while True:
                if os.path.isfile(f"./amazon/{product_id}.csv"):
                    product_id = product_id + "-" + str(int(uniform(1, 100)))
                else:
                    break
            csv_filename = f"./amazon/{product_id}.csv"
            df.to_csv(csv_filename, index=False)
            print(f"Data saved to {csv_filename}")
