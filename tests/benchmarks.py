__author__ = 'Lucas Ou-Yang'

from lib.web import fb_shares, top_image
from time import time
import requests


def run_1():
    """"""

    # print fb_shares('http://foxnews.com/sdfdsg\'sdfgas\'fasd')

    s1 = time()
    for i in range(10):
       print fb_shares('http://foxnews.com')
    print 'this took %d seconds' % ((time()-s1))


def run_2():
    """"""

    html = requests.get('http://cnn.com').text
    img_url = top_image(html)
    print img_url



if __name__ == '__main__':
    # run_1()
    run_2()