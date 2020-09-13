# coding=utf-8
import eyed3
from eyed3.id3 import Tag
from eyed3.mp3 import *
import re, os


class Merge():

    def __init__(self):
        pass


if __name__ == '__main__':
    os.chdir(r'\\RASPBERRYPI\BackUp\Music')
    files = os.listdir(".")
    files.sort()
    #print(files)

    



    # file = eyed3.load("0001.mp3")
    # file = Mp3AudioFile("毛不易_像我这样的人.mp3")
    # file.initTag()
    # file.tag.images.set(3, open(r'毛不易_像我这样的人.jpg', 'rb').read(), 'image/jpeg')
    #
    # file.tag.save()
    # print(files)
