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

def create_insight(conn, insight):
    sql = ''' INSERT INTO searching_insight (title,body,date,year,creator,publication,citation) VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, insight)
    return cur.lastrowid
    
def create_sql_connection(db_file):
    conn = None
    conn = lite.connect(db_file)
    return conn
    
def main():
    db = r"./db.sqlite3"
    conn = create_sql_connection(db)
    
    uri = "mongodb://mcwatera:" + urllib.parse.quote("yawp@1") + "@ds255308.mlab.com:55308/wwbtr"

    client = pymongo.MongoClient(uri)

    stuff = client.wwbtr

    collection = stuff.articles

    cursor = collection.find()

    for article in cursor:
        title = article['title']
        body = article['body']
        date = article['date']
        year = article['year']
        creator = article['creator']
        publication = article['publication']
        citation = article['citation']
        
        print(title)
        
        insight = (title,body,date,year,creator,publication,citation)
        
        create_insight(conn, insight)
        
    conn.commit()
    cursor.close()
    
    print("Done with uploading all these dang infos")

if __name__ == '__main__':
    main()