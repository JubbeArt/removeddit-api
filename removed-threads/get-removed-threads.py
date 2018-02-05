import requests
import requests.auth
import time
import sys
import pymysql.cursors
import pprint
import random
pp = pprint.PrettyPrinter()

sys.path.append('../')
from config import *
from throwaway import *

def get_token():
  client_auth = requests.auth.HTTPBasicAuth(scriptID, secret)
  post_data = {
    'grant_type': 'password',
    'username': username,
    'password': password
  }

  headers = {'User-Agent': '{}/1.0 by {}'.format(appName, username)}
  response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
  return response.json()['access_token']

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

def get_threads(token, after = ''):
  headers = {'Authorization': 'bearer ' + token, 'User-Agent': '{}/1.0 by {}'.format(appName, username)}
  response = requests.get('https://oauth.reddit.com/r/undelete?limit=1&after={}'.format(after), headers=headers)
  return response.json()

def extract_threads(resp):
  children = resp['data']['children']
  return [child['data'] for child in children]


before = thread['data']['before']

token = get_token()


while True:
  if random.random() < 0.01:
    token = get_token()

  response = get_threads(token)
  after = response['data']['after']
  threads = extract_threads(thread)

  for thread in threads:
    if thread['link_flair_text'] == '[META]':
      continue

    url = thread['url']
    parts = url.split('/')

    

  if after:
    break
  
    #save_to_database()

