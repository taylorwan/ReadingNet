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
	donor_id INT NOT NULL, 
    phone_num INT NOT NULL, 
    email varchar(200) NOT NULL, 
    street_address varchar(200) NOT NULL, 
    first_name varchar(120) NOT NULL, 
    last_name varchar(120) NOT NULL, 
    dob DATE NOT NULL, 
    zip_code varchar(10) NOT NULL, #varchar bc some zipcodes have a 4 digit extension 
    gender enum('M','F','Other'), #gender is not a binary
    PRIMARY KEY(donor_id)
); 

CREATE TABLE genres( 
	genre varchar(120) NOT NULL, 
    description MEDIUMTEXT NOT NULL,
    PRIMARY KEY (genre)
);

INSERT INTO genres(genre, description)
VALUES ("fiction","interesting made up stories");

CREATE TABLE levels( 
	reading_level enum('Level 1','Level 2','Level 3') NOT NULL,
    PRIMARY KEY(reading_level)
);

CREATE TABLE book_status( 
	book_status enum('New','Gently used') NOT NULL, 
    cost INT NOT NULL,
    PRIMARY KEY(book_status)
);

INSERT INTO book_status(book_status, cost)
values('New',3);

CREATE TABLE volunteers( 
	volunteer_id INT NOT NULL, 
    phone_num INT NOT NULL, 
    email varchar(200) NOT NULL, 
    street_address varchar(200) NOT NULL,
    first_name varchar(120) NOT NULL, 
    last_name varchar(120) NOT NULL, 
    dob DATE NOT NULL, 
    zip_code varchar(10) NOT NULL, #varchar bc some zipcodes have a 4 digit extension  
    gender enum('M','F','Other'), #gender is not a binary
    PRIMARY KEY(volunteer_id)
);

INSERT INTO volunteers
values(456, 202202202, 'a@b.com', '1 1st St', 'Sam', 'Smith', '1990-01-01', 20057, 'M');

CREATE TABLE clients( 
	client_id INT NOT NULL, 
    organization_name varchar(200) NOT NULL,  
    phone_num INT NOT NULL, 
    email varchar(200) NOT NULL,  
    street_address varchar(200) NOT NULL,
    contact_person varchar(200), 
    tokens INT NOT NULL, 
    new_count INT NOT NULL, 
    used_count INT NOT NULL,
    PRIMARY KEY(client_id)
);

INSERT INTO clients
VALUES (222, 'Georgetown', 800555555, 'a@a.com', '2 2nd St', 'Sandy Smith', 2, 0, 0);

CREATE TABLE clients_readinglevel(
	client_id INT NOT NULL,
    reading_level enum('Level 1','Level 2','Level 3'),
    PRIMARY KEY(client_id, reading_level),
    FOREIGN KEY(client_id) REFERENCES clients(client_id),
    FOREIGN KEY(reading_level) REFERENCES levels(reading_level)
);

insert into clients_readinglevel
values (222,'Level 1');
    
    
CREATE TABLE book_inventory( 
	isbn INT NOT NULL, 
    book_status enum('New','Gently used') NOT NULL,
    title varchar(300) NOT NULL, 
    reading_level enum('Level 1','Level 2','Level 3') NOT NULL, 
    edition INT NOT NULL, 
    publisher varchar(200) NOT NULL, 
    genre varchar(120) NOT NULL, 
    count INT NOT NULL,
    author varchar(250) NOT NULL,
    PRIMARY KEY(isbn),
    FOREIGN KEY(book_status) REFERENCES book_status(book_status),
    FOREIGN KEY(reading_level) REFERENCES levels(reading_level),
    FOREIGN KEY(genre) REFERENCES genres(genre)
);

insert into book_inventory
values (123123, 'New', 'Harry Potter', 'Level 1', 2, 'Random House', 'Fiction', 1);

CREATE TABLE book_donations( 
	isbn INT NOT NULL, 
    donor_id INT NOT NULL, 
    date_donated DATE NOT NULL, 
    quantity INT NOT NULL,
    PRIMARY KEY(isbn, donor_id, date_donated),
    FOREIGN KEY(donor_id) REFERENCES donors(donor_id),
    FOREIGN KEY(isbn) REFERENCES book_inventory(isbn)
);

insert into book_donations
values(123123, 123, '2015-04-12',1);

CREATE TABLE cash_donations( 
	donor_id INT NOT NULL, 
    amount FLOAT(2) NOT NULL, 
    date_donated DATE NOT NULL,
    PRIMARY KEY(donor_id, amount, date_donated),
    FOREIGN KEY(donor_id) REFERENCES donors(donor_id)
);

insert into cash_donations
values(123, 12.00, '2015-04-12');

CREATE TABLE purchased ( 
	volunteer_id INT NOT NULL, 
    isbn INT NOT NULL,  
    date_purchased DATE NOT NULL, 
    book_status enum('New','Gently used') NOT NULL, 
    quantity INT NOT NULL,
    PRIMARY KEY(volunteer_id, isbn, date_purchased, book_status),
    FOREIGN KEY(volunteer_id) REFERENCES volunteers(volunteer_id)
);

insert into purchased
values (456, 12345, '2015-04-12', 'Gently used', 1);

drop table requests;
CREATE TABLE requests( 
	client_id INT NOT NULL, 
    isbn INT NOT NULL,
    request_date DATE NOT NULL,
    PRIMARY KEY(client_id, isbn, request_date),
    FOREIGN KEY(client_id) REFERENCES clients(client_id),
    FOREIGN KEY(isbn) REFERENCES book_inventory(isbn)
);

insert into requests
values(222, 123123, '2015-04-12');

CREATE TABLE author_book( 
	isbn INT NOT NULL, 
    author_fn VARCHAR(250) NOT NULL,
    author_ln VARCHAR(250) NOT NULL,
    PRIMARY KEY(isbn, author_fn, author_ln),
    FOREIGN KEY(isbn) REFERENCES book_inventory(isbn)
);



INSERT INTO levels(reading_level) 
VALUES ('Level 1');

INSERT INTO donors(donor_id, phone_num, email, street_address, first_name, last_name, dob, zip_code, gender) 
VALUES (123, 2019568701, "test@test.com", "1 Main Street", "Sophia", "Kleyman", '1994-08-09', 07410, 'F');
	