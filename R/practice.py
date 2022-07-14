# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 16:04:28 2021

@author: YoungMin
"""
import requests


url = "https://search.daum.net/search?w=tot&q=2019%EB%85%84%EC%98%81%ED%99%94%EC%88%9C%EC%9C%84&DA=MOR&rtmaxcoll=MOR"

picture_href = 'https://search1.kakaocdn.net/thumb/R232x328.q85/?fname=http%3A%2F%2Ft1.daumcdn.net%2Fmovie%2F4e00e81f2b6f4d2eb65b3387240cc3c01547608409838'
res = requests.get(url)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser')
#image 리스트 추출
image = soup.find_all("img", attrs = {'class':'thumb_img'})
#거기서 다시 url 을 추출
img_res = requests.get(image[0]['src'])
img_res.raise_for_status()
image_url = image[0]['src']
#를 get()안에 넣어서 조금 더 깔끔하게 타이핑 가능
#img_res.content는 사진 출력시 사용
#file 오픈 시 with as 구문 사용
#.format은 {}안에 ()안의 문구가 들어간다.
with open('movie{}.jpg'.format(1), "wb") as f:
    f.write(img_res.content)
    
#for 문 사용, 여러개 받아보기
for i in range(5):
    img_res =requests.get(image[i]['src'])
    with open('movie{}.jpg'.format(i),'wb') as f:
        f.write(img_res.content)
#좀 더 깔끔한 ,enumerate 사용 버전
import requests
from bs4 import BeautifulSoup


url = 'https://search.daum.net/search?w=tot&q=2020%EB%85%84%EC%98%81%ED%99%94%EC%88%9C%EC%9C%84&DA=MOR&rtmaxcoll=MOR'
res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "html.parser")
images = soup.find_all("img", attrs={"class":"thumb_img"})

for idx, image in enumerate(images):
    img_url = image["src"]
    #url이 http로 시작하지 않을 경우
    if img_url.startswith("//"):
        img_url = "https:" + img_url
        
    img_res = requests.get(img_url)
    img_res.raise_for_status()
    
    print(img_res.content)
    
    with open("movie{}.jpg".format(idx + 1), "wb")  as f:
       f.write(img_res.content)
       
    if idx >= 4:
        break #break를 통해 for 문 탈출(enumerate에선 필요)
#2015~2021년 까지의 url 변환

url = 'https://search.daum.net/search?w=tot&q=2020%EB%85%84%EC%98%81%ED%99%94%EC%88%9C%EC%9C%84&DA=MOR&rtmaxcoll=MOR'
for year in range(2016,2020):
    #format 으로 간단하게 설정 가능
    url = 'https://search.daum.net/search?w=tot&q={}%EB%85%84%EC%98%81%ED%99%94%EC%88%9C%EC%9C%84&DA=MOR&rtmaxcoll=MOR'.format(year)
    res = requests.get(url)
    res.raise_for_status()
    
    soup = BeautifulSoup(res.text, "html.parser")
    images = soup.find_all("img", attrs={"class":"thumb_img"})
    
    for idx, image in enumerate(images):
        img_url = image["src"]
        #url이 http로 시작하지 않을 경우
        if img_url.startswith("//"):
            img_url = "https:" + img_url
            
        img_res = requests.get(img_url)
        img_res.raise_for_status()
        
        print(img_res.content)
        #순서도 지정가능하고, 쉼표로 순서 구분 가능
        with open("movie{0}_{1}.jpg".format(idx + 1,year), "wb")  as f:
           f.write(img_res.content)
           
        if idx >= 4:
            break
