--1.2.create company_keyword_set
create table company_keyword_set(
    date varchar(8),
    company_id varchar,
    company varchar(256),
    brand varchar(256),
    keyword varchar(256)
);

--2.1.create keyword_trend
create table keyword_trend(
    date varchar(8),
    source varchar(50),
    keyword varchar(256),
    query float
);