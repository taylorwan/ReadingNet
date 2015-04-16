
INSERT INTO donors(donor_id, donor_first_name, donor_last_name, donor_dob, donor_gender, donor_phone_num, donor_email, donor_street_address, donor_city, donor_state, donor_zipcode)
    VALUES (1, 'Joseph', 'Shmoseph', '1990-08-09', 'M', 2019568702, 'joseph@s.com', '6 Main Street','Fair Lawn','CA',07410);
INSERT INTO donors(donor_id, donor_first_name, donor_last_name, donor_dob, donor_gender, donor_phone_num, donor_email, donor_street_address, donor_city, donor_state, donor_zipcode)
    VALUES (2, 'Doug', 'Mug', '1960-09-09', 'M', 2019888702, 'doug@s.com', '71 Main Street','Fair Lawn','DC',07410);
INSERT INTO donors(donor_id, donor_first_name, donor_last_name, donor_dob, donor_gender, donor_phone_num, donor_email, donor_street_address, donor_city, donor_state, donor_zipcode)
    VALUES (3, 'Mary', 'Lary', '1940-08-09', 'F', 800800800, 'Mary@s.com', '17 8th Street','Fair Lawn','NY',07410);
INSERT INTO donors(donor_id, donor_first_name, donor_last_name, donor_dob, donor_gender, donor_phone_num, donor_email, donor_street_address, donor_city, donor_state, donor_zipcode)
    VALUES (4, 'Jane', 'Doe', '1993-08-09', 'F', 2019908702, 'jane@s.com', '6 Main Street','Fair Lawn','NJ',07410);

INSERT INTO volunteers(volunteer_id, volunteer_first_name, volunteer_last_name, volunteer_dob, volunteer_gender, vounteer_phone_num, volunteer_email, vounteer_street_address, volunteer_city, volunteer_state, volunteer_zipcode)
	VALUES (1, 'John','Smith', '1998-08-09', 'M', 800800800, 'j@j.com', '1 First Street', 'Washington','DC',20057);
INSERT INTO volunteers(volunteer_id, volunteer_first_name, volunteer_last_name, volunteer_dob, volunteer_gender, vounteer_phone_num, volunteer_email, vounteer_street_address, volunteer_city, volunteer_state, volunteer_zipcode)
	VALUES (2, 'Kate','Smith', '1998-08-09', 'F', 800800800, 'k@j.com', '1 First Street', 'Washington','DC',20057);
INSERT INTO volunteers(volunteer_id, volunteer_first_name, volunteer_last_name, volunteer_dob, volunteer_gender, vounteer_phone_num, volunteer_email, vounteer_street_address, volunteer_city, volunteer_state, volunteer_zipcode)
	VALUES (3, 'Sarah','Jones', '1998-08-09', 'F', 800800800, 's@j.com', '1 First Street', 'Washington','DC',20057);

INSERT INTO clients(client_id, organization_name, client_phone_num, client_email, client_street_address, client_city, client_state, client_zipcode, client_tokens)
	VALUES(1, 'Booksasarus', 800800800, 'books@books.com', '14 Main St', 'Washington','DC',20057,8);
INSERT INTO clients(client_id, organization_name, client_phone_num, client_email, client_street_address, client_city, client_state, client_zipcode, client_tokens)
	VALUES(2, 'Books-A-Million', 800800800, 'hi@bam.com', '4 Dupont Circle', 'Washington','DC',20023,4);
INSERT INTO clients(client_id, organization_name, client_phone_num, client_email, client_street_address, client_city, client_state, client_zipcode, client_tokens)
	VALUES(3, 'Barnes Noble', 800800800, 'support@bn.com', '423 Metro Center', 'Washington','DC',20001,4);
INSERT INTO clients(client_id, organization_name, client_phone_num, client_email, client_street_address, client_city, client_state, client_zipcode, client_tokens)
	VALUES(4, 'B3', 800800800, 'support@bn.com', '423 Metro Center', 'Washington','DC',20001,4);

INSERT INTO clients_contactperson(client_id, client_cp_fn, client_cp_ln) VALUES (1, 'Sandra', 'Stern');

INSERT INTO reading_levels(reading_level) VALUES (1);
INSERT INTO reading_levels(reading_level) VALUES (2);
INSERT INTO reading_levels(reading_level) VALUES (3);
INSERT INTO reading_levels(reading_level) VALUES (4);

INSERT INTO clients_readinglevel(client_id, reading_level) VALUES (1, 1);
INSERT INTO clients_readinglevel(client_id, reading_level) VALUES (1, 2);
INSERT INTO clients_readinglevel(client_id, reading_level) VALUES (2, 1);
INSERT INTO clients_readinglevel(client_id, reading_level) VALUES (2, 2);
INSERT INTO clients_readinglevel(client_id, reading_level) VALUES (4, 1);

INSERT INTO genres(genre_type, description) VALUES ("Fiction", "Interesting made up stories");
INSERT INTO genres(genre_type, description) VALUES ("Non-Fiction", "Stories based on mostly true happenings");

#insert more here
INSERT INTO cash_reserves(cash_amount, cash_id) VALUES (0,1);

# insert client_book_purchases
# insert client_book_requests

