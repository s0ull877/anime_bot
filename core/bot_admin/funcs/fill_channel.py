import os
import sys
sys.path.insert(0,os.path.join(os.getcwd()))

import bs4
import requests
from aiogram.types import InputFile
from fake_useragent import UserAgent
from aiogram import Bot
from database import database
import config
import time

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
        print(f'Error core/bot_admin/funcs/parse_video.py in get_params:\n{ex}')
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
    
    

async def fill_channel(url:str, chan_id: str,  chan_name: str, bot: Bot) -> str:
    row_id = 0
    urls = get_series_urls(url)

    if not urls:
        return fr'Error core/bot_admin/funcs/parse_video.py in get_series_urls'

    try:
        for url in urls:
            params_dict = get_params('https://jut.su/' + url)
            if params_dict:
                row_id +=1
                seria_num = params_dict['seria_num']
                seria_title = params_dict['seria_title']
                text = f"<b>{seria_num}</b>\n{seria_title}"
                photo = InputFile('core/bot_admin/temp/poster.jpg')

                message = await bot.send_photo(chat_id=int(chan_id), photo=photo, caption=text,parse_mode='HTML')
                database.insert_seria(table_name=chan_name,msg_id=message.message_id,seria=seria_num,title=seria_title,rowid=row_id)
                time.sleep(1)
            else:
                return f'Bad params with link https://jut.su/{url}'

        return "Successfull fill channel!"

    except Exception as ex:
        text = f'Error core/bot_admin/funcs/parse_video.py in fill_channel:\n{ex}'
        return text





if __name__ == '__main__':
    print(get_series_urls('https://jut.su/life-no-game/'))
    # get_params('https://jut.su/fullmeetal-alchemist/season-1/episode-1.html')
    # get_params('https://jut.su/life-no-game/episode-1.html')
