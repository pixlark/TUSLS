import praw
import re
import urllib
import os
import time
import sys

from account import *

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     password=password,
                     user_agent='TUSLS link scraper @ http://pixlark.github.io/',
                     username=username)

def get_submissions(sub, category, num):
    if   (category == 'top'):
        return sub.top(limit=num)
    elif (category == 'hot'):
        return sub.hot(limit=num)
    elif (category == 'controversial'):
        return sub.controversial(limit=num)
    elif (category == 'gilded'):
        return sub.gilded(limit=num)
    else:
        raise RuntimeError('No such category \'{0}\'.'.format(category))

def scrape_sub_links(sub_name, category, num, regex):
    link_file = open(sub_name + '.txt', 'w')
    sub = reddit.subreddit(sub_name)
    submission_list = get_submissions(sub, category, num)
    for submission in submission_list:
        if regex == None or re.search(re.compile(regex), submission.title):
            #print('\033[1K\r', end='')
            #print('Downloading', submission.title, '...', end='')
            #sys.stdout.flush()
            link_file.write(submission.title + '\n' + submission.url + '\n\n')
    link_file.close()

def scrape_sub(sub_name, category, num, regex, file_types):
    sub = reddit.subreddit(sub_name)
    if (not os.path.isdir(sub_name)):
        os.mkdir(sub_name)
    submission_list = get_submissions(sub, category, num)
    for submission in submission_list:
        ascii_name = submission.title.encode('ascii', errors='ignore').decode()
        file_name = re.sub(re.compile(r'(\<|\>|\:|\"|\/|\\|\||\?|\*)'), '', ascii_name)
        if regex == None or re.search(re.compile(regex), submission.title):
            if (re.match(re.compile(file_types), submission.url.split('.')[-1])):
                #print('\033[1K\r', end='')
                #print('Downloading', submission.title, '...', end='')
                #sys.stdout.flush()
                try:
                    urllib.request.urlretrieve(submission.url,
                                               sub_name + '/' + 
                                               file_name +
                                               '.' + submission.url.split('.')[-1])
                except OSError:
                    print("The image at {0} could not be downloaded".format(submission.url))
