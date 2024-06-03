import requests
from bs4 import BeautifulSoup

class PinterestVideo:
    def __init__(self, url):
        self.url = url

    def get_video_url(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        video_url = soup.find('video')['src']
        return requests.get(video_url, stream=True)