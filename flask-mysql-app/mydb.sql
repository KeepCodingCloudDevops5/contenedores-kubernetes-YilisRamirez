CREATE DATABASE studentdb;
use studentdb;

CREATE TABLE 'students' (
  'id' int unsigned NOT NULL AUTO_INCREMENT,
  'name' varchar(50) NOT NULL,
  'email' varchar(100) NOT NULL,
  'phone' int unsigned NOT NULL,
  'address' varchar(250) NOT NULL,
  PRIMARY KEY ('id')
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

insert  into 'students'('id','name','email','phone','address') values
(1,'Pedro Romero','pedro_romero@gmail.com',657798564,'Sant Joan Despi'),
(2,'Nazaret OLivieri','nazaret_olivieri@gmail.com',610432987,'Cornella de Llobregat');
