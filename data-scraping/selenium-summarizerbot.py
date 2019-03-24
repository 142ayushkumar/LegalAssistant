# mkdir summary keywords keyfragments
from selenium import webdriver
import sys
import time
from os import listdir,walk,path
from os.path import isfile, join
import sys
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import pandas as pd
from selenium.webdriver.common.keys import Keys



username = ""
password = ""

browser = webdriver.Firefox()
browser.get('https://opensoft19.slack.com/messages/DH2S1SKCM/')
username = browser.find_element_by_id('email')
password = browser.find_element_by_id('password')
username.send_keys(username)
password.send_keys(password)
browser.find_element_by_id("signin_btn").click()

time.sleep(5)

bot = browser.find_element_by_xpath("//a[@aria-label='summarizebot (direct message, active)']")
bot.click()

links = pd.read_csv("final-store.csv")
x = int(len(links.index))


for i in range(0, 5000):
	url = links['link'][i]
	filename = links['filename'][i]
	message = "'" + url + "'"
	browser.execute_script(f"document.getElementsByClassName('ql-editor')[1].innerHTML = {message}")
	browser.execute_script("TS.view.submit()")
	time.sleep(5)
	bot = browser.find_elements_by_xpath("//a[@data-qa='message_attachment_title_link']")
	# Ignore SSL certificate errors
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE

	url = bot[-1].get_attribute('href')
	html = urlopen(url, context=ctx).read()
	soup = BeautifulSoup(html, "html.parser")

	#print(soup.prettify())
	sys.stdout = open("summary\\" + filename, 'w+')
	summary = soup.find_all("p")
	print(summary.prettify())


	sys.stdout = open("keywords\\" + filename, 'w+')
	keywords = soup.find_all('span', { 'class' : 'keyword_item'})
	for x in keywords:
	    print(x.text)

	sys.stdout = open("keyfragments\\" + filename, 'w+')
	keyfragments = soup.find_all('span', { 'class' : 'bullet_item'})
	for x in keyfragments:
	    print(x.text)
