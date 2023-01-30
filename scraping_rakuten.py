from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import time
import openpyxl
import re

"""
Scraping books.rakuten.co.jp
"美容・暮らし・健康・料理"ジャンルの評価数でソートされている。
 1. Click "もっと見る" button
 2. Get article's data (title, link, date)
"""

driver = webdriver.Chrome()
url = 'https://books.rakuten.co.jp/search?g=001010&e=5&s=7&h=50&l-id=search-c-number-02'
wait = WebDriverWait(driver, 10)
driver.get(url)

# Get 7 info
html = driver.page_source.encode('utf-8')
soup = BeautifulSoup(html, "lxml")

divs = soup.find_all("div",class_="rbcomp__item-list__item")
export_list = []

for div in divs:

    title = div.find(class_="rbcomp__item-list__item__title").text

    h3_link = div.find(class_="rbcomp__item-list__item__details__lead")
    link = h3_link.find("a").get("href")

    if div.find(class_="rbcomp__item-list__item__author") is not None:
        p_author = div.find(class_="rbcomp__item-list__item__author")
        author = p_author.find("a").text

    div_review = div.find(class_="rbcomp__item-list__item__review")
    review = div_review.find("em").text
    num_review = re.sub(r"\D", "", div_review.find("a").text[4:9])

    date = div.find_all(class_="rbcomp__item-list__item__subtext")[-1].text.split("／")[0][:-3]

    p_price = div.find(class_="rbcomp__item-list__item__price")
    price = p_price.find("em").text

    temp = []
    temp.append(title)
    temp.append(link)
    temp.append(author)
    temp.append(review)
    temp.append(num_review)
    temp.append(date)
    temp.append(price)

    export_list.append(temp)

driver.close()
driver.quit()

# Write to excel
wb = openpyxl.load_workbook('PRTIMES.xlsx')
sheet = wb['Sheet1']
for i in range(len(export_list)):
    for j in range(7):
        sheet.cell(row=i+1, column=j+1, value=export_list[i][j])
wb.save('PRTIMES.xlsx')

print("complete")


