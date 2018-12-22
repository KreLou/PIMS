CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  username varchar(50) UNIQUE NOT NULL,
  fistname varchar(60),
  lastname varchar(60),
  department varchar(40),
  company varchar(100),
  password TEXT NOT NULL
);
