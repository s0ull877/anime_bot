import os
import sys
sys.path.insert(0,os.path.join(os.getcwd()))

import bs4
import requests
from fake_useragent import UserAgent
import re
import config
from aiogram import types

ua = UserAgent()
headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": ua.random
    }
    

# мне лень переписывать заполнения строки в таблице
def get_desc(url: str) -> None:

    session = requests.session()
    session.headers.update(headers)
    req = session.get(url)

    soup = bs4.BeautifulSoup(req.text,'lxml')
    
    text = str(soup.find('p', class_='under_video').find('span'))
    text = re.sub(r'<br/>', '\n', text)
    cleaned_text = re.sub(r'<i>.*?</i>', '', text)
    
    desc = bs4.BeautifulSoup(cleaned_text,'lxml').text
    
    return desc


if __name__ == '__main__':
    rework('https://jut.su/ninja-kamui/')
