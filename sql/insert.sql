
INSERT INTO donors(donor_id, donor_first_name, donor_last_name, donor_dob, donor_gender, donor_phone_num, donor_email, donor_street_address, donor_city, donor_state, donor_zipcode)
    VALUES (1, 'Joseph', 'Shmoseph', '1990-08-09', 'M', 2019568702, 'joseph@s.com', '6 Main Street','Fair Lawn','NJ',07410);
INSERT INTO donors(donor_id, donor_first_name, donor_last_name, donor_dob, donor_gender, donor_phone_num, donor_email, donor_street_address, donor_city, donor_state, donor_zipcode)
    VALUES (2, 'Doug', 'Mug', '1960-09-09', 'M', 2019888702, 'doug@s.com', '71 Main Street','Fair Lawn','NJ',07410);
INSERT INTO donors(donor_id, donor_first_name, donor_last_name, donor_dob, donor_gender, donor_phone_num, donor_email, donor_street_address, donor_city, donor_state, donor_zipcode)
    VALUES (3, 'Mary', 'Lary', '2000-08-09', 'F', 800800800, 'Mary@s.com', '17 8th Street','Fair Lawn','NJ',07410);
INSERT INTO donors(donor_id, donor_first_name, donor_last_name, donor_dob, donor_gender, donor_phone_num, donor_email, donor_street_address, donor_city, donor_state, donor_zipcode)
    VALUES (4, 'Jane', 'Doe', '1998-08-09', 'F', 2019908702, 'jane@s.com', '6 Main Street','Fair Lawn','NJ',07410);

INSERT INTO volunteers(volunteer_id, volunteer_first_name, volunteer_last_name, volunteer_dob, volunteer_gender, vounteer_phone_num, volunteer_email, vounteer_street_address, volunteer_city, volunteer_state, volunteer_zipcode)
	VALUES (1, 'John','Smith', '1998-08-09', 'M', 800800800, 'j@j.com', '1 First Street', 'Washington','DC',20057);
INSERT INTO volunteers(volunteer_id, volunteer_first_name, volunteer_last_name, volunteer_dob, volunteer_gender, vounteer_phone_num, volunteer_email, vounteer_street_address, volunteer_city, volunteer_state, volunteer_zipcode)
	VALUES (2, 'Kate','Smith', '1998-08-09', 'F', 800800800, 'j@j.com', '1 First Street', 'Washington','DC',20057);
INSERT INTO volunteers(volunteer_id, volunteer_first_name, volunteer_last_name, volunteer_dob, volunteer_gender, vounteer_phone_num, volunteer_email, vounteer_street_address, volunteer_city, volunteer_state, volunteer_zipcode)
	VALUES (3, 'Sarah','Jones', '1998-08-09', 'F', 800800800, 'j@j.com', '1 First Street', 'Washington','DC',20057);


INSERT INTO clients(client_id, organization_name, client_phone_num, client_email, client_street_address, client_city, client_state, client_zipcode, client_tokens, new_count, used_count)
	VALUES(1, 'Booksasarus', 800800800, 'books@books.com', '14 Main St', 'Washington','DC',20057,8,0,0);

INSERT INTO clients_contactperson(client_id, client_cp_fn, client_cp_ln) VALUES (1, 'Sandra', 'Stern');

INSERT INTO reading_levels(reading_level) VALUES (1);
INSERT INTO reading_levels(reading_level) VALUES (2);
INSERT INTO reading_levels(reading_level) VALUES (3);

INSERT INTO clients_readinglevel(client_id, reading_level) VALUES (1, 1);
INSERT INTO clients_readinglevel(client_id, reading_level) VALUES (1, 2);

INSERT INTO genres(genre_type, description)
	VALUES ("Fiction","Interesting made up stories");

INSERT INTO cash_reserves(cash_amount, cash_id) VALUES (0,1);

INSERT INTO book_inventory(isbn, title, reading_level, genre_type, book_status, edition, publisher, quantity) VALUES (444, 'Harry Potter', 1, 'Fiction', 'New', 1, 'Random House', 1);

INSERT INTO book_author(isbn, title, author_fn, author_ln) VALUES (444, 'Harry Potter', 'JK', 'Rowling');



    