import bs4
import requests
import re
from fake_useragent import UserAgent

ua = UserAgent()
headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": ua.random
    }

## will be in bot
# def parse_video(url: str):

#     session = requests.session()
#     session.headers.update(headers)
#     req = session.get(url)
    
#     try:
#         soup = bs4.BeautifulSoup(req.text,'lxml')
#         # with open('index.html', 'w') as f:
#         #     f.write(req.text)
#         video = soup.source['src']

#         with open(r'core/client/temp/video.mp4', 'wb') as f:
#             response = session.get(video, stream=True)
            
#             for data in response.iter_content(chunk_size=4096):
#                 f.write(data)

#         return True
    
#     except Exception as ex:
#         print(ex)
#         return False

def valid_url_for_chan(msg: str):
    msg_list = msg.split(' ')
    
    if len(msg_list) != 2:
        return "Неправильный ввод команды: \n`/create_chan` {ссылка на аниме}"
    
    url = msg_list[-1]
    pattern = r"https://jut\.su/.*/"

    if not re.match(pattern, url):
        return 'Некорректная ссылка. Нужна ссылка типа https://jut.su/anime_name/'

    session = requests.session()
    session.headers.update(headers)
    req = session.get(url)
    soup = bs4.BeautifulSoup(req.text,'lxml')

    if req.status_code != 200:
        return f'status code: {req.status_code}'

    if soup.h1.text[:8] != 'Смотреть':
        return 'Это вроде не ссылка на просмотр аниме.'

    return url


def parse_params(url: str):

    session = requests.session()
    session.headers.update(headers)
    req = session.get(url)

    try:
        soup = bs4.BeautifulSoup(req.text,'lxml')
        img_div = soup.find('div', class_= 'all_anime_title')['style']
        ptr = re.search("http.*[']",img_div)

        img_link = img_div[ptr.start():ptr.end()-1]
        tg_me = 'S0_' + img_link.split('/')[-1][:-4]
        tg_me = tg_me.replace('-','_')
        
        name = soup.h1.text[9:]
    

        # print(name, '\n', tg_me, '\n', img_link)
        response = session.get(img_link)
        with open (r'core/client/temp/image.jpg', 'wb') as ph:
            ph.write(response.content)
        
        return name, tg_me

    except Exception as ex:
        print(ex)
        return False

    



if __name__ == '__main__':
    print(parse_params('https://jut.su/berserk/'))