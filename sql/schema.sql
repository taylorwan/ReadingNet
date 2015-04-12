DROP USER 'user280'@'localhost';
DROP DATABASE IF EXISTS project280;

# create user
CREATE DATABASE project280;
CREATE USER 'user280'@'localhost' IDENTIFIED BY 'p4ssw0rd';
USE project280;
GRANT ALL ON project280.* TO 'user280'@'localhost';

# create database
DROP DATABASE IF EXISTS project280;
CREATE DATABASE project280;
USE project280;

CREATE TABLE donors( 
	donor_id INT PRIMARY KEY NOT NULL, 
    phone_num INT NOT NULL, 
    email varchar(200) NOT NULL, 
    street_address varchar(200) NOT NULL, 
    first_name varchar(120) NOT NULL, 
    last_name varchar(120) NOT NULL, 
    dob DATE NOT NULL, 
    zip_code varchar(10) NOT NULL, #varchar bc some zipcodes have a 4 digit extension 
    gender enum('M','F','Other') #gender is not a binary
); 

CREATE TABLE genres( 
	genre varchar(120) PRIMARY KEY NOT NULL, 
    description MEDIUMTEXT NOT NULL
);

CREATE TABLE levels( 
	reading_level enum('Level 1','Level 2','Level 3') PRIMARY KEY NOT NULL 
);

CREATE TABLE book_status( 
	book_status enum('New','Gently used') PRIMARY KEY NOT NULL, 
    cost INT NOT NULL 
);

CREATE TABLE volunteers( 
	volunteer_id INT PRIMARY KEY NOT NULL, 
    phone_num INT NOT NULL, 
    email varchar(200) NOT NULL, 
    street_address varchar(200) NOT NULL,
    first_name varchar(120) NOT NULL, 
    last_name varchar(120) NOT NULL, 
    dob DATE NOT NULL, 
    zip_code varchar(10) NOT NULL, #varchar bc some zipcodes have a 4 digit extension  
    gender enum('M','F','Other') #gender is not a binary
);

CREATE TABLE clients( 
	client_id INT PRIMARY KEY NOT NULL, 
    organization_name varchar(200) NOT NULL,  
    phone_num INT NOT NULL, 
    email varchar(200) NOT NULL,  
    street_address varchar(200) NOT NULL,
    contact_person varchar(200) NOT NULL, 
    reading_level enum('Level 1','Level 2','Level 3'),
    tokens INT NOT NULL, 
    new_count INT NOT NULL, 
    used_count INT NOT NULL,
    FOREIGN KEY(reading_level) REFERENCES levels(reading_level)
);

CREATE TABLE book_inventory( 
	isbn INT PRIMARY KEY, 
    book_status enum('New','Gently used'),
    title varchar(300) NOT NULL, 
    reading_level enum('Level 1','Level 2','Level 3'), 
    edition INT NOT NULL, 
    publisher varchar(200) NOT NULL, 
    genre varchar(120) NOT NULL, 
    count INT NOT NULL,
    FOREIGN KEY(book_status) REFERENCES book_status(book_status),
    FOREIGN KEY(reading_level) REFERENCES levels(reading_level),
    FOREIGN KEY(genre) REFERENCES genres(genre)
);

INSERT INTO levels(reading_level) VALUES ('Level 1');