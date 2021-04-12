# Political Perspective
Political Perspective was designed to bring articles on similar topics from different viewpoints to the same place

## Resource

**Users**

Attributes:

* id (integer)
* first name (string)
* last name (string)
* age (integer)
* email (string)
* password (string)

## Schema

```psql
CREATE TABLE users (
id INTEGER PRIMARY KEY,
fname VAR_CHAR(50),
lname VAR_CHAR(50),
age INTEGER,
email VAR_CHAR(50),
password VAR_CHAR(50);
```

## Resource 2

**Articles**

Attributes:

* id (integer)
* source (string)
* title (string)
* url (string)
* story (string)

## Schema

```psql
CREATE TABLE articles (
id INTEGER PRIMARY KEY,
source VAR_CHAR(10),
title VAR_CHAR(255),
url VAR_CHAR(255),
story TEXT);
```

## REST Endpoints

Name                           | Method | Path
-------------------------------|--------|------------------
Retrieve article collection    | GET    | /articles
Retrieve article member        | GET    | /articles/*\<id\>*
Create user member             | POST   | /users
Login user                     | POST   | /sessions
Logout user                    | DELETE | /sessions
