import falcon
import json
import pymysql.cursors
from config import *

class RemovedThreads:
  def on_get(self, req, resp):
    resp.set_header('Access-Control-Allow-Origin', '*')

    connection = pymysql.connect(
      host=HOST,
      user=USER,
      password=PASSWORD,
      db=DB_NAME,
      cursorclass=pymysql.cursors.DictCursor
    )

    subreddit = req.get_param('subreddit')    
    page = req.get_param('page', default=0)
    
    try:
      page = int(page)
    except:
      error = {
        'error': 'Page parameter needs to be a integer, got: {}'.format(page)
      }
      resp.body = json.dumps(error)
      return
    
    offset = page * 100

    try:
      with connection.cursor() as cursor:
        sql = 'SELECT `thread_id` FROM `removed_threads` '
        args = None

        if subreddit:
          sql += ' WHERE `subreddit`=%s '
          args = (subreddit.lower(), offset)        
        else:
          args = (offset,)
          
        sql += ' ORDER BY utc DESC LIMIT %s, 100 '
        cursor.execute(sql, args)
        result = cursor.fetchall()
        resp.body = json.dumps([row['thread_id'] for row in result])

    except Exception as e:
      error = {
        'error': str(e)
      }
      resp.body = json.dumps(error)
      resp.status = falcon.HTTP_500
    finally:
      connection.close()
