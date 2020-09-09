# coding=utf-8

import eyed3
import re, os


class Merge():

    def __init__(self):
        pass

if __name__ == '__main__':
    os.chdir(r'\\RASPBERRYPI\BackUp\Music')
    files = os.listdir(".")
    files.sort()
    print(files)
