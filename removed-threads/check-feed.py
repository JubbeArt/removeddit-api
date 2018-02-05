import requests
import time
import sys
import pymysql.cursors

sys.path.append('../')
from config import *

def save_to_database(threadID, subreddit, utc):
  connection = pymysql.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    db=DB_NAME,
    autocommit=True
  )

  try: 
    with connection.cursor() as cursor:
      sql = 'INSERT INTO removed_threads (thread_id, subreddit, utc) VALUES (%s, %s, %s)'
      cursor.execute(sql, (threadID, subreddit, str(utc)))
  finally:
      connection.close()


# Throwaway account
username = 'ComprehensiveMeeting'
appName = 'dickbutt'

url = 'https://www.reddit.com/r/undelete/new.json?limit=10'
headers = {'User-Agent': '{}/1.0 by {}'.format(appName, username)}

while True:
  # Check every 5 min
  time.sleep(60*5)
  print('-- CHECKING --')
  res = requests.get(url, headers=headers).json()
  threads = res['data']['children']
  threads = [thread['data'] for thread in threads]

  for thread in threads:  
    if thread['link_flair_text'] != '[META]':
      parts = thread['url'].split('/')

      if len(parts) < 7:
        print('SOMETHING WRONG WITH URL:', parts, flush=True)
        continue

      subreddit = parts[4]
      threadID = parts[6]
      utc = int(thread['created_utc'])

      print('{:<22} {:<8} {:<5}'.format(subreddit, threadID, utc), end='', flush=True)
      try:
        save_to_database(threadID, subreddit, utc)
      except pymysql.err.IntegrityError as e:
        if e.args[0] == 1062:
          print(' - ALREADY IN DATABASE', end='')
        else:
          print()
          print(e)      
      print()
