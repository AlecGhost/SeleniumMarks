from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import requests
import os
from dotenv import load_dotenv

# get login data from environment variables
load_dotenv()
username = os.environ.get('THM_USERNAME')
password = os.environ.get('THM_PASSWORD')
api_key = os.environ.get('SELENIUM_MARKS_API_KEY')
ip_address = os.environ.get('IP_ADDRESS')


#setup driver
chrome_driver_path = "../chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

# login to THM ecampus
driver.get("https://ecampus.thm.de/service/pages/cs/sys/portal/hisinoneStartPage.faces?chco=y")

email_field = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[1]/div[4]/div[1]/form[1]/input[3]')
email_field.send_keys(username)
password_field = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[1]/div[4]/div[1]/form[1]/input[4]')
password_field.send_keys(password)
password_field.send_keys(Keys.ENTER)

#go to marks page
driver.get("https://ecampus.thm.de/service/pages/cs/sys/portal/hisinoneIframePage.faces"
           "?id=qisstudnoten&navigationPosition=thmqisstudposlsf%2Clink_qisstudnoten&recordRequest=true")

driver.switch_to.frame("frame_iframe_qisstudnoten")
link_bachelor = driver.find_element_by_xpath('//*[@id="wrapper"]/div/div[1]/form/ul/li/a[1]')
link_bachelor.click()
link_info = driver.find_element_by_xpath('//*[@id="wrapper"]/div/div[1]/form/ul/li/ul/li/a[1]/img')
link_info.click()

# scan data
table = driver.find_element_by_xpath('//*[@id="wrapper"]/div/div[1]/form/table[2]/tbody')
table_headers = driver.find_elements_by_class_name("tabelleheader")
entries = table.find_elements_by_class_name("tabelle1")

# generate json from data
marks = []
index = 0
row = {}
for entry in entries:
    if index > 9:
        marks.append(row)
        row = {}
        index = 0
    row[table_headers[index].text] = entry.text
    index = index + 1

driver.quit()


# compare current data with existing data
def compare():
    with open('marks.json', 'r') as f:
        current_data = json.load(f)
        return current_data == marks


# if changes where made, send them to local server
if not compare():
    with open('marks.json', 'w') as f:
        json.dump(marks, f)
requests.post(f"http://{ip_address}/add",
              json=marks,
              params={
                  "username": "SeleniumMarks",
                  "api-key": api_key,
                  "subject": "New Marks"
              })
print("New marks added.")
