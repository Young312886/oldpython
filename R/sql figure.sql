-- please seperate the workplace and checking query

select * from usertbl	;
select * from usertbl where name = '김경호';
select userID, name from usertbl where birthYear >= 1970 and height >= 182;
select userID, name from usertbl where birthYear >=1970 or height >= 182;

select name, height from usertbl where height >= 180 and height <= 183;
select name, height from usertbl where height between 180 and 183; -- we can use between to use it for 구간

select name, addr from usertbl where addr = '경남' or addr = '전남' or addr = '경북';
select name, addr from usertbl where addr in ('경남', '전남','경북'); -- we can use IN to use it for 리스트

select name, height from usertbl where name like '김%'; -- any kind of string can be follow after the %
select name, height from usertbl where name like '_종신'; -- only one, single string can be added at the place of _
-- for the large size of database, we don't use %, _
select name, height from usertbl where height > 177;
select name, height from usertbl where height > (select height from usertbl where name = '김경호'); -- we also can repalce the numbers from the selected values

select name, addr, height from usertbl where height >= (select height from usertbl where addr = '경남'); -- if it returns more than 2 values, we can't use it directly
select name, addr, height from usertbl where height >= any (select height from usertbl where addr = '경남'); -- 두개가 기준이 존재, 어느것이든 충족만 하면 select
select name, addr, height from usertbl where height >= all (select height from usertbl where addr = '경남'); -- 두 기준 모두 충족시 select

select name,addr from usertbl where height = any (select height from usertbl where addr = '경남');
select name,addr from usertbl where height in (select height from usertbl where addr = '경남');-- = any is equal to the in

select name,mDate from usertbl order by mDate; -- 오름차순
select name,mDate from usertbl order by mDate desc; -- 내림차순

select name, height from usertbl order by height desc, name desc; -- 동석차 존재시 이름으로 다시 차순 정함
select distinct addr from usertbl; -- 중복값 제거

use employees;
select emp_no, hire_date from employees order by hire_date asc limit 5; -- limit means cutting, or head()
select emp_no, hire_date from employees order by hire_date asc limit 0,5; -- limit 0,5 = limit 5 offset 0

use sqldb2;
create table buytbl2 ( select * from buytbl); -- extract된게 새로운 table에 적용됨
select * from buytbl2;

create table buytbl3 (select userID, prodName from buytbl);
select * from buytbl3;

drop table buytbl2, buytbl3;
select userID , SUM(amount) from buytbl group by userID; -- we can group by the certain value and also use sum
select userID as '사용자아이디', sum(amount) as '총 구매 갯수' from buytbl group by UserID;
select avg(amount) as '평균 구매 갯수' from buytbl; 

select min(height), max(height), name from usertbl;
select name, min(height), max(height)from usertbl group by name;
select name, height from usertbl where height = (select max(height) from usertbl) or height = (select min(height) from usertbl);
-- 특정 인물을 추출하려면 where을 써서 (조건문) 뽑는게 더 빠르고 좋다

select count(mobile2) as '휴대폰' from usertbl; 
select userID, sum(price*amount) as '구매금액 합계' from buytbl 
group by userID 
order by sum(price);

select userID as '사용자', sum(price * amount) as '총구매액' 
from buytbl
group by userID
having sum(price * amount) > 1000; -- having 이 매우 유용. but have to place after the group by

select userID as '사용자', sum(price * amount) as '총구매액' 
from buytbl
group by userID
having sum(price * amount) > 1000
order by sum(price * amount); -- having 이 매우 유용. but have to place after the group by



select num, groupName, sum(price * amount) as '총비용' from buytbl group by groupName, num;
select num, groupName, sum(price * amount) as '총비용' from buytbl group by groupName, num with rollup; -- 소합계 it provide sum between group by
select num, groupName, sum(price * amount) as '총비용' from buytbl group by groupName with rollup; 

-- 수정은 update
use employees;
create table testTBL4 (id int, Fname varchar(50), Lname varchar(50));
insert into testTbl4
select emp_no, first_name, last_name from employees.employees;

use sqldb2;
create table testtlb5 (select emp_no, first_name, last_name from employees.employees); -- or we can maek it directly by () the data

update testtbl4 set Lname = '없음' where Fname = 'Kyoichi'; -- where apply to the whole dataset. so becareful when using where - to make it sure to untact the original data
use sqldb2;
update buytbl set price = price * 1.5; -- we can update, replace the data by update
use employees;
delete from testtbl4 where fname = 'Aamer' limit 5; -- also we can use limit to limit the range of delete

/* join enable the two tables to be searched at the same time
 join을 할시 상속시킬 값을 생성, 그걸 key값으로 두 table을 연결시키는 것이다.
join은 2개 이상, 3개 이상의 table도 가능 양쪽에 동일한 column이 존지하면 통합할 column을 지시해줘야 한다
ex) where a.deptno = b.deptno 이런식으로  	
