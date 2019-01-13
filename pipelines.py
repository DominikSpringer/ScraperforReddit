
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
            self.connection = mysql.connector.connect(host=setting["mysqlip"],
                                                      database=setting["mysqldb"],
                                                      user=setting["mysqluser"],
                                                      password=setting["mysqlpwd"])
            self.cursor=self.connection.cursor()
            #self.insert= "insert %s(id,text,posted,typ) values(%s, %s, %s, %s)"
            self.insert= "insert into %s(id,text, posted, typ) values(\"%s\", \"%s\", \"%s\",\"%s\")"
            #if self.connection.is_connected():
            #    pipelogger.debug('connection to MySQLDatabase established')
        except mysql.connector.Error as err:
            pipelogger.error(err.msg)
            pipelogger.error('connection to MySQLDatabase couldnt be established')

    def process_data(self, data):
        pipelogger.info('process_item called')
        #values_insert=(item['id'],item['body'],item['created_at'],item['type'])
        for line in data:
            if isinstance(line,dict):
                pass
            else:
                line = json.loads(line)
            id = line["id"]
            body = str(line["body"][0])
            posted = line["tstamp"]
            type = line["type"]


            values_insert = (setting["mysqltable"], id, body, posted , type)
        try:
            pipelogger.debug(self.insert % values_insert)
            self.cursor.execute(self.insert % values_insert)
            self.connection.commit()
        except mysql.connector.Error as err:
            pipelogger.error(err.msg)
            pipelogger.error('value couldnt be inserter into MySQLDatabase')
        else:
            pipelogger.info('line added to MYSQL DB')
