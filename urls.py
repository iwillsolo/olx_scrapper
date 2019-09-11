import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from pandas import *
import re
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.common.keys import Keys
from PIL import Image, ImageFont, ImageDraw
from itertools import zip_longest

ShowText = 'I Will Solo'


def draw():
    font = ImageFont.truetype('arialbd.ttf', 15)  # load the font
    size = font.getsize(ShowText)  # calc the size of text in pixels
    image = Image.new('1', size, 1)  # create a b/w image
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), ShowText, font=font)  # render the text to the bitmap
    for rownum in range(size[1]):
        # scan the bitmap:
        # print ' ' for black pixel and
        # print '#' for white one
        line = []
        for colnum in range(size[0]):
            if image.getpixel((colnum, rownum)):
                line.append(' '),
            else:
                line.append('#'),
        print (''.join(line))


options = Options()
options.add_argument("--headless")
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('permissions.default.image', 2)
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
driver = webdriver.Firefox(firefox_profile=firefox_profile, options=options)

x_link = []
d_links = []
d_title = []
d_price = []
d_num = []
draw()
print("Welcome to Olx Scrapping Script\nFeel free to contact me: abdalrahman.gamal.m@gmail.com for any feedback or "
      "for reporting bugs")
n = int(input("how many pages to scrap? "))
user_url = str(input("please enter Url: "))

for i in range(1, n):
    urls = user_url + "?page={}".format(i)
    driver.get(urls)
    elem = driver.find_elements(By.XPATH, '//div[@class="ads__item__info"]/a')
    for element in elem:
        link = element.get_attribute('href')
        x_link.append(link)
for links in x_link:
    driver.get(links)
    d_links.append(links)
    print(links)
    try:
        x_title = driver.find_element_by_class_name('brkword.lheight28').text
        d_title.append(x_title)
        print(x_title)

    except:
        pass
    try:
        x_price = driver.find_element_by_class_name('xxxx-large.margintop7.block.not-arranged').text
        d_price.append(x_price)
        print(x_price)
    except:
        pass
    try:
        # x_num = driver.find_element_by_class_name('icon.inlblk.vtop.b_phone4').click()
        x_num = driver.find_element_by_id("contact_methods").click()
        time.sleep(2)
        f_num = driver.find_element_by_id("contact_methods").text
        f_num = re.sub(r"\s+", "", f_num)
        d_num.append(f_num)
        print(f_num)
        print ('*' * 10)
    except:
        pass

    # print (d_num,d_price,d_title,d_links)
    full_data = list(zip_longest(d_links, d_title, d_price, d_num, fillvalue=None))
    # print (full_data)
    df = pd.DataFrame(full_data, columns=['Links', 'Title', 'Price', 'Phone Number'])
    df.to_csv('cc.csv', encoding='utf-8-sig', index=False)

driver.quit()
