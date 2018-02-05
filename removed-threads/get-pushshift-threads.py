import requests
import requests.auth
import time
import sys
import pymysql.cursors
import json

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

def get_threads(fromm):
  query = {
    'query': {
      'bool': {
        'must': [
          { 'match': { 'subreddit': 'undelete' }},
          { 'range': { 'created_utc': { 
            'gte': 1390000000, #1510000000 
            'lte': 1400000000 #1520000000
          }}}      
        ]
      }
    },
    'size': 1000,
    'from': fromm 
  }

  response = requests.get('https://elastic.pushshift.io/rs/submissions/_search?source=' + json.dumps(query))
  return response.json()

def extract_threads(resp):
  children = resp['hits']['hits']
  return [child['_source'] for child in children]


i = 0
counter = 0

while True:
  response = get_threads(i)
  threads = extract_threads(response)

  if not threads:
    break  

  for thread in threads:
    if thread['subreddit'] != 'undelete': 
      print('WRONG SUB!!!!')
      exit()

    if 'link_flair_text' in thread:
      if thread['link_flair_text'] == '[META]':
        continue

    url = thread['url']
    parts = url.split('/')
    if len(parts) < 7:
        continue
    subreddit = parts[4].lower()
    threadID = parts[6]
    utc = int(thread['created_utc'])
    print('{:<22} {:<8} {:<12} {:<5}'.format(subreddit, threadID, utc, counter), end='')
    counter += 1

    try:
      save_to_database(threadID, subreddit, utc)
    except pymysql.err.IntegrityError as e:
      if e.args[0] == 1062:
        print(' - ALREADY IN DATABASE', end='')
      else:
        print()
        print(e)
        exit()

    print()

  i += 1000
  time.sleep(10)    

