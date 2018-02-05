from lxml import html
import requests
import pathlib
import json
import dateutil.parser
import time 
import sys

inputFile = '../output/banned-subs'
outputFolder = '../output'
outputFile = 'banned-subs-info'

if len(sys.argv) >= 3:
  inputFile = sys.argv[1]
  outputFile = sys.argv[2]

outputPath = pathlib.PurePath(outputFolder, outputFile)
pathlib.Path(outputFolder).mkdir(parents=True, exist_ok=True)

# Throwaway account
username = 'ComprehensiveMeeting'
appName = 'dickbutt'

def scrape(subreddit):
  headers = {
    'User-Agent': '{}/1.0 by {}'.format(appName, username),
    'Accept-Language': 'en-US'    
  }
  response = requests.get('https://www.reddit.com/r/{}/'.format(subreddit), headers=headers)
  tree = html.fromstring(response.content)  
  info = tree.xpath('//div[@class="md"]')[0]
  banReason = html.tostring(info[1]).strip()
  utc = None

  try:
    banDate = info[2].xpath('//time')[0].get('datetime')
    date = dateutil.parser.parse(banDate)
    utc = int(date.timestamp())
    return banReason, utc
  except KeyboardInterrupt:
    raise
  except IndexError:
    # f = open('xD.html', 'w')
    # f.write(html.tostring(html.fromstring(response.content), encoding='unicode', pretty_print=True))
    # f.close()
    return banReason, None

with open(inputFile) as inputF:
  with open(str(outputPath), 'w') as outputF:
    for subreddit in inputF:
      subreddit = subreddit.strip()
      reason, date = scrape(subreddit)
      print(''.format(subreddit, reason, date))
      outputF.write('{};{};{}\n'.format(subreddit, reason, date))