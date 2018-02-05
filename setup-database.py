import pymysql.cursors
from config import *

connection = pymysql.connect(
  host=HOST,
  user=USER,
  password=PASSWORD,
  autocommit=True
)

try:
  with connection.cursor() as cursor:
    sql = 'CREATE DATABASE {}'.format(DB_NAME)
    cursor.execute(sql)

  connection.select_db(DB_NAME)

  with connection.cursor() as cursor:
    sql = '''
    CREATE TABLE banned_subreddits (
      name varchar(22) PRIMARY KEY,
      title varchar(300),
      ban_reason varchar(300),
      ban_utc int(10)
    )
    '''
    cursor.execute(sql)

finally:
  connection.close()