INSERT INTO book_inventory(isbn, title, reading_level, genre_type, book_status, edition, publisher, quantity)
	VALUES (444, 'Harry Potter', 1, 'Fiction', 'New', 1, 'Random House', 1);
INSERT INTO book_inventory(isbn, title, reading_level, genre_type, book_status, edition, publisher, quantity)
	VALUES (445, 'Harry Potter 2', 2, 'Fiction', 'New', 1, 'Random House', 1);
INSERT INTO book_inventory(isbn, title, reading_level, genre_type, book_status, edition, publisher, quantity)
	VALUES (446, 'Harry Potter 3', 3, 'Fiction', 'New', 1, 'Random House', 1);
INSERT INTO book_inventory(isbn, title, reading_level, genre_type, book_status, edition, publisher, quantity)
	VALUES (446, 'Harry Potter 3', 3, 'Fiction', 'Gently used', 1, 'Random House', 2);
INSERT INTO book_inventory(isbn, title, reading_level, genre_type, book_status, edition, publisher, quantity)
	VALUES (447, 'Harry Potter 4', 4, 'Fiction', 'New', 1, 'Random House', 1);
INSERT INTO book_inventory(isbn, title, reading_level, genre_type, book_status, edition, publisher, quantity)
	VALUES (447, 'Harry Potter 4', 4, 'Fiction', 'Gently used', 1, 'Random House', 1);
INSERT INTO book_inventory(isbn, title, reading_level, genre_type, book_status, edition, publisher, quantity)
	VALUES (800, 'Zero To One', 2, 'Non-Fiction', 'New', 1, 'Crown Business', 2);

INSERT INTO book_author(isbn, author_fn, author_ln) VALUES (444, 'Jane', 'Doe');
INSERT INTO book_author(isbn, author_fn, author_ln) VALUES (445, 'Jane', 'Doe');
INSERT INTO book_author(isbn, author_fn, author_ln) VALUES (446, 'Jane', 'Doe');
INSERT INTO book_author(isbn, author_fn, author_ln) VALUES (447, 'Jane', 'Doe');
INSERT INTO book_author(isbn, author_fn, author_ln) VALUES (800, 'Peter', 'Thiel');

INSERT INTO book_donations ( book_donation_id, isbn, book_status, donor_id, date_donated, quantity )
    VALUES ( 4920384, 444, 'New', 4, '2012-02-10', 1);
INSERT INTO book_donations ( book_donation_id, isbn, book_status, donor_id, date_donated, quantity )
    VALUES ( 4920385, 445, 'New', 4, '2012-02-15', 1);
INSERT INTO book_donations ( book_donation_id, isbn, book_status, donor_id, date_donated, quantity )
    VALUES ( 4920386, 446, 'New', 3, '2014-02-15', 1);
INSERT INTO book_donations ( book_donation_id, isbn, book_status, donor_id, date_donated, quantity )
    VALUES ( 4920387, 447, 'New', 3, '2014-02-15', 1);

INSERT INTO cash_donations( cash_donation_id, donor_id, amount, date_donated ) VALUES ( 1, 1, 23, '2015-01-02' );
INSERT INTO cash_donations( cash_donation_id, donor_id, amount, date_donated ) VALUES ( 2, 2, 32, '2015-01-03' );
INSERT INTO cash_donations( cash_donation_id, donor_id, amount, date_donated ) VALUES ( 3, 3, 53, '2015-01-01' );

INSERT INTO client_book_purchases(client_id, total_books_purchased, used_book_purchased) VALUES (1, 0, 0);
INSERT INTO client_book_purchases(client_id, total_books_purchased, used_book_purchased) VALUES (4, 0, 0);

INSERT INTO volunteer_books_purchased( book_purchase_id, volunteer_id, isbn, date_purchased, book_status, quantity, book_cost )
	VALUES( 1, 1, 800, '2015-02-15', 'New', 2, 20 );
INSERT INTO volunteer_books_purchased( book_purchase_id, volunteer_id, isbn, date_purchased, book_status, quantity, book_cost )
	VALUES( 2, 2, 447, '2015-02-20', 'New', 1, 5 );
INSERT INTO volunteer_books_purchased( book_purchase_id, volunteer_id, isbn, date_purchased, book_status, quantity, book_cost )
	VALUES( 3, 3, 446, '2014-02-20', 'New', 2, 25 );

# we need to make it so volunteers can approve requests
INSERT INTO client_book_requests( client_id, isbn, book_status, quantity, request_date, request_status )
	VALUES ( 1, 446, 'New', 1, '2014-03-10', 'In Progress' );
INSERT INTO client_book_requests( client_id, isbn, book_status, quantity, request_date, request_status )
	VALUES ( 1, 447, 'New', 1, '2014-03-12', 'In Progress' );
INSERT INTO client_book_requests( client_id, isbn, book_status, quantity, request_date, request_status )
	VALUES ( 2, 445, 'New', 1, '2012-04-12', 'Approved' );
INSERT INTO client_book_requests( client_id, isbn, book_status, quantity, request_date, request_status )
	VALUES ( 2, 447, 'New', 1, '2014-04-12', 'In Progress' );
INSERT INTO client_book_requests( client_id, isbn, book_status, quantity, request_date, request_status )
	VALUES ( 3, 444, 'New', 1, '2012-04-12', 'Approved' );
