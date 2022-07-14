# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 13:44:55 2021

@author: YoungMin
"""



## titanic 데이터셋을 활용한 mysql에 db업로드 하기

import pymysql
import pandas as pd

def Connection():
    conn, cur = None, None
    sql = " "
    conn = pymysql.connect (host = 'localhost',user = 'root', password = '1111', db = 'taitanic',charset = 'utf8' )
    cur = conn.cursor()
    conn.close()

def CreateTables():
    conn = pymysql.connect (host = 'localhost',user = 'root', password = '1111', db = 'taitanic',charset = 'utf8' )
    cur = conn.cursor()
    cur.execute('create table if not exists titanic ( sex char(10), age int, embarked varchar(10));')
    conn.commit()
    conn.close()
    
def InsertDB():
    conn = pymysql.connect (host = 'localhost',user = 'root', password = '1111', db = 'taitanic',charset = 'utf8' )
    cur = conn.cursor()
    df = pd.read_csv("Documents/Ubion/Jupyter/titanic_train.csv")
    ages = df.Age
    ages = ages.fillna(ages.mean())
    sexs = df.Sex
    embarkeds = df.Embarked
    for i in range(len(df)):
        age = ages[i]
        sex = sexs[i]
        embarked = embarkeds[i]
        sql = f"insert into titanic (age,sex,embarked) values ({age},'{sex}','{embarked}')"
        cur.execute(sql)
        conn.commit()
        if( i % 100) == 0:
            print(f'{i}번째 자료 입력중')
    conn.close()

    
Connection()
CreateTables()
InsertDB()
##### 이번엔 class로
class Titanic():
    def __init__ (self):
        self.conn = pymysql.connect (host = 'localhost',user = 'root', password = '1111', db = 'taitanic',charset = 'utf8' )
        self.cur = self.conn.cursor()
    
    def __del__(self):
        self.conn.close()
        print('close')

    def CreateTables(self):
        self.cur.execute('create table if not exists titanic ( sex char(10), age int, embarked varchar(10));')
        self.conn.commit()
        
    def InsertDB(self):
        self.CreateTables()
        df = pd.read_csv("Documents/Ubion/Jupyter/titanic_train.csv")
        ages = df.Age.fillna(df.Age.mean())
        sexs = df.Sex
        embarkeds = df.Embarked
        for i in range(len(df)):
            age = ages[i]
            sex = sexs[i]
            embarked = embarkeds[i]
            sql = f"insert into titanic (age,sex,embarked) values ({age},'{sex}','{embarked}')"
            self.cur.execute(sql)
            self.conn.commit()
            if( i % 100) == 0:
                print(f'{i}번째 자료 입력중')
        self.conn.close()
        
database = Titanic()
database.InsertDB()
