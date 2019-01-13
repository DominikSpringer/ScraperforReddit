# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 10:50:10 2019

@author: Dominik Springer
@email: dominik.springer@hotmail.com
"""
import logging
from logging import config
import os
import sys
import praw
from prawcore.exceptions import RequestException
import settings
from functions import getAll, dict_from_module
#configure the logger
path=os.path.dirname(__file__)
logging.config.fileConfig('logging.ini', defaults={'logfile': 'ScraperforReddit.log','loggname':'nofile'})
logger = logging.getLogger('spider')
#make a dict from settings.py
setting=dict_from_module(settings)
#importing pipelines
pipelineclass = getattr(__import__('pipelines', fromlist=[setting['pipelines']]), setting['pipelines'])


# Please specify which strings to look for and what to use as the user agent.
strings_to_scrape = ["let me find this"]
user_agent = "Sentiment_news v0.1"

def ScraperForReddit(Institutions, useragent=user_agent, lmt=10, sort="new"):
    try:
        reddit = praw.Reddit("MyScraper",user_agent=useragent)
    except RequestException:
        logging.error("failed to connect to reddit")
        sys.exit()
    all = reddit.subreddit("all")
    pipe = pipelineclass ()
    for inst in Institutions:
        logging.info(inst)
        for i in all.search(inst, limit=lmt, sort=sort):
            submission = reddit.submission(i.id)
            dataline = getAll(reddit, i.id, inst)
            pipe.process_data(dataline)

ScraperForReddit(strings_to_scrape)