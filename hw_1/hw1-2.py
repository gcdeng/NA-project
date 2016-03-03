#! /usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2, urllib, json, re, argparse, requests
from pprint import pprint
from bs4 import BeautifulSoup

def get_title(results, number):
    titles=[]
    # print results.find_all('h3').a
    for header in results.find_all('h3'):
        for title in header.a:
            # print title
            titles.append(title)

    i=0
    while i<number:
        print titles[i] #all title in page
        i+=1

def get_link(results, number):
    links=[]
    youtubeUrl = "https://www.youtube.com/"
    # print results.find_all('h3').a
    for link in results.find_all('h3'):
        links.append(link.a.get('href'))

    i=0
    while i<number:
        completeUrl=youtubeUrl+links[i] #all title in page
        print completeUrl
        i+=1

def get_description(results, number):
    description = results.find_all("div", "yt-lockup-description")
    i=0
    while i<number:
        print(description[i].string)
        i+=1

if __name__ == '__main__':
    argPrser = argparse.ArgumentParser(description='Process youtube search crawler argument.')
    argPrser.add_argument('-n', help="number of search result. default is 5", metavar="number", type=int, default=5)
    argPrser.add_argument('-p', help="page that you parse", metavar="page", type=int, default=1)
    argPrser.add_argument('keyword', help="search term", type=str, nargs=1)
    args = argPrser.parse_args()
    # print args

    # Process args
    term = args.keyword[0]
    # print term
    page = str(args.p)
    number = args.n

    # get html
    url = "https://www.youtube.com/results?search_query=" + term + "&page=" + page
    html = requests.get(url)
    # print html.text

    # BeautifulSoup
    soup = BeautifulSoup(html.text)
    # print soup.prettify()
    results = soup.find(id="results")


    get_description(results, number)
    # get_link(results, number)
    # get_title(results, number)
