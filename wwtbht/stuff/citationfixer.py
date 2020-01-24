import os
import sqlite3 as lite
import sys
import pymongo
import django
import urllib


def main():
    db = r"./db.sqlite3"
    conn = create_sql_connection(db)
    
