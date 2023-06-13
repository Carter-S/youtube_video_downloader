from pytube import YouTube

class YoutubeVideo():
    def __init__(self, link):
            self.video = YouTube(link)
