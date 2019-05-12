#util
import os
import random
import re
import time

#twitter
import tweepy

#pillow
from PIL import Image
import requests
from io import BytesIO

#end_imports

key = os.environ.get('key')
secret = os.environ.get('secret')
token = os.environ.get('token')
token_secret = os.environ.get('token_secret')


def getSentence():
 file = open("words.txt","r")
 content = file.read().splitlines()
 words = []
 sentence = ""
 maxSentenceSize = random.randint(10, 140)
 count = 0
 
 for i in content:
  words.append(i)
 words.pop(len(words)-1) #remove stupid blank line, why python?
 
 for r in range(len(words)):
  p = random.choice(words)
  
  if not re.match('https?:.*?(\.png|\.jpg|\.gif)', p): #we dont count urls
   count += len(p)
  if maxSentenceSize < count:
   break
  sentence = sentence+" "+p
 
 return sentence
 
 
def getImages(images):
 urls = images
 count = 0
 names = []
 
 for i in urls:
  count += 1
  response = requests.get(i)
  img = Image.open(BytesIO(response.content))
  tosave = "{n}.{ex}".format(n=count, ex=img.format)
  
  img.save(tosave)
  names.append(tosave)
  
 return names
 
 
def sendTweet(sentence):

 auth = tweepy.OAuthHandler(key, secret)
 auth.set_access_token(token, token_secret)
 api = tweepy.API(auth)
 #api end
 
 oracion = sentence
 images = re.findall('https?:.*?(?:\.png|\.jpg|\.gif)', oracion)
 
 if len(images) < 1:
  api.update_status(oracion)
 else: 
  #remove links from tweet
  for im in images:
   oracion = oracion.replace(im, '')
   oracion = oracion.replace('  ', '') #remove double empty spaces
 
  media = getImages(images) #get images for twitter <- names because they already saved
  meids = []
 
  for img in media:
   up = api.media_upload(img)
   meids.append(up.media_id) #done, now post the tweet
  
  api.update_status(status=oracion, media_ids=meids)
 print("done")
 

#sendTweet(getSentence())

while True:
 sendTweet(getSentence())
 time.sleep(60*10)#every ten minutes