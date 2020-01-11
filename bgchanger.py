import requests
import urllib.request
import ctypes
import os
import queue as Queue
from time import sleep


def storeImage(url, fileName):
    open(fileName, "wb").write(urllib.request.urlopen(url).read())


def setImageAsBG(image_path):
    image = os.path.join(image_path)
    print(image)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image, 0)


def bgChanger(url, q):
    try:
        res = requests.get(url=url)
        data = res.json()
        url = data["urls"]["full"]
        fileName = data["id"]
        img_path = os.getcwd() + '\\'
        storeImage(url, fileName)
        setImageAsBG(img_path + fileName)
        q.put(fileName)
        if(q.qsize() >= 5):
            i = 0
            while(i < 4):
                os.remove(img_path + q.get())
                i += 1
    except requests.exceptions.RequestException as e:
        print(e)


def main():
    api_key = '126dd8010ccd2ee35ed15fb5f5020ea54323cef125297fb0d0dd3863002ce74d'

    url = 'https://api.unsplash.com/photos/random/?client_id=' + api_key

    q = Queue.Queue()

    while True:
        bgChanger(url, q)
        sleep(1440.0)


if __name__ == '__main__':
    main()
