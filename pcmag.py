from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import random
import time
import pandas as pd


url = "https://www.pcmag.com/categories/processors/brands/intel?page={}"
path = "./chromedriver.exe"
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run the browser in headless mode
# chrome_options.add_argument("--no-sandbox")  # Bypass the OS security model
# chrome_options.add_argument(
#     "--disable-dev-shm-usage"
# )  # Overcome limited resource problems
# chrome_options.add_argument("--disable-features=InterestCohort")
service = Service(path)
driver = webdriver.Chrome(service=service, options=chrome_options)

parsed_url = urlparse(url)
baseUrl = f"{parsed_url.scheme}://{parsed_url.netloc}"

reviews_dict = {
    "product_url": [],
    "product_name": [],
    "review_title": [],
    "review_content": [],
    "review_rating": [],
    "review_date": [],
}

try:
    for i in range(1, 1 + 1):

        driver.get(url.format(i))
        content_div = driver.find_element(By.ID, "content-river")

        content_html = content_div.get_attribute("outerHTML")
        result = BeautifulSoup(content_html, "html.parser")
        reviews = result.find_all(
            "div",
            class_="flex w-full flex-wrap border-b border-gray-200 py-4 md:flex-nowrap",
        )

        for j in reviews:

            # product link
            lnk = j.find("a")["href"]
            link = baseUrl + lnk
            driver.get(link)

            # Product Name
            title = (
                j.find(
                    "div",
                    class_="font-stretch-ultra-condensed text-base font-semibold leading-compact md:text-xl",
                )
                .text.strip()
                .replace("Review", "")
            )

            # Review Date
            date = j.find("span", class_="mr-3 hidden md:inline-block").text.strip()

            # Review Rating
            rating = j.find("span", class_="ml-1 mr-3").text.strip()

            sub_content_div1 = driver.find_element(
                By.CSS_SELECTOR, ".bottom-line.w-full.pt-6.text-base"
            )
            try:
                sub_content_div2 = driver.find_element(
                    By.CSS_SELECTOR, ".mb-4.leading-normal"
                )
                ttle = sub_content_div2.text.strip()
            except NoSuchElementException:
                ttle = " "

            content = (
                sub_content_div1.text.replace("THE BOTTOM LINE", "")
                .replace("\n", " ")
                .replace(",", " ")
                .strip()
            )

            reviews_dict["product_url"].append(link)
            reviews_dict["review_title"].append(ttle)
            reviews_dict["product_name"].append(title)
            reviews_dict["review_content"].append(content)
            reviews_dict["review_rating"].append(rating)
            reviews_dict["review_date"].append(date)

            print(title)
            time.sleep(random.uniform(1, 5))
            driver.back()

finally:
    df = pd.DataFrame(reviews_dict)
    csv_filename = "reviews.csv"
    df.to_csv(csv_filename, index=False)
    print(f"Data saved to {csv_filename}")
    driver.quit()
