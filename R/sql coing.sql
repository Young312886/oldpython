show databases;
show table status;
desc employees;
use employees;
select first_name as 이름, gender 성별, hire_date '회사 입사일' from employees;
select emp_no as 번호, birth_date 생일 from employees;
create table `y TestTBL` (id INT); 
drop table `y TestTBL`;

drop database if exists sqldb2;
create database sqldb2;
-- database == schema 같다
use sqldb2;
create table usertbl 
(`userID` CHAR(8) NOT NULL primary key,
`name` VARCHAR(10) NOT NULL,
`birthYear` INT NOT NULL,
`addr` CHAR(2) NOT NULL,
`moblie` CHAR(3),
`mobile2` CHAR(8),
`height`SMALLINT,
`mDate` DATE
);
show tables;
desc usertbl;

create table buytbl  -- 이름 / 자료 형태 / null / primary 값  ++ foreign key 설정까지
(`num` INT auto_increment not null primary key,
`userID` char(8) not null,
`prodName` char(6) not null,
`groupName` char(4),
`price` int not null,
`amount` smallint not null,
Foreign key (`userID`) references usertbl(userID));
-- foreing key = 다른 테이블의 내용을 부모 테이블로 삼을 수 있게 만들어 준다. 즉, 참고 가능
-- insert into table values ~~~
insert into usertbl values ('LSG','이승기',1987, '서울','011', '1111111', 182, '2008-8-8');
insert into usertbl values ( 'KBS', '김범수' , 1979, '경남', 011, 22222222 , 173, '2012-4-4');
insert into usertbl values( 'KKH', '김경호', 1971,'전남', 019, 33333333,177,'2007-7-7');
insert into usertbl values('JYP','조용필',1950,'경기',011,4444444,177,'2009-4-4');
insert into usertbl values('SSK','성시경',1979,'서울',null,null,186,'2013-5-6');
insert into usertbl values('LBJ','임재범',1963,'서울',016,66666666,182,'2003-5-8');
insert into usertbl values('YJS','윤종신',1969,'경남',null,null,170,'2007-4-1');
insert into usertbl values('EJW','은지원',1972,'경북',011,8888888,174,'2010-4-6');
insert into usertbl values('JWK','조관우',1965,'경기',018,9999999,172,'2010-5-3');
insert into usertbl values('BBK','바비킴',1973,'서울',010,0000000,176,'2010-8-3');
insert into buytbl values (null, 'KBS', '운동화',null,30,2);
insert into buytbl values (null, 'KBS','노트북','전자',1000,1);
insert into buytbl values (null, 'JYP','모니터','전자',200,1);
insert into buytbl values (null, 'BBK','모니터','전자',200,5);
insert into buytbl values (null, 'KBS','청바지','의류',50,3);
insert into buytbl values (null, 'BBK','메모리','전자',80,10);
insert into buytbl values (null, 'SSK','책','서적',10,1);
insert into buytbl values (null, 'EJW','책','서적',15,6);
insert into buytbl values (null, 'EJW','청바지','의류',30,4);
insert into buytbl values (null, 'BBK','운동화',null,30,2);
insert into buytbl values (null, 'EJW','책','서적',15,1);
insert into buytbl values (null, 'BBK','운동화',null,30,2);
