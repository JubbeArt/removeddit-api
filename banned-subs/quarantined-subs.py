import gzip
import json
import pathlib

# THIS SCRIPT IS VERY HEAVY! SAVE STUFF BEFORE YOU RUN THIS, IT MIGHT CRACH YOUR COMPUTER.
# IT WILL TAKE ABOUT 2GB OF RAM TO RUN THIS SINCE IT UNZIPS THE SUBREDDIT FILE

zippedFile = 'subreddits.gz'
outputFile = 'output/quarantined-subs'

# Open gzipped file from pushshift
with gzip.open(zippedFile, 'rb') as zippedF:  
  with open(outputFile, 'w') as outputF:
    subreddits = zippedF.readlines()

    for jsonString in subreddits:
      subreddit = json.loads(jsonString.decode())
      
      # Quarantine will be None if it is banned or private
      # It will be false otherwise (but it will never True) 
      if subreddit['quarantine'] is None:
        outputF.write('{}>{}\n'.format(
          subreddit['display_name'], 
          subreddit['title'],
        ))
        #print(subreddit)

print('Done! File saved to', outputFile)
