# create database
#DROP DATABASE readingNet;
CREATE DATABASE readingNet;
USE readingNet;

# create user
# CREATE USER 'readingNet280'@'localhost' IDENTIFIED BY 'p4ssw0rd';
GRANT ALL ON readingNet.* TO 'readingNet280'@'localhost';
USE readingNet;

CREATE TABLE donors( 
	donor_id INT AUTO_INCREMENT NOT NULL, 
    donor_first_name VARCHAR(120) NOT NULL, 
    donor_last_name VARCHAR(120) NOT NULL,
    donor_dob DATE NOT NULL, 
    donor_gender enum('M','F','Other'), #gender is not a binary
    donor_phone_num BIGINT NOT NULL, 
    donor_email VARCHAR(200) NOT NULL, 
    donor_street_address VARCHAR(250) NOT NULL,
    donor_city VARCHAR(250) NOT NULL,
    donor_state VARCHAR(2) NOT NULL,
    donor_zipcode BIGINT NOT NULL, #varchar bc some zipcodes have a 4 digit extension 
    PRIMARY KEY(donor_id)
); 

CREATE TABLE volunteers( 
	volunteer_id INT AUTO_INCREMENT NOT NULL,
    volunteer_first_name VARCHAR(120) NOT NULL,
    volunteer_last_name VARCHAR(120) NOT NULL, 
    volunteer_dob DATE NOT NULL,
    volunteer_gender ENUM('M','F','Other'), #gender is not a binary
    vounteer_phone_num BIGINT NOT NULL, 
    volunteer_email VARCHAR(200) NOT NULL, 
    vounteer_street_address VARCHAR(200) NOT NULL,
    volunteer_city VARCHAR(250) NOT NULL,
    volunteer_state VARCHAR(2) NOT NULL,
    volunteer_zipcode BIGINT NOT NULL, #varchar bc some zipcodes have a 4 digit extension  
    PRIMARY KEY(volunteer_id)
);

CREATE TABLE clients( 
	client_id INT AUTO_INCREMENT NOT NULL, 
    organization_name VARCHAR(200) NOT NULL,  
    client_phone_num INT NOT NULL, 
    client_email VARCHAR(200) NOT NULL,  
    client_street_address VARCHAR(200) NOT NULL,
    client_city VARCHAR(250) NOT NULL,
    client_state VARCHAR(2) NOT NULL,
    client_zipcode BIGINT NOT NULL,
    client_tokens INT NOT NULL, 
    new_count INT NOT NULL, 
    used_count INT NOT NULL,
    PRIMARY KEY(client_id)
);

CREATE TABLE clients_contactperson(
	client_id INT NOT NULL, 
    client_cp_fn VARCHAR(120) NOT NULL, 
    client_cp_ln VARCHAR(120) NOT NULL,
	PRIMARY KEY(client_id, client_cp_fn, client_cp_ln),
    FOREIGN KEY (client_id) 
		REFERENCES clients(client_id)
		ON DELETE CASCADE
);

CREATE TABLE reading_levels( 
	reading_level INT NOT NULL,
    PRIMARY KEY(reading_level)
);

-- CREATE TABLE book_status( 
-- 	book_status ENUM('New','Gently used') NOT NULL, 
--     cost INT NOT NULL,
--     PRIMARY KEY(book_status)
-- );
-- 
-- INSERT INTO book_status(book_status, cost)
-- values('New',3);
-- 

CREATE TABLE clients_readinglevel(
	client_id INT NOT NULL,
    reading_level INT NOT NULL,
    PRIMARY KEY(client_id, reading_level),
    FOREIGN KEY(client_id) 
		REFERENCES clients(client_id)
        ON DELETE CASCADE,
    FOREIGN KEY(reading_level) 
		REFERENCES reading_levels(reading_level)
        ON DELETE CASCADE
);

CREATE TABLE genres( 
	genre_type varchar(120) NOT NULL, 
    description MEDIUMTEXT NOT NULL,
    PRIMARY KEY (genre_type)
);

CREATE TABLE book_inventory(
	isbn INT NOT NULL, 
    title VARCHAR(500) NOT NULL,
    reading_level INT NOT NULL, 
    genre_type VARCHAR(120) NOT NULL,
    book_status ENUM('New','Gently used') NOT NULL,
    edition INT NOT NULL, 
    publisher VARCHAR(200) NOT NULL,
    quantity INT NOT NULL,
    PRIMARY KEY (isbn, book_status),
	FOREIGN KEY(reading_level)
		REFERENCES reading_levels(reading_level)
        ON DELETE CASCADE,
    FOREIGN KEY(genre_type) 
		REFERENCES genres(genre_type)
        ON DELETE CASCADE
);

