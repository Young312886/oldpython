# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 15:19:24 2021

@author: YoungMin
"""

import pymysql
import pandas as pd
from bs4 import BeautifulSoup
import requests
import calendar, time, json
from datetime import datetime
from threading import Timer
import numpy as np
import re
import string
##만약 class를 활용한다면

class DBUpdater:
    def __init__(self):
        ## sql 연걸
          self.conn = pymysql.connect(host='localhost', user='root',
            password='1111', db='INVESTAR', charset='utf8')
          ## sql table 작성
          with self.conn.cursor() as curs:
            sql = """
            CREATE TABLE IF NOT EXISTS company_info (
                code VARCHAR(20),
                company VARCHAR(40),
                last_update DATE,
                PRIMARY KEY (code))
            """
            curs.execute(sql)
            sql = """
            CREATE TABLE IF NOT EXISTS daily_price (
                code VARCHAR(20),
                date DATE,
                open BIGINT(20),
                high BIGINT(20),
                low BIGINT(20),
                close BIGINT(20),
                diff BIGINT(20),
                volume BIGINT(20),
                PRIMARY KEY (code, date))
            """
            curs.execute(sql)
            self.conn.commit()
            self.codes = dict()
## __del__ 은 init이후 바로 작동되는 것이다
    def __del__(self): 
        self.conn.close()
        print('종료')
        ## krx 에서 url 읽어오기
    def read_krx_code(self):
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13'
        krx = pd.read_html(url, header = 0)[0]
        krx = krx [['종목코드','회사명']]
        ## 코드와 회사명만 추출
        krx = krx.rename(columns = {'종목코드':'code','회사명':'company'})
        krx.code = krx.code.map('{:06d}'.format)            
        return krx
    
    def update_company_info(self):
        ## 만약 if구문이 돌아가지 않는다면 = 기본 세팅이 필요함 else 에 넣음
        with self.conn.cursor() as curs:
            ## sql의 last_update날짜 확인
            sql = "select max(last_update) from company_info"
            curs.execute(sql)
            rs = curs.fetchone()
            today = datetime.today().strftime("%Y-%m-%d")
            ## 만약 다르거나 작다면 최신으로 업데이트하기
            if rs[0] == None or rs[0].strftime("%Y-%m-%d") < today:
                krx = self.read_krx_code() ## read html
                for idx in range(len(krx)):
                    #데이터 추출
                    code = krx.code.values[idx]
                    company = krx.company.values[idx] 
                    ## dictionary 형성(이따 회사 코드 활용하려고)
                    self.codes[code] = company 
                    #sql input
                    sql = """replace into company_info (code, company, last_update) values (%s, %s, %s);"""
                    curs.execute(sql, (code, company, today))
                    #log 표시
                    tmnow = datetime.now().strftime('%y-%m-%d %H:%M') 
                    print(f'[{tmnow}] #{idx+1:04d} replace into company_info' f" values ({code},{company},{today}")
                self.conn.commit()
            else : 
                ##만약 최신이라면, sql읽어와서 dictionary 만들기 (회사코드)
                sql = 'select * from company_info'
                df = pd.read_sql(sql, self.conn)
                for idx in range (len(df)):
                    self.codes [df['code'].values[idx]]= df['company'].values[idx]
    ## 또 다른 formating = f"뭐라뭐라 {value}" 를 쓰면 외부 변수가 {} 안에 들어갈 수 있다
    def crawl_naver(self, code, company, pages_to_fetch):
        #크롤링 만들기
        try : 
            url = f'https://finance.naver.com/item/sise_day.nhn?code={code}'
            html = BeautifulSoup(requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text, 'lxml')
            pgrr = html.find('td',class_='pgRR')
            if pgrr is None:
                return None
            s = str (pgrr.a['href']).split('=')
            #페이지 수 구하기
            lastpage = s[-1]
            pages = min(int(lastpage),pages_to_fetch)
            for page in range(1,pages+1):
                pg_url = '{}&page = {}'.format(url,page)
                df = df.append(pd.read_html(requests.get(pg_url, headers={'User-agent': 'Mozilla/5.0'}).text)[0])
                ##log 출력
                tmnow= datetime.now().strftime('%y-%m-%d %H:%M')
                print('[{}] {} ({}) : {:04d}/{:04d} pages are downloading'.format(
                    tmnow, company, code, page, pages),end = "\r")
                
            df = df.rename(columns = {'날짜':'date','종가':'close','전일비':'diff','시가':'open','고가':'high','저가':'low','거래량':'volume'})
            df['date'] = df.date.replace('.','-')
            df = df.dropna()
            df[['close','diff','open','high','low','volume']] = df[['close','diff','open','high','low','volume']] .astype(int)
            df = df[['date','open','high','low','close','diff','volume']] 
            
        except Exception as e:
            print("Exception occured :", str(e))
            return None
        return df               

        
        # for number in range(1,10):
        #     code = '005930'
        #     url = f'https://finance.naver.com/item/sise_day.nhn?code={code}&page={number}'
        #     res = requests.get(url,headers={'User-agent': 'Mozilla/5.0'})
        #     res.raise_for_status()
        #     soup = BeautifulSoup(res.text, "html.parser")
        #     datas = soup.find_all('tr',onmouseover = 'mouseOver(this)')
        #     #크롤링된 데이터 합치기
        #     datas = pd.DataFrame(datas)
        #     df = pd.concat([df,datas],ignore_index=True)
        #     print(len(df))

        # df.columns = ['1','date','2','close','3','diff','4','open','5','high','6','low','7','volume','8']
        # df = df[['date','close','diff','open','high','low','volume']]
        # self.df = df
        # return self.df
            
    def db_input (self, df, num, code, company):
        with self.conn.cursor() as curs:
            for r in df.itertuples():
                sql = f"""replace into daily_price values ('{code}','{r.date}','{r.open_price}','{r.high}','{r.low}','{r.close}','{r.diff}','{r.volume}')"""
                curs.execute(sql)
            self.conn.commit()
            print('{} {} {} data input done '.format(code, company, len(df)))
    
    def update_daily(self, pages_to_fetch):
        #code를 하나씩 읽는 for문 적용
        for idx, code in enumerate(self.codes):
            df = self.crawl_naver(code, self.codes[code], pages_to_fetch)
            if df is None:
                continue
            self. db_input(df, idx, code, self.codes[code])
        pass
        #위에 update_company_info처럼 시간이 다르면 업데이트 하는 방법으로 진행해야 함
    
    def execute_daily(self):
        pass
    ##timer 함수 활용(5시마다 작동), update daily 함수 호출하여 자동으로 할 수 있게 krx 함수 까지 호출하는거 필요
            

dbu = DBUpdater()
data = dbu.read_krx_code()
dbu.update_company_info()
dbu.update_daily(3)


##나중에 검색해보기
if __name__ == '__main__':
    dbu = DBUpdater()
    dbu.execute_daily()
## crawling and uploadng practice
# number = 1
# code = '005930'

# url = f'https://finance.naver.com/item/sise_day.nhn?code={code}&page={number}'
# df = pd.DataFrame()

# for number in range(1,10):
#     res = requests.get(url,headers={'User-agent': 'Mozilla/5.0'})
#     res.raise_for_status()
#     soup = BeautifulSoup(res.text, "html.parser")
#     datas = soup.find_all('tr',onmouseover = 'mouseOver(this)')
#     datas = pd.DataFrame(datas)
#     df = pd.concat([df,datas],ignore_index=True)

# df.columns = ['1','date','2','close','3','diff','4','open','5','high','6','low','7','volume','8']
# df = df[['date','close','diff','open','high','low','volume']]
# print(df)

# for idx in range(len(df)):
#     date = df.loc[idx]['open'].get_text()
#     date = Astype(date)
#     print(date)


## """ is reference multilines \ is escape code (to make the inner value can be read as it is)    

