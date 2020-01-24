import os
import sqlite3 as lite
import sys
import pymongo
import django
import urllib

sys.path.append('wwtbht')
os.environ['DJANGO_SETTINGS_MODULE'] = 'wwtbht.settings'
django.setup()

from searching.models import Document

uri = "mongodb://mcwatera:" + urllib.parse.quote("yawp@1") + "@ds255308.mlab.com:55308/wwbtr"

client = pymongo.MongoClient(uri)

stuff = client.wwbtr

collection = stuff.articles

cursor = collection.find()
    
for article in cursor:
    print(article['year'])