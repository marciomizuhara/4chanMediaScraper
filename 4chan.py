import os
import errno
import time
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from urllib.request import Request
import requests
import re

# Input from the user for the valid 4chan thread link
chan_thread = input('Please insert the URL of the thread you want to scrape: ')

# Input from the user for the directory path to save the media
folder_path = input('Please insert a folder path to save the media (e.g., N:\\TORRENTS\\System\\webms): ')

# Ensure the folder path ends with a slash
if not folder_path.endswith("\\"):
    folder_path += "\\"

# Convert the path to the correct format
folder_path = folder_path.replace("\\", "/")

# Set up the request
my_url = Request(f"{chan_thread}", headers={'User-Agent': 'Mozilla/5.0'})
uClient = uReq(my_url)
time.sleep(0.5)
page_html = uClient.read()
time.sleep(0.5)
uClient.close()

# HTML parsing
page_soup = soup(page_html, "html.parser")


# Function to create directories recursively
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


# Variables to store thread elements
webm = page_soup.findAll("div", {'class': 'file'})
thread_title = page_soup.findAll("span", {'class': 'subject'})

# Scraping the content
counter = 0
try:
    for number in range(len(webm)):
        non_formatted = thread_title[0].getText().strip()  # Remove extra whitespace
        print(non_formatted)
        folder_thread_title = re.sub(r'[^\w\s-]', '', non_formatted).strip()[:30]  # Remove special characters
        webm_link = webm[number].findChild("div", {'class': 'fileText'}).find('a')['href'][2:]
        webm_data = requests.get(f'https://{webm_link}').content
        print(webm_link)
        mkdir_p(f'{folder_path}/{folder_thread_title}')
        with open(f'{folder_path}/{folder_thread_title}/video_{number+1}.webm', 'wb') as handler:
            handler.write(webm_data)
        counter += 1
except IndexError:
    print(f'{counter} media files downloaded successfully!')
