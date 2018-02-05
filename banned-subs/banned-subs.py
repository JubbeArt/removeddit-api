import requests
import requests.auth
import pathlib
import json
import time 
import sys
import pymysql.cursors

sys.path.append('../')
from config import *

# APPROX 2 requests / sec

inputFile = 'output/quarantined-subs'
startInputRow = int(sys.argv[1])
endInputRow = int(sys.argv[2])

# Throwaway account
username = 'ComprehensiveMeeting'
appName = 'dickbutt'

def make_request(path):
  headers = {'User-Agent': '{}/1.0 by {}'.format(appName, username)}
  response = requests.get('https://api.reddit.com{}'.format(path), headers=headers)
  return response

def save_to_database(subreddit, title):
  connection = pymysql.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    db=DB_NAME,
    autocommit=True
  )

  try: 
    with connection.cursor() as cursor:
      sql = 'INSERT INTO banned_subreddits (name, title) VALUES (%s, %s)'
      cursor.execute(sql, (subreddit, title))
  finally:
      connection.close()

def log_error(subreddit, response):
  errorFile = open('error', 'a')
  errorFile.write('{} - {}\n\n\n'.format(subreddit, response.text))
  errorFile.close()
 
with open(inputFile) as inputF:
  startTime = time.time()  
  inputRows = inputF.readlines()[startInputRow:endInputRow]
  
  for i, subreddit in enumerate(inputRows):
    subreddit_name = subreddit.split('>')[0].strip()
    description =  subreddit.split('>')[1].replace('\n', '')
    tries = 0

    while True:
      try:
        res = make_request('/r/{}/'.format(subreddit_name))
        json = res.json()
        
        if 'reason' in json:
          print('{:<20} {:<14} iter: {:<10} time: {:.1f}'.format(subreddit_name, json['reason'], i, time.time()-startTime))
          
          if json['reason'] == 'banned':
            save_to_database(subreddit_name, description)
          
        # Subreddit was banned/private but is no longer or it has never existed
        elif 'data' in json:
          # do nothing
          _ = None
        # Subreddit was probably permantly deleted by reddit themselves (e.g. /r/Comments and /r/hot)
        else:
          print('{:<20} ERROR: {}'.format(subreddit_name, res.json()))
        break
      except KeyboardInterrupt:
        raise
      except:        
        log_error(subreddit_name, res)
        tries += 1

        if tries >= 5:
          break 

print('Done! Data saved to database')
