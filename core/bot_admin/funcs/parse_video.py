import os
import sys
sys.path.insert(0,os.path.join(os.getcwd()))

import bs4
import requests
from fake_useragent import UserAgent
from aiogram import Bot
from database import database


ua = UserAgent()
headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": ua.random
    }



def parse_video(url: str):

    session = requests.session()
    session.headers.update(headers)
    req = session.get(url)
    
    try:
        soup = bs4.BeautifulSoup(req.text,'lxml')
        # with open('index.html', 'w') as f:
        #     f.write(req.text)
        video = soup.source['src']

        with open(r'core/client/temp/video.mp4', 'wb') as f:
            response = session.get(video, stream=True)
            
            for data in response.iter_content(chunk_size=4096):
                f.write(data)

        return True
    
    except Exception as ex:
        print(ex)
        return False




def get_params(url: str) -> dict:
    param_dict = {}
    url_list = url.split('/')
    seria_num = ' '.join(url_list[4:]).replace('.html','').replace('-', ' ')
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
        print(f'Error core\\bot_admin\\funcs\parse_video.py in get_params:\n{ex}')
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
        print(f'Error core\\bot_admin\\funcs\parse_video.py in get_series_urls:\n{ex}')
        return False
    
    

async def fill_channel(url:str, chan_id: str, bot: Bot) -> str:
    urls = get_series_urls(url)

    if not urls:
        return False

    try:
        for url in urls:
            params_dict = get_params('https://jut.su/' + url)

            seria_num = params_dict['seria_num']
            seria_title = params_dict['seria_title']
            text = f"*{seria_num}*\n{seria_title}"
            photo = open('core/bot_admin/temp/poster.jpg')
            
            message = await bot.send_photo(chat_id=int(chan_id), photo=photo, caption=text, parse_mode="MARKDOWN")

            database.insert_seria(table_name=chan_id,msg_id=message.id,seria=seria_num,title=seria_title)

        return "Successfull fill channel!"

    except Exception as ex:
        print(f'Error core\\bot_admin\\funcs\parse_video.py in fill_channel:\n{ex}')
        return False





if __name__ == '__main__':
    # get_series_urls('https://jut.su/life-no-game/')
    get_params('https://jut.su/fullmeetal-alchemist/season-1/episode-1.html')
    # get_params('https://jut.su/life-no-game/episode-1.html')
