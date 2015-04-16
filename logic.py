import pymysql
import config

class CursorIterator(object):
    """Iterator for the cursor object."""

    def __init__(self, cursor):
        """ Instantiate a cursor object"""
        self.__cursor = cursor

    def __iter__(self):
        return self

    def next(self):
        elem = self.__cursor.fetchone()

        if elem is None:
            self.__cursor.close()
            raise StopIteration()
        else:
            return elem

class Database(object):
    """Database object"""

    def __init__( self, opts ):
        """Initalize database object"""
        super( Database, self ).__init__()
        self.opts = opts
        self.__connect()

    def __connect( self ):
        """Connect to the database"""
        self.conn = pymysql.connect(self.opts.DB_HOST, self.opts.DB_USER,
                                    self.opts.DB_PASSWORD, self.opts.DB_NAME)
        # self.conn = pymysql.connect('localhost','readingNet280', 'p4ssw0rd', 'readingNet' )

        self.conn.autocommit(True)

    def search(self, isbn, title, author_fn, author_ln, publisher, status):
        with self.conn:
            cur = self.conn.cursor()

            isbn = pymysql.escape_string( isbn )
            title = pymysql.escape_string( title )
            author_fn = pymysql.escape_string( author_fn )
            author_ln = pymysql.escape_string( author_ln )
            publisher = pymysql.escape_string( publisher )
            status = pymysql.escape_string( status )

            paramstring = []

            
            like = "like "
            quotation = "\""
            wildcard = "%"
            titleF = "book_inventory.title "
            if title != "IS NOT NULL":
                title = titleF +like +quotation + wildcard + title + wildcard + quotation
            else:
                title = titleF + title

            paramstring.append(title)

            isbnF = "book_inventory.isbn "
            if isbn != "IS NOT NULL":
                isbn = isbnF + like + quotation + wildcard + isbn + wildcard + quotation
            else:
                isbn = isbnF + isbn

            paramstring.append(isbn)

            author_fnF = "book_author.author_fn "
            if author_fn != "IS NOT NULL":
                author_fn = author_fnF + like + quotation + wildcard + author_fn + wildcard + quotation
            else:
                author_fn = author_fnF + author_fn

            paramstring.append(author_fn)

            author_lnF = "book_author.author_ln "
            if author_ln != "IS NOT NULL":
                author_ln = author_lnF + like + quotation + wildcard + author_ln + wildcard + quotation
            else:
                author_ln = author_lnF + author_ln

            paramstring.append(author_ln)

            publisherF = "book_inventory.publisher "
            if publisher != "IS NOT NULL":
                publisher = publisherF + like + quotation + wildcard+ publisher + wildcard + quotation
            else:
                publisher = publisherF + publisher

            paramstring.append(publisher)

            if status != "IS NOT NULL":
                status = "book_inventory.book_status " + like + quotation + wildcard+ status + wildcard + quotation
            else:
                status = "book_inventory.book_status " + status

            paramstring.append(status)

            paramstring = " AND ".join(paramstring)
            
            cur.execute("SELECT book_inventory.title, book_inventory.isbn, book_author.author_fn, book_author.author_ln, book_inventory.publisher, book_inventory.book_status FROM book_inventory INNER JOIN book_author ON book_inventory.isbn = book_author.isbn WHERE {0}".format(paramstring))
            
            data = cur.fetchall()

            return data

    def checkout(self, client_ID, approved):
        
        with self.conn:
            cur = self.conn.cursor()
            query_cur = self.conn.cursor()

            #client_ID = pymysql.escape_string( client_ID )

            # updating book recommendation table
            cur.execute("SELECT DISTINCT isbn FROM client_shopping_cart ORDER BY isbn")
            allBooks = cur.fetchall()
            length = len(allBooks)

            if length > 1:
                counterA = 0
                counterB = 1

                while counterA + 1 < length:
                    counterB = counterA + 1
                    while counterB < length:
                        isbn_a = allBooks[counterA]
                        isbn_b = allBooks[counterB]

                        # make sure isbn_a is smaller than isbn_b
                        if isbn_a > isbn_b:
                            temp = isbn_a
                            isbn_a = isbn_b
                            isbn_b = temp

                        cur.execute( "SELECT quantity FROM purchase_couples WHERE isbn_1 = %s AND isbn_2 = %s", ( isbn_a, isbn_b ) )
                        qty = cur.fetchone()

                        if qty is None:
                            cur.execute("INSERT INTO purchase_couples ( isbn_1, isbn_2, quantity ) VALUES ( %s, %s, 1 )", ( isbn_a, isbn_b ) )
                        else:
                            newQty = qty[0] + 1
                            cur.execute("UPDATE purchase_couples SET quantity = %s WHERE isbn_1 = %s AND isbn_2 = %s", ( newQty, isbn_a, isbn_b ) )

                        cur.execute("SELECT * FROM purchase_couples")
                        counterB += 1
                    counterA += 1
                

            cur.execute("SELECT * FROM client_shopping_cart")
            
            row = cur.fetchone()
            while row is not None:
                failed = False

                isbn = row[0]
                status = row[1]
                quantity = row[2]
                error = 0

                # get the reading level of the book just added to cart
                query_cur.execute("SELECT reading_level FROM book_inventory WHERE book_inventory.isbn = %s",(isbn))
                row_from_query = query_cur.fetchone()
                reading_level = row_from_query[0]

                #this is the reading level of the book they want to buy. check if it is in that client's lookup table
                query_cur.execute("SELECT reading_level FROM clients_readinglevel WHERE client_id = %s AND reading_level = %s",(client_ID, reading_level))
                exists = query_cur.fetchone()

                if exists == None and not approved:
                    #reading level doesn't exist. add the book to the requests table
                    query_cur.execute("INSERT INTO client_book_requests(client_id, isbn, book_status, quantity, request_date, request_status) VALUES (%s, %s, %s, %s, CURDATE(), 'In Progress')",(client_ID, isbn, status, quantity))
                    query_cur.execute("DELETE FROM client_shopping_cart WHERE isbn = %s and book_status = %s",(isbn,status))
                    
                    #TAYLOR TO JS
                    
                else:
                    #proceed - get the number of tokens the client has and check if they can purchase
                    query_cur.execute("SELECT client_tokens FROM clients WHERE client_id = %s",(client_ID))

                    tokens_row = query_cur.fetchone()
                    tokens = tokens_row[0]

                    if status == 'New':
                        cost_of_current_purchase = 3
                    else:
                        cost_of_current_purchase = 1

                    #if there aren't enough tokens to purchase, remove it from the cart
                    if tokens < cost_of_current_purchase:
                        
                        ## js error
                        query_cur.execute("DELETE FROM client_shopping_cart WHERE isbn = %s and book_status = %s",(isbn,status))
                        
                        error = error+1
                        failed = True

                    else:

                        #find the book quantity in the inventory to see if you need to decrease it or delete it
                        query_cur.execute("SELECT quantity FROM book_inventory WHERE isbn = %s and book_status = %s",(isbn,status))
                        quant_row = query_cur.fetchone()
                        quant_in_inventory = quant_row[0]

                        #if the amount they want to buy is greater than the amount there is, remove it from the cart and cancel this transaction
                        if quantity > quant_in_inventory:
                            query_cur.execute("DELETE FROM client_shopping_cart WHERE isbn = %s and book_status = %s",(isbn,status))
                            
                            ###TAYLOR TO JS###
                            failed = True
                            row = cur.fetchone()
                            continue
                        
                        #if the amount to be purchased will bring the amount current down to 0, remove the book from inventory
                        elif quantity == quant_in_inventory:
                            query_cur.execute("INSERT INTO client_transaction_history(client_id, isbn, book_status, date_purchased, quantity) VALUES (%s, %s, %s, CURDATE(), %s)",(client_ID, isbn, status, quantity))
                            query_cur.execute("DELETE FROM client_shopping_cart WHERE isbn = %s and book_status = %s",(isbn,status))
                            query_cur.execute("DELETE FROM book_inventory WHERE isbn = %s and book_status = %s",(isbn,status))

                        # just decrease the quantity
                        elif quantity < quant_in_inventory:
                            query_cur.execute("INSERT INTO client_transaction_history(client_id, isbn, book_status, date_purchased, quantity) VALUES (%s, %s, %s, CURDATE(), %s)",(client_ID, isbn, status, quantity))
                            query_cur.execute("DELETE FROM client_shopping_cart WHERE isbn = %s and book_status = %s",(isbn,status))
                            new_quant_in_inventory = quant_in_inventory - quantity
                            query_cur.execute("UPDATE book_inventory SET quantity = %s WHERE isbn = %s and book_status = %s",(new_quant_in_inventory,isbn,status))

                        #now, we are ready to update the tokens and check if more need to be added by the system
                        if failed != True:
                            new_tokens = tokens - cost_of_current_purchase
                            query_cur.execute("UPDATE clients SET client_tokens = %s WHERE client_id = %s",(new_tokens, client_ID))

                            #check to see how many books the client has purchsed to see if we need to give them more tokens
                            query_cur.execute("SELECT total_books_purchased, used_book_purchased FROM client_book_purchases WHERE client_id = %s",(client_ID))
                            books_purchased_row = query_cur.fetchone()
                            total_books_owned = books_purchased_row[0]
                            used_book_owned = books_purchased_row[1]

                            # calculate which counter needs to be updated: if used, then both, if not, then just total
                            if status =='Gently used' or status == 'gently used' or status == 'Gently Used':
                                new_used_count = used_book_owned + quantity
                                used_book_owned = new_used_count

                                new_total_count = total_books_owned + quantity
                                total_books_owned = new_total_count

                                query_cur.execute("UPDATE client_book_purchases SET used_book_purchased = %s WHERE client_id = %s",(new_used_count,client_ID))
                                query_cur.execute("UPDATE client_book_purchases SET total_books_purchased = %s WHERE client_id = %s",(new_total_count,client_ID))
                            else:
                                new_total_count = total_books_owned + quantity
                                query_cur.execute("UPDATE client_book_purchases SET total_books_purchased = %s WHERE client_id = %s",(new_total_count,client_ID))
                            
                            if used_book_owned >= 10:
                                update_tokens = new_tokens + 3 
                                query_cur.execute("UPDATE clients SET client_tokens = %s",(new_tokens))
                                #reset the counter
                                query_cur.execute("UPDATE client_book_purchases SET used_book_purchased= 0")
                            if total_books_owned >= 5:
                                update_tokens = new_tokens + 3 
                                query_cur.execute("UPDATE clients SET client_tokens = %s",(new_tokens))
                                #reset the counter
                                query_cur.execute("UPDATE client_book_purchases SET total_books_owned= 0")

                row = cur.fetchone()
            self.conn.commit()
            return cur

    def process_purchase(self, check_list):
        with self.conn:
            cur = self.conn.cursor()
            for check in check_list:
                new_check = pymysql.escape_string(check)
                quantity_selected, isbn, status = new_check.split("_")
                isbn = int(isbn)
                quantity_selected = int(quantity_selected)

                cur.execute("SELECT * FROM book_inventory WHERE isbn = %s AND book_status = %s",(isbn,status))
                book = cur.fetchone()
                book_isbn = book[0]
                title = book[1]
                reading_level = book[2]
                genre_type = book[3]
                book_status = book[4]
                edition = book[5]
                publisher = book[6]
                quantity = book[7]
                cur.execute("SELECT * FROM client_shopping_cart WHERE isbn = %s AND book_status=%s",(isbn,book_status))
                exists_in_cart = cur.fetchone()
               
                # if this book isn't already in the client's shopping cart, add it
                if exists_in_cart == None:
                    cur.execute("INSERT INTO client_shopping_cart(isbn, book_status, quantity) VALUES (%s, %s, 1)",(book_isbn, book_status))
                #if it does, just increment the quantity
                else:
                    existing_quant_in_cart = exists_in_cart[2]
                    new_quantity = existing_quant_in_cart + quantity_selected
                    cur.execute("UPDATE client_shopping_cart SET quantity = %s WHERE isbn = %s AND book_status=%s",(new_quantity, isbn, book_status))

            self.conn.commit()
            return cur

    def change_request_status(self, request_id, status):
        with self.conn:
            cur = self.conn.cursor()
            temp = self.conn.cursor()
            temp2 = self.conn.cursor()

            request_id = pymysql.escape_string( request_id )
            status = pymysql.escape_string( status ) 

            cur.execute("UPDATE client_book_requests SET request_status = %s WHERE request_id = %s",(status, request_id))
            self.conn.commit()
            

            cur.execute("SELECT * FROM book_inventory WHERE isbn = 446 AND book_status='New'")

            # if status was changed to approved, treat it like a client purchase
            if status == 'Approved':
                temp.execute("SELECT * FROM client_book_requests WHERE request_id = %s", (request_id))
                # data is now from the client book request
                data = temp.fetchone()

                isbn = data[2]
                client_id = data[1]
                book_status = data[3]
                quantity = data[4]

                temp.execute("INSERT INTO client_shopping_cart(isbn, book_status, quantity) VALUES (%s, %s, %s)",(isbn, book_status, quantity))
                
                self.checkout(client_id, True)

            self.conn.commit()

            return cur

    def addDonor( self, donorID, firstName, lastName, DOB, gender, phoneNum, email, streetAddress, city, state, zipCode):
        with self.conn:
            cur = self.conn.cursor()
            
            #donorID = pymysql.escape_string( donorID )
            firstName = pymysql.escape_string( firstName )
            lastName = pymysql.escape_string( lastName )
            DOB = pymysql.escape_string( DOB )
            gender = pymysql.escape_string( gender )
            phoneNum = pymysql.escape_string( phoneNum )
            email = pymysql.escape_string( email )
            streetAddress = pymysql.escape_string( streetAddress )
            city = pymysql.escape_string( city )
            state = pymysql.escape_string( state )
            zipCode = pymysql.escape_string( zipCode )
            
            cur.execute("INSERT INTO donors VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )",(donorID, firstName, lastName, DOB, gender, phoneNum, email, streetAddress, city, state, zipCode))

            self.conn.commit()
            return cur

    def add_volunteer(self, volunteerID, firstName, lastName, DOB, gender, phoneNum, email, streetAddress, city, state, zipCode):
        with self.conn:
            cur = self.conn.cursor( )

            volunteerID = pymysql.escape_string( volunteerID )
            firstName = pymysql.escape_string( firstName )
            lastName = pymysql.escape_string( lastName )
            DOB = pymysql.escape_string( DOB )
            gender = pymysql.escape_string( gender )
            phoneNum = pymysql.escape_string( phoneNum )
            email = pymysql.escape_string( email )
            streetAddress = pymysql.escape_string( streetAddress )
            city = pymysql.escape_string( city )
            state = pymysql.escape_string( state )
            zipCode = pymysql.escape_string( zipCode )

            cur.execute("INSERT INTO volunteers(volunteer_id, volunteer_first_name, volunteer_last_name, volunteer_dob, volunteer_gender, vounteer_phone_num, volunteer_email, vounteer_street_address, volunteer_city, volunteer_state, volunteer_zipcode) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )",(volunteerID, firstName, lastName, DOB, gender, phoneNum, email, streetAddress, city, state, zipCode))

            self.conn.commit()
            return cur

    def add_reading_level(self, reading_level):
        with self.conn:
            cur = self.conn.cursor()  
            reading_level = pymysql.escape_string( reading_level ) 

            cur.execute("INSERT INTO reading_levels(reading_level) VALUES (%s)",(reading_level))
            
            self.conn.commit()

            return cur

    def add_genre(self, genre, description):
        with self.conn:
            cur = self.conn.cursor()  
            genre = pymysql.escape_string( genre ) 
            description = pymysql.escape_string( description ) 

            cur.execute("INSERT INTO genres(genre_type, description) VALUES (%s, %s)",(genre, description))
            
            self.conn.commit()
            return cur


    def see_all_levels(self):
        with self.conn:      
            cur = self.conn.cursor()  

            cur.execute("SELECT * FROM reading_levels")
            data = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]

            return data, colnames

    def see_all_donors(self):
        with self.conn:
            cur = self.conn.cursor()

            cur.execute("SELECT * FROM donors")
            data = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]
        
            return data, colnames

    def see_all_volunteers(self):
        with self.conn:
            cur = self.conn.cursor()

            cur.execute("SELECT * FROM volunteers")
            data = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]
            
            return data, colnames

    def see_all_book_inventory(self):
        with self.conn:
            cur = self.conn.cursor()

            cur.execute("SELECT * FROM book_inventory")
            data = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]

            return data, colnames

    def see_all_donations(self):
        with self.conn:
            cur = self.conn.cursor()

            cur.execute("SELECT * FROM book_donations")
            data = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]

            return data, colnames

    def see_all_cash_donations(self):
        with self.conn:
            cur = self.conn.cursor()
            
            cur.execute("SELECT * FROM cash_donations")
            data = cur.fetchall()
            
            colnames = [desc[0] for desc in cur.description]

            return data, colnames

    def see_cash_reserves(self):
        with self.conn:
            cur = self.conn.cursor()
            
            cur.execute("SELECT * FROM cash_reserves")
            data = cur.fetchall()
            
            colnames = [desc[0] for desc in cur.description]

            return data, colnames

    def add_book(self, isbn, title, readingLevel, genre, bookStatus, edition, publisher, quantity, author_fn, author_ln, donorID, donationDate):
        with self.conn:
            cur = self.conn.cursor()

            isbn = pymysql.escape_string( isbn )
            title = pymysql.escape_string( title )
            readingLevel = pymysql.escape_string( readingLevel )
            genre = pymysql.escape_string( genre )
            bookStatus = pymysql.escape_string( bookStatus )
            edition = pymysql.escape_string( edition )
            publisher = pymysql.escape_string( publisher )
            quantity = pymysql.escape_string( quantity )
            quantity = int(quantity)
            author_fn = pymysql.escape_string( author_fn )
            author_ln = pymysql.escape_string( author_ln )
            donorID = pymysql.escape_string( donorID )
            donationDate = pymysql.escape_string( donationDate )

            cur.execute("SELECT * FROM book_inventory WHERE isbn = %s AND book_status = %s",(isbn, bookStatus))
            exists = cur.fetchone()

            #if the book is not already in the database
            if exists == None:
                cur.execute("INSERT INTO book_inventory(isbn, title, reading_level, genre_type, book_status, edition, publisher, quantity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(isbn, title, readingLevel, genre, bookStatus, edition, publisher, quantity))
                cur.execute("INSERT INTO book_donations(isbn, book_status, donor_id, date_donated, quantity) VALUES (%s, %s, %s, %s, %s)",(isbn, bookStatus, donorID, donationDate, quantity))
                cur.execute("INSERT INTO book_author(isbn, author_fn, author_ln) VALUES (%s, %s, %s)",(isbn, author_fn, author_ln))
            else:
                existing_quant = 0
                existing_quant = exists[7]
                new_quantity = existing_quant + quantity
                cur.execute("UPDATE book_inventory SET quantity=%s WHERE isbn=%s AND book_status=%s",(new_quantity, isbn, bookStatus))
                cur.execute("INSERT INTO book_donations(isbn, book_status, donor_id, date_donated, quantity) VALUES (%s, %s, %s, %s, %s)",(isbn, bookStatus, donorID, donationDate, quantity))

            self.conn.commit()

            return cur

    
    def add_client(self, client_ID, organization_name, client_phone_num, email, street_address, city, state, zipCode, tokens, new_count, used_count):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO clients(client_id, organization_name, client_phone_num, client_email, client_street_address, client_city, client_state, client_zipcode, client_tokens, new_count, used_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(client_ID, organization_name, client_phone_num, email, street_address, city, state, zipCode, tokens, new_count, used_count))

            self.conn.commit()

            return cur

    def add_tokens(self, client_ID, token_amount):
        with self.conn:
            cur = self.conn.cursor()

            token_amount = int(token_amount)

            cur.execute("SELECT * FROM clients WHERE client_id = %s",(client_ID))
            data = cur.fetchone()
            client_current_tokens = data[8]
            new_token_amount = client_current_tokens + token_amount
            cur.execute("UPDATE clients SET client_tokens = %s WHERE client_id = %s",(new_token_amount, client_ID))

            self.conn.commit()

            return cur

    def new_cash_donation(self, donor_ID, amount, donation_date):
        with self.conn:
            cur = self.conn.cursor()

            donor_ID = pymysql.escape_string( donor_ID )
            amount = pymysql.escape_string( amount )
            amount = float(amount)
            donation_date = pymysql.escape_string( donation_date )

            cur.execute("INSERT INTO cash_donations(donor_id, amount, date_donated) VALUES (%s, %s, %s)",(donor_ID, amount, donation_date))
            cur.execute("SELECT * FROM cash_reserves WHERE cash_id = 1")
            
            data = cur.fetchone()
            current_cash_reserves = data[0]
            new_cash = current_cash_reserves + amount

            cur.execute("UPDATE cash_reserves SET cash_amount = %s WHERE cash_id = 1",(new_cash))

            # threshold for dispersing tokens will be $500
            if new_cash > 500:
                cur.execute("SELECT * FROM clients")
                row = cur.fetchone()
                while row is not None:
                    client_ID = row[0]
                    self.add_tokens(client_ID, 3)
                    row = cur.fetchone()

            self.conn.commit()

            return cur

    def purchase_new_book(self, volunteer_ID, isbn, title, reading_level, genre, book_status, edition, publisher, quantity, author_fn, author_ln, purchase_date, cost):
        with self.conn:
            cur = self.conn.cursor()

            volunteer_ID = pymysql.escape_string( volunteer_ID )
            isbn = pymysql.escape_string( isbn )
            title = pymysql.escape_string( title )
            reading_level = pymysql.escape_string( reading_level )
            reading_level = int(reading_level)
            genre = pymysql.escape_string( genre )
            book_status = pymysql.escape_string( book_status )
            edition = pymysql.escape_string( edition )
            edition = int(edition)
            publisher = pymysql.escape_string( publisher )
            quantity = pymysql.escape_string( quantity )
            quantity = int(quantity)
            author_fn = pymysql.escape_string( author_fn )
            author_ln = pymysql.escape_string( author_ln )
            purchase_date = pymysql.escape_string( purchase_date )
            cost=pymysql.escape_string( cost )
            cost = int(cost)

            cur.execute("SELECT * FROM cash_reserves WHERE cash_id = 1")
            data = cur.fetchone()
            cash_on_hand = data[0]

            if cost > cash_on_hand:
                #JS ERROR
                return cur
            else:
                new_cash_amount = cash_on_hand - cost
                cur.execute("UPDATE cash_reserves SET cash_amount = %s WHERE cash_id = 1",(new_cash_amount))

                cur.execute("SELECT * FROM book_inventory WHERE isbn = %s AND book_status = %s",(isbn, book_status))
                exists = cur.fetchone()

                # if the book doesn't already exist in the DB, first add it to the inventory, then add it to the purchase history
                if exists == None:
                    cur.execute("INSERT INTO book_inventory(isbn, title, reading_level, genre_type, book_status, edition, publisher, quantity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(isbn, title, reading_level, genre, book_status, edition, publisher, quantity))
                    cur.execute("INSERT INTO volunteer_books_purchased(volunteer_id, isbn, date_purchased, book_status, quantity, book_cost) VALUES (%s, %s, %s, %s, %s, %s)",(volunteer_ID, isbn, purchase_date, book_status, quantity, cost))
                    cur.execute("INSERT INTO book_author(isbn, title, author_fn, author_ln) VALUES (%s, %s, %s, %s)",(isbn, title, author_fn, author_ln))
                #if the book already exists, you are just adding to the quantity
                else:
                    existing_quant = exists[7]
                    new_quantity = existing_quant + quantity
                    cur.execute("UPDATE book_inventory SET quantity=%s WHERE isbn=%s AND book_status=%s",(new_quantity, isbn, book_status))
                    cur.execute("INSERT INTO volunteer_books_purchased(volunteer_id, isbn, date_purchased, book_status, quantity, book_cost) VALUES (%s, %s, %s, %s, %s, %s)",(volunteer_ID, isbn, purchase_date, book_status, quantity, cost))

            self.conn.commit()

            return cur

### Queries Taylor 4.14

    # 4
    def author_donators(self):
        with self.conn:
            cur = self.conn.cursor()

            cur.execute("SELECT DISTINCT donor_first_name as 'First Name', donor_last_name as 'Last Name' FROM donors NATURAL JOIN book_donations NATURAL JOIN book_author WHERE donor_first_name = author_fn AND donor_last_name = author_ln ")
            data = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]
        
            return data, colnames

    # 5
    def most_recent_donor(self):
        with self.conn:
            cur = self.conn.cursor()

            cur.execute("SELECT donor_first_name as 'First Name', donor_last_name as 'Last Name' FROM donors NATURAL JOIN cash_donations ORDER BY date_donated DESC")
            data = []
            data.append(cur.fetchone())
            colnames = [desc[0] for desc in cur.description]
        
            return data, colnames

    # 6
    def avg_tokens(self):
        with self.conn:
            cur = self.conn.cursor()

            cur.execute("SELECT avg(client_tokens) as 'Avg Tokens' from clients")
            data = []
            data.append(cur.fetchone())
            colnames = [desc[0] for desc in cur.description]

            return data, colnames

    def min_tokens(self):
        with self.conn:
            cur = self.conn.cursor()

            cur.execute("SELECT min(client_tokens) as 'Min Tokens' from clients")
            data = []
            data.append(cur.fetchone())
            colnames = [desc[0] for desc in cur.description]

            return data, colnames

    def max_tokens(self):
        with self.conn:
            cur = self.conn.cursor()

            cur.execute("SELECT max(client_tokens) as 'Max Tokens' from clients")
            data = []
            data.append(cur.fetchone())
            colnames = [desc[0] for desc in cur.description]

            return data, colnames


    # 7
    def book_per_genre(self):
        with self.conn:
            cur = self.conn.cursor()

            cur.execute("SELECT genre_type as 'Genre', count(genre_type) as 'Books' from book_inventory GROUP BY genre_type")
            data = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]

            return data, colnames

    def book_per_level(self):
        with self.conn:
            cur = self.conn.cursor()

            cur.execute("SELECT reading_level as 'Reading Level', count(reading_level) as 'Books' from book_inventory GROUP BY reading_level")
            data = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]

            return data, colnames

    def book_per_genre_level(self):
        with self.conn:
            cur = self.conn.cursor()

            cur.execute("SELECT genre_type as 'Genre', reading_level as 'Reading Level', count(isbn) as 'Books' from book_inventory GROUP BY genre_type, reading_level")
            data = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]

            return data, colnames

    # 8
    def top_book(self):
        with self.conn:
            cur = self.conn.cursor()

            # cur.execute("SELECT title, sum(quantity) from book_inventory GROUP BY isbn")
            cur.execute("SELECT title as 'Title', sum(quantity) as 'Quantity' from book_inventory GROUP BY isbn HAVING sum(quantity) >= all( SELECT sum(quantity) FROM book_inventory GROUP BY isbn )")
            data = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]
       
            return data, colnames

    # 9
    def target_donors(self):
        with self.conn:
            cur = self.conn.cursor()
 
            cur.execute("SELECT donor_first_name as 'First Name', donor_last_name as 'Last Name', donor_street_address as 'Street Address', donor_city as 'City', donor_state as 'State', donor_zipcode as 'Zip' FROM donors WHERE  (donor_state = 'CA' OR donor_state = 'NY' OR donor_state = 'IL') AND (donor_dob < DATE_SUB(CURDATE(), INTERVAL 65 YEAR) OR donor_dob <= DATE_SUB(CURDATE(), INTERVAL 18 YEAR) AND donor_dob >= DATE_SUB(CURDATE(), INTERVAL 24 YEAR)) ")
            data = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]
        
            return data, colnames

    # 10 new/used per genre - checkbox
    # doesn't work
    def purchased_selected_genres(self, fiction, non_fiction):
        with self.conn:
            cur = self.conn.cursor()

            print fiction
            print non_fiction

            # if fiction:
            #     genre = 'Fiction'
            #     cur.execute("SELECT organization_name AS 'Organization' FROM clients WHERE )

            cur.execute("SELECT donor_first_name, donor_last_name FROM donors NATURAL JOIN cash_donations ORDER BY date_donated ASC")
            data = cur.fetchone()
            colnames = [desc[0] for desc in cur.description]
        
            return data, colnames

    # checkbox
    # <form action="demo_form.asp">
    #     <input type="checkbox" name="vehicle" value="Bike"> I have a bike<br>
    #     <input type="checkbox" name="vehicle" value="Car" checked> I have a car<br>
    #     <input type="submit" value="Submit">
    # </form>

    # 11 book title match - text input
    def show_user_input(self, user_input):
        with self.conn:
            cur = self.conn.cursor()

            user_input = pymysql.escape_string( user_input )
            
            like = "like "
            quotation = "\""
            wildcard = "%"
            titleF = "title "
            user_input = titleF + like + quotation + wildcard + user_input + wildcard + quotation

            print user_input
            params = (user_input)
            print params

            cur.execute("SELECT title as 'Title' FROM book_inventory WHERE {0}".format(params))
            data = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]
            return data, colnames


    # 12 donor history - input
    def list_donation_history(self, donor_id):
        with self.conn:
            cur = self.conn.cursor()

            #donor_id = pymysql.escape_string( donor_id )
            cur.execute("SELECT date_donated AS 'Date Donated', quantity AS 'Quantity' FROM book_donations WHERE donor_id = %s",(donor_id))
            data=cur.fetchall()
            colnames = [desc[0] for desc in cur.description]

            return data,colnames


    # 13 # do last month
    def volunteer_purchases_last_month(self):
        with self.conn:
            cur = self.conn.cursor()

            cur.execute("SELECT volunteer_id as 'Volunteer ID', sum(quantity) as Quantity from volunteer_books_purchased WHERE date_purchased > DATE_SUB(CURDATE(), INTERVAL 1 MONTH) GROUP BY volunteer_id")
            data = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]
        
            return data, colnames


    # 14 purchased books from specific author - textinput
    def purchased_from_specified_author(self, author_fn, author_ln):
        with self.conn:
            cur = self.conn.cursor()

            cur.execute("SELECT DISTINCT organization_name as 'Organization' FROM clients NATURAL JOIN client_transaction_history NATURAL JOIN book_author WHERE clients.client_id = client_transaction_history.client_id AND client_transaction_history.isbn = book_author.isbn AND book_author.author_fn = %s AND book_author.author_ln = %s",(author_fn, author_ln))
            data = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]
        
            return data, colnames

    # 15 all publishers with 2+ new books and <5 used books
    def publisher_filter(self):
        with self.conn:
            cur = self.conn.cursor()

            cur.execute("SELECT DISTINCT publisher as 'Publisher' FROM book_inventory GROUP BY publisher, book_status HAVING ( count(book_status) > 2 AND book_status = 'New' ) OR ( count(book_status) < 5 AND book_status = 'Gently used' )")
            data = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]
        
            return data, colnames


    # 16 big donors - user textinput
    # cash + 10*(number used books) + 20*(number new books)
    def user_amount_input(self, amount):
        with self.conn:
            cur = self.conn.cursor()

            # create views
            cur.execute("create view cash_by_donor as (SELECT donor_id, sum(amount) FROM cash_donations GROUP BY donor_id)")
            cur.execute("create view new_by_donor as (SELECT donor_id, 20*sum(quantity) FROM book_donations WHERE book_status = 'New' GROUP BY donor_id)")
            cur.execute("create view used_by_donor as (SELECT donor_id, 10*sum(quantity) FROM book_donations WHERE book_status = 'Gently used' GROUP BY donor_id)")
            
            cur.execute("SELECT *, 10*sum(quantity) FROM book_donations WHERE book_status = 'Gently used' GROUP BY donor_id")
            # cur.execute("SELECT * FROM cash_donations c RIGHT JOIN book_donations b WHERE b.donor_id = c.donor_id")
            
            data = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]

            # get rid of views
            cur.execute("drop view cash_by_donor")
            cur.execute("drop view new_by_donor")
            cur.execute("drop view used_by_donor")
        
            return data, colnames


    # 17
    # ratio of books:clients grouped by reading level
    # improve upon, if there is time
    def books_clients_ratio(self):
        with self.conn:
            cur = self.conn.cursor()

            # create views
            cur.execute("create view clients_per_level as (SELECT reading_level, count(client_id) as clients FROM clients_readinglevel group by reading_level)")
            # cur.execute("create view clients_per_level as (SELECT r.reading_level, count(client_id) as clients FROM clients_readinglevel c RIGHT JOIN reading_levels r group by r.reading_level)")
            cur.execute("create view books_per_level as (SELECT reading_level, sum(quantity) as books FROM book_inventory group by reading_level)")
            
            # select
            # cur.execute("SELECT eading_level, books/clients from clients_per_level NATURAL JOIN books_per_level")
            cur.execute("SELECT b.reading_level as 'Reading Level', books/clients as 'Books:Clients' from clients_per_level c RIGHT JOIN books_per_level b on c.reading_level = b.reading_level")
            data = cur.fetchall()
            colnames = [ desc[0] for desc in cur.description ]

            # get rid of views
            cur.execute("drop view clients_per_level")
            cur.execute("drop view books_per_level")

            return data, colnames

    # 18
    def clients_with_requests(self):
        with self.conn:
            cur = self.conn.cursor()

            cur.execute("SELECT DISTINCT client_id as 'Client ID', organization_name as 'Organization' FROM client_book_requests NATURAL JOIN clients WHERE request_status = 'In Progress'")
            data = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]
        
            return data, colnames

