import math
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


amazon_site = "amazon.in"
product_asin = "B09MDJDSGH"

sleep_time = 10
start_page = 1
end_page = None

product_url = (
    "https://www."
    + amazon_site
    + "/dp/product-reviews/"
    + product_asin
    + "?pageNumber={}"
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
}

start_page = 1
end_page = None

try:
    if end_page is None:
        driver.get(product_url.format(1))
        no_reviews = driver.find_element(
            By.XPATH, '//div[@data-hook="cr-filter-info-review-rating-count"]'
        )
        end_page = math.ceil(int(no_reviews.text.split(" ")[3].replace(",", "")) / 10)
except Exception as e:
    print(e)
    end_page = 1

try:
    for j in range(start_page, end_page + 1):

        driver.get(product_url.format(j))
        print(product_url.format(j))
        # raise Exception("No reviews found")
        content_div = driver.find_element(
            By.CSS_SELECTOR, ".a-section.a-spacing-none.review-views.celwidget"
        )
        content_html = content_div.get_attribute("outerHTML")
        result = BeautifulSoup(content_html, "html.parser")

        reviews = result.find_all("div", class_="a-section review aok-relative")
        ## 1. title
        titleOwn = reviews.find_all(
            "a", class_="review-title"
        )  # Find all reviews from own country
        titleAll = reviews.find_all(
            "span", class_="review-title"
        )  # Find all reviews from other countries
        title_lst = []
        for title in titleOwn:
            # print('own',title.find_all('span')[-1].text)
            title_lst.append(title.find_all("span")[-1].text)

        for title in titleAll:
            # print('oth',title.find_all('span')[0].text)
            title_lst.append(title.find_all("span")[0].text)

        ## 2. name
        attribute_lst = []
        attributes = reviews.find_all("span", {"class": "a-profile-name"})
        for attribute in attributes:
            attribute_lst.append(attribute.contents[0])
        name_lst = attribute_lst

        ## 3. rating
        ratingOwn = reviews.find_all("span", class_="a-icon-alt")
        rating_lst = []

        for rating in ratingOwn:
            rating_lst.append(rating.text)
            # rating_lst.append(rating.find_all("span")[0].contents[0])

        ## 4. date
        attribute_lst = []
        attributes = reviews.find_all("span", {"class": "a-profile-name"})
        for attribute in attributes:
            attribute_lst.append(attribute.contents[0])
        date_lst = attribute_lst

        ## 5. content
        contents = reviews.find_all("span", {"data-hook": "review-body"})
        content_lst = []
        for content in contents:
            text_ = content.find_all("span")[0].get_text("\n").strip()
            text_ = ". ".join(text_.splitlines())
            text_ = re.sub(" +", " ", text_)
            content_lst.append(text_)

        # # adding to the main list
        print(date_lst)
        print(name_lst)
        print(title_lst)
        print(content_lst)
        print(rating_lst)

        raise Exception("No reviews found")
finally:
    df = pd.DataFrame(reviews_dict)
    while True:
        if os.path.isfile(f"./amazon/{product_asin}.csv"):
            product_asin = product_asin + "-" + str(int(uniform(1, 100)))
        else:
            break
    csv_filename = f"./amazon/{product_asin}.csv"
    df.to_csv(csv_filename, index=False)
    print(f"Data saved to {csv_filename}")
    driver.quit()
