import re
import sys
from zipfile import ZipFile
import os

import requests
from html2text import HTML2Text
import inspect
BASE_URL = 'http://www.yifysubtitles.com'

def get(url):
    '''Retrieve page content and use html2text to convert into readable text.'''
    # get webpage content for this url
    r = requests.get(url)
    # raise exception if status code is not 200
    r.raise_for_status()

    # use html2text to transfer html to readable text
    h = HTML2Text()
    h.ignore_links = False
    text = h.handle(r.text)

    return text
def search_subtitle(query):
    import urllib
    print('''Search subtitle by query in parameter.''')
    #text = get('{}/search?q={}'.format(BASE_URL, query))
    print(f'your query is {query}')
    text=get(BASE_URL+'/search?'+urllib.parse.urlencode({'q':query}))
    # try to find subtitle link in this page
    m = re.search(r'(\/movie-imdb\/.+)\)', text)
    if m:
        print('match')
        # call get_subtitles() to get all available subtitles
        print('m group1',m.group(1))
        get_subtitles('{}{}'.format(BASE_URL, m.group(1)))
    
global global_text
global_text=''
def get_subtitles(url):
    '''Find all subtitles url for the movie.'''
    # get webpage content for this url
    print('movie url,',url)
    text = requests.get(url)
    text=text.text
#     with open('movie_url.txt','w') as f:
#         f.write(text)
    # save english subtitles
    subs = []
    # print('texy',text)
    # print('total lines',len(text.splitlines()))
    i=0
    global m
    for line in text.splitlines():
        #print(line)
        # find upvote count, subtitle language and subtitle link
        #m = re.search(r'upvote(\d+).+\[(\w+) subtitle.*\((.*?)\)', line)
        #m=re.search(r'/subtitles/.+-english-yify-\d+',line)
        m=re.search(r'/subtitles/[^\s\"]+\-english\-yify-\d+',line)
        if not m:
            continue
        
        
        
        #upvote, language, link = m.group(1), m.group(2), m.group(3)
        link=m.group(0)
        
        # we only want english subtitle
    #     if language == 'English':
    #         subs.append({
    #             'up': upvote,
    #             'link': link
    #         })
    # # sort list by upvote count
    # subs.sort(key=lambda x: int(x['up']), reverse=True)

    # only download subtitle which has the most upvote count
    get_subtitle(link)

def get_subtitle(url):
    '''Download the specific subtitle.'''
    #print('our_url {}{}'.format(BASE_URL, url))
    text = get('{}{}'.format(BASE_URL, url))


    #m = re.search(r'\[Download subtitle\]\((.*\n.*)\)', text)
    m=re.search(r'https://www.yifysubtitles.com/subtitle/.+zip',text, flags=re.DOTALL)
    if m:
        
        # remove all newline
        # link = m.group(1).replace('\n', '')
        link = m.group(0).replace('\n','')
        print('Download {}'.format(link))

        # use last part of url as file name
        filename = 'sample.zip'#link.split('-')[-1]

        # save the file to current directory
        print('link',link)
        print('filename',filename)
        print('space in link', ' ' in link)
        with open(filename, 'wb') as f:
            f.write(requests.get(link).content)

        # extr0act subtitles from zip file
        
        with ZipFile(filename) as zf:
            zf.extractall()

        # after extracting subtitles, remove zip file
        os.remove(filename)
    else:
        print("no match")
if __name__=='__main__':
    print('working directory',os.getcwd())
    
    print(" ".join(sys.argv[1:]))
    search_subtitle(" ".join(sys.argv[1:]))
    
