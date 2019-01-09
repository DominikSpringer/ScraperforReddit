# ScraperforReddit
Scraper for Reddit using Reddit's API to retreive data

# Introduction
This scraper searches reddit for subreddits containing the strings provided.
It then retrieves the title and comments of those subreddits.

To be able to run this scraper please first **register a Reddit API**. This takes no more than 5 minutes and is free.
In order to do so, do the following steps:
1. login to your reddit account
2. go to: https://www.reddit.com/prefs/apps and register your application 
3. note down the client_id (14 character string) and the client_secret

# Get it running
After having registered an Reddit API (see Introduction above): 
1. open **settings.py** of this directory and fill in:
    what pipeline to use \
    **pipelines** = 'Filepipeline' #'MySQLpipeline'

    Specify the path to store output at in case you set pipeline = 'Filepipeline' above \
    **savepath** = 'path to save the output to'

    Specify a MySQL database in case you set pipeline = 'MySQLpipeline' above \
    **mysqluser** = '' \
    **mysqlpwd** = '' \
    **mysqldb** = '' \
    **mysqltable** = '' \
3. Open **praw.ini** and fill in Reddit related stuff \
    **user** = your Reddit username \
    **password** = your Reddit password  \
    **clientid** = client ID \
    **clientsecret** = client secret
3. In scraper_for_reddit.py fill the **strings_to_scrape** with a list of strings you want to look for and \
    specify the **user_agent** 
2. **run scraper_for_reddit.py**

# Disclaimer
This programm was brought to you by Dominik Springer

# License
This software is licenced under the GNU General Public License v3.0


  


