## python and mysql connection
# pip install pymysql
import pymysql

conn, cur = None, None
data1, data2, data3, data4 = "","","",""
sql = ""
### just change the db name
conn = pymysql.connect(host = 'localhost',user = 'root', password = '1111', db = 'shopDB',charset = 'utf8')

cur = conn.cursor()
##now we can use same codesin sql at the python
cur.execute ('create table if not exists usertable (id char(4), userName char(15), email char (20), birthYear int)')
cur.execute ("insert into usertable values ('john','John Bann','john@naver.com',1990)")
cur.execute ("insert into usertable values ('kim','kim mike','kim@naver.com',1980)")
cur.execute ("insert into usertable values ('park','park minseo','park@naver.com',2000)")

## closing
conn.commit()
conn.close()

## now select start
import pymysql

conn, cur = None, None
data1, data2, data3, data4 = "","","",""
row = None

conn = pymysql.connect(host = 'localhost',user = 'root', password = '1111', db = 'shopDB',charset = 'utf8')

cur = conn.cursor()

cur.execute("select * from usertable")
print('사용자ID    사용자이름      이메일       출생년도')
print("------------------------------------------------")

while (True):
    row = cur.fetchone()
    if row == None :
         break
     
    data1 = row[0]
    data2 = row[1]
    data3 = row[2]
    data4 = row[3]
    print("%5s  %15s  %15s  %d"%(data1, data2, data3, data4))
    
conn.close()


import csv
import pymysql

f = open('2.csv','r')
csvReader = list(csv.reader(f))

cur.execute("create table if not exists test (name char(10), kor char(15))")

for data in csvReader[1:] :
    row1 = data[0]
    row2 = data[1]
    
    sql = """insert into test (name,kor) values (%s, %s);"""
    cur.execute(sql, (row1, row2))
    
f.close()
conn.commit()
conn.close()