CREATE TABLE cash_reserves(
	cash_amount FLOAT DEFAULT 0,
    cash_id INT NOT NULL DEFAULT 1,
    PRIMARY KEY(cash_id)
);

CREATE TABLE book_author(
	isbn INT NOT NULL, 
    title VARCHAR(500) NOT NULL,
    author_fn VARCHAR(120) NOT NULL,
    author_ln VARCHAR(120) NOT NULL,
    PRIMARY KEY(isbn, author_fn, author_ln),
    FOREIGN KEY(isbn)
		REFERENCES book_inventory(isbn)
		ON DELETE CASCADE
);

CREATE TABLE book_donations(
	book_donation_id INT AUTO_INCREMENT NOT NULL,
	isbn INT NOT NULL, 
    title VARCHAR(500) NOT NULL,
    book_status ENUM('New','Gently used') NOT NULL,
    donor_id INT NOT NULL, 
    date_donated DATE NOT NULL, 
    quantity INT NOT NULL,
    PRIMARY KEY(book_donation_id),
    FOREIGN KEY(donor_id) 
		REFERENCES donors(donor_id),
    FOREIGN KEY(isbn) 
		REFERENCES book_inventory(isbn)
);

CREATE TABLE cash_donations(
	cash_donation_id INT AUTO_INCREMENT NOT NULL,
	donor_id INT NOT NULL, 
    amount FLOAT(2) NOT NULL, 
    date_donated DATE NOT NULL,
    PRIMARY KEY(cash_donation_id),
    FOREIGN KEY(donor_id)
		REFERENCES donors(donor_id)
);

CREATE TABLE volunteer_books_purchased(
	book_purchase_id INT AUTO_INCREMENT NOT NULL,
	volunteer_id INT NOT NULL, 
    isbn INT NOT NULL,  
    date_purchased DATE NOT NULL, 
    book_status ENUM('New','Gently used') NOT NULL, 
    quantity INT NOT NULL,
    book_cost INT NOT NULL,
    PRIMARY KEY(book_purchase_id),
    FOREIGN KEY(volunteer_id) 
		REFERENCES volunteers(volunteer_id)
);

CREATE TABLE client_book_requests( 
	client_id INT NOT NULL, 
    isbn INT NOT NULL,
    book_status ENUM('New','Gently used') NOT NULL, 
    quantity INT NOT NULL,
    request_date DATE NOT NULL,
    request_status ENUM('Approved','Declined','In Progress') NOT NULL DEFAULT 'In Progress', 
    PRIMARY KEY(client_id, isbn, request_date),
    FOREIGN KEY(client_id) 
		REFERENCES clients(client_id)
        ON DELETE CASCADE,
    FOREIGN KEY(isbn) 
		REFERENCES book_inventory(isbn)
        ON DELETE CASCADE
);

CREATE TABLE client_shopping_cart(
    isbn INT NOT NULL,
    book_status ENUM('New','Gently used') NOT NULL, 
    quantity INT NOT NULL,
    PRIMARY KEY(isbn, book_status),
    FOREIGN KEY(isbn) 
		REFERENCES book_inventory(isbn)
        ON DELETE CASCADE
	#FOREIGN KEY (book_status)
		#REFERENCES book_inventory(book_status)
        #ON DELETE CASCADE
);

CREATE TABLE client_transaction_history(
	purchase_id INT NOT NULL,
	client_id INT NOT NULL,
    isbn INT NOT NULL,
    book_status ENUM('New','Gently used') NOT NULL, 
    date_purchased DATE NOT NULL,
    quantity INT NOT NULL,
    PRIMARY KEY (purchase_id),
    FOREIGN KEY (client_id)
		REFERENCES clients(client_id),
	FOREIGN KEY (isbn)
		REFERENCES book_inventory(isbn)
	#FOREIGN KEY (book_status)
	#	REFERENCES book_inventory(book_status)
);

CREATE TABLE client_book_purchases(
	client_id INT NOT NULL, 
    total_books_purchased INT NOT NULL,
    used_book_purchased INT NOT NULL,
    PRIMARY KEY (client_id),
    FOREIGN KEY (client_id)
		REFERENCES clients(client_id)
        ON DELETE CASCADE
);