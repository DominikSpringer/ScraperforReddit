
import datetime
import mysql.connector
import logging
import json
import os
from functions import mkdirs
import settings
from functions import dict_from_module

#configure the logger
pipelogger = logging.getLogger('pipeline')
#make a dict from settings.py
setting=dict_from_module(settings)

class Filepipeline(object):
    def __init__(self):
        self.saveTweetPath = setting['savepath']
        mkdirs(self.saveTweetPath)

    def process_data(self, data):
        savepath = os.path.join(self.saveTweetPath, str(datetime.datetime.now())+'.txt')
        if os.path.isfile(savepath):
            pass # skip existing items
        else:
            with open(savepath, 'w') as f:
                json.dump(data, f)
                pipelogger.debug("added entry")

class MySQLpipeline(object):
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(host='localhost',
                                                      database=setting['mysqldb'],
                                                      user=setting['mysqluser'],
                                                      password=setting['mysqlpwd'])
            self.cursor=self.connection.cursor()
            #self.insert= "insert %s(id,text,posted,typ) values(%s, %s, %s, %s)"
            self.insert= "insert into %s(id,text,typ) values(%s,%s,%s)"

            #if self.connection.is_connected():
            #    pipelogger.debug('connection to MySQLDatabase established')
        except mysql.connector.Error as err:
            pipelogger.error(err.msg)
            pipelogger.error('connection to MySQLDatabase couldnt be established')

    def process_data(self, data):
        pipelogger.info('process_item called')
        #values_insert=(item['id'],item['body'],item['created_at'],item['type'])
        values_insert = (setting['mysqltable'], data['id'],'"' + str(data['body'][0]) + '"' , data['type'])
        try:
            pipelogger.debug(self.insert % values_insert)
            self.cursor.execute(self.insert % values_insert)
            self.connection.commit()
        except mysql.connector.Error as err:
            pipelogger.error(err.msg)
            pipelogger.error('value couldnt be inserter into MySQLDatabase')
        else:
            pipelogger.info('line added to MYSQL DB')

'''
def writedata(Institutions, user_agent=setting['USER_AGENT'], lmt=10, sort="new"):
    try:
        reddit = praw.Reddit('justi', user_agent=user_agent)
    except RequestException:
        logging.error("failed to connect to reddit")
        sys.exit()

    with open('reddit_scraper.csv', mode='w') as datafile:
        datawriter = csv.writer(datafile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        all = reddit.subreddit("all")
        print(Institutions)
        print(Institutions[0])
        for inst in Institutions:
            logging.info(inst)
            for i in all.search(inst, limit=lmt, sort=sort):
                print(i.title)
                print(i.id)
                submission = reddit.submission(i.id)
                print(submission.title)
                print(submission.id)
                datawriter.writerow(getAll(reddit, i.id, inst))
'''