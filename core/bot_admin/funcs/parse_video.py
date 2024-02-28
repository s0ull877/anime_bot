import bs4
import requests
from fake_useragent import UserAgent

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