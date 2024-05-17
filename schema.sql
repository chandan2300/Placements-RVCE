CREATE TABLE coordinator(name text not null, email text primary key, password text not null, admin boolean not null DEFAULT '0');

CREATE TABLE offers(usn text not null, name text not null, dept text not null, gender text, compName text not null, offerType text not null, ctc real not null, jobProfile text, category text not null, remarks text not null, offerDate date);

CREATE TABLE company(name text not null, nStudent integer);