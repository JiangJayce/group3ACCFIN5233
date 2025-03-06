import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import re
import pandas as pd

def convert_chinese_number(num_str):
    match = re.match(r"([\d.]+)(万?)", num_str)
    if match:
        number = float(match.group(1))  
        unit = match.group(2) 
        if unit == "万":
            return int(number * 10000) 
        return int(number)  
    return None  


def getHtml(url):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; LCTE; rv:11.0) like Gecko'}
    try:
        r=requests.get(url,headers=header)
        r.encoding='utf-8'
        #print(r.status_code)
        r.raise_for_status()
        return r.text 
    except:
        getHtml(url)


chrome_options = Options()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://guba.eastmoney.com/list,zssh000001_2.html"
driver.get(url)
search_keyword = "医疗器械"  
search_box = driver.find_element(By.CLASS_NAME, "list_search")  
search_box.clear()  
search_box.send_keys(search_keyword)
time.sleep(5)


search_button = driver.find_element(By.CLASS_NAME, "searchimg")  
search_button.click()  
time.sleep(5)

for page in range(5): 
    listitem=driver.find_elements(By.CLASS_NAME,'listitem')
    for i in listitem:
        read = convert_chinese_number(i.find_element(By.CLASS_NAME, "read").text)
        reply = i.find_element(By.CLASS_NAME, "reply").text
        title_element = i.find_element(By.CLASS_NAME, "title").find_element(By.TAG_NAME, "a")
        title = title_element.text
        link = title_element.get_attribute("href")
        commentHtml=getHtml(link)
        soup = BeautifulSoup(commentHtml, "html.parser")
        try:
            like_count = soup.find("span", class_="zancout text-primary").text.strip()
        except:
            try:
                like_count = soup.find("span", class_="likemodule").text.strip()
            except:
                like_count = soup.find("div", {"id": "like_wrap"})["data-like_count"]
        
        date = i.find_element(By.CLASS_NAME, "update").text.split(" ")[0]


        author = i.find_element(By.CLASS_NAME, "nametext").text
        userUrl= i.find_element(By.CLASS_NAME, "nametext").get_attribute("href")
        driver.execute_script("window.open(arguments[0]);", userUrl)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)
        fan_button = driver.find_element(By.XPATH, '//li[@class="head_nav" and @tracker-eventcode="person.top.followtab"]/a')        
        fan_button.click()
        time.sleep(2)
        fan_element=driver.find_element(By.XPATH,'//a[@href="#tafans"]')
        fan = fan_element.text  
        fan = re.search(r"\d+", fan).group()
        time.sleep(2)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        data=[{'read':read,'reply':reply,"title":title,"date":date,"like_count":like_count,'fan':fan}]
        df = pd.DataFrame(data)
        df.to_csv('data.csv', mode='a', header=False,index=False)


    try:
        next_button = driver.find_element(By.CLASS_NAME, "nextp")  
        next_button.click()
        time.sleep(10)
    except:
        driver.quit()



