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


def get_params(url: str) -> dict:
    param_dict = {}
    url_list = url.split('/')
    seria_num = ' '.join(url_list[5:]).replace('.html','').replace('-', ' ')
    seria_num = seria_num.replace('season', 'Сезон').replace('episode','Серия')
    param_dict['seria_num'] = seria_num

    try:
        session = requests.session()
        session.headers.update(headers)
        req = session.get(url)

        soup = bs4.BeautifulSoup(req.text,'lxml')
        param_dict['seria_title'] = soup.h2.text

        poster_url = soup.find('video', id='my-player').get('poster')

        response = session.get(poster_url)
        with open('core/bot_admin/temp/poster.jpg', 'wb') as f:
            f.write(response.content)

        return param_dict


    except Exception as ex:
        print(f'Error core/bot_admin/funcs/parser.py in get_params:\n{ex}')
        return False



def get_series_urls(url:str) -> list:
    try:
        session = requests.session()
        session.headers.update(headers)
        req = session.get(url)

        soup = bs4.BeautifulSoup(req.text,'lxml')

        links = soup.find('div', class_='watch_l').find_all('a')

        urls_list = [] 

        for link in links:
            url = link.get('href')
            if '/episode' in url:
                urls_list.append(url)

        return urls_list

    except Exception as ex:
        print(ex)
        return False
    

# мне лень переписывать заполнения строки в таблице
def rework(url: str) -> None:

    session = requests.session()
    session.headers.update(headers)
    req = session.get(url)

    soup = bs4.BeautifulSoup(req.text,'lxml')
    
    text = str(soup.find('p', class_='under_video').find('span'))
    text = re.sub(r'<br/>', '\n', text)
    cleaned_text = re.sub(r'<i>.*?</i>', '', text)
    
    desc = bs4.BeautifulSoup(cleaned_text,'lxml').text
    
    print(desc)
    # await


async def get_decription(message:types.Message) -> None:

    session = requests.session()
    session.headers.update(headers)
    req = session.get('https://jut.su/tomodachi-game/')

    soup = bs4.BeautifulSoup(req.text,'lxml')
    
    text = str(soup.find('p', class_='under_video').find('span'))
    text = re.sub(r'<br/>', '\n', text)
    cleaned_text = re.sub(r'<i>.*?</i>', '', text)
    
    desc = bs4.BeautifulSoup(cleaned_text,'lxml').text

    await message.answer(desc, parse_mode='HTML')


if __name__ == '__main__':
    rework('https://jut.su/ninja-kamui/')
