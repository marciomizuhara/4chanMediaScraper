import os, os.path
import errno
import time
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from urllib.request import Request
import requests
import regex as re


# Input user for valid 4chan thread link
chan_thread = input('Please insert the url of the thread you want to scrap: ')
# Input user for a folder path to save the media
folder_path = input('Please insert a folder path to save the media: ')
folder_path.replace("\\","/")


# Set up requests
my_url = Request(f"{chan_thread}", headers={'User-Agent': 'Mozilla/5.0'})
uClient = uReq(my_url)
time.sleep(0.5)
page_html = uClient.read()
time.sleep(0.5)
uClient.close()


# html parsing
page_soup = soup(page_html, "html.parser")


# Folder creation function
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


# Variables
webm = page_soup.findAll("div",{'class': 'file'})
thread_title = page_soup.findAll("span",{'class': 'subject'})


# Scrap the content
counter = 0
try:
    for number in range(500):
        non_formatted = thread_title[0].getText()
        folder_thread_title = re.sub('[/|!:,*)@#%(&$_?.^  ]', ' ', non_formatted)[:30]
        webm_link = webm[number].findChild("div",{'class': 'fileText'}).find('a')['href'][2:]
        webm_data = requests.get(f'https://{webm_link}').content
        mkdir_p(f'{folder_path}/{folder_thread_title}')
        with open(f'{folder_path}/{folder_thread_title}/video_{number+1}.webm','wb') as handler:
            handler.write(webm_data)
        counter = counter + 1
except IndexError:
    print(f'{counter} media downloaded successfully!')
