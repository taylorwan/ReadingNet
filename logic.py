import pymysql


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
        # self.conn = pymysql.connect(self.opts.DB_HOST, self.opts.DB_USER,
                                    # self.opts.DB_PASSWORD, self.opts.DB_NAME)
        self.conn = pymysql.connect('localhost','readingNet280', 'p4ssw0rd', 'readingNet' )

    def search(self, isbn, title, author_fn, author_ln, publisher):
        print "In search" 
        cur = self.conn.cursor()

        isbn = pymysql.escape_string( isbn )
        title = pymysql.escape_string( title )
        author = pymysql.escape_string( author )
        publisher = pymysql.escape_string( publisher )
        print isbn
        print title
        print author 
        print publisher
        #cur.execute("SELECT * FROM book_inventory WHERE title like '%%title%' AND isbn like '%%isbn%' AND author like '%%author%' AND publisher like '%%publisher%'",(title, isbn, author, publisher))
        cur.execute("SELECT * FROM book_inventory WHERE title = %s AND isbn = %s AND author_ = %s AND publisher = %s",(title, isbn, author, publisher))
        data = cur.fetchall()

        colnames = [desc[0] for desc in cur.description]

        return data, colnames

    def addDonor( self, donorID, firstName, lastName, DOB, gender, phoneNum, email, streetAddress, city, state, zipCode):
        print "in addDonor"
        
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
        print "in add_volunteer"
        
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
        print "in add level"
        
        with self.conn:
            cur = self.conn.cursor()  
            reading_level = pymysql.escape_string( reading_level ) 

            cur.execute("INSERT INTO reading_levels(reading_level) VALUES (%s)",(reading_level))
            
            self.conn.commit()

            return cur

    def add_genre(self, genre, description):
        print "in add genre"

        with self.conn:
            cur = self.conn.cursor()  
            genre = pymysql.escape_string( genre ) 
            description = pymysql.escape_string( description ) 

            cur.execute("INSERT INTO genres(genre_type, description) VALUES (%s, %s)",(genre, description))
            
            self.conn.commit()

            cur.execute("SELECT * FROM genres")
            data = cur.fetchall()
            print cur.rowcount

            for row in data :
                print row

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
        print "in addbook"
        
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
                cur.execute("INSERT INTO book_donations(isbn, title, book_status, donor_id, date_donated, quantity) VALUES (%s, %s, %s, %s, %s, %s)",(isbn, title, bookStatus, donorID, donationDate, quantity))
                cur.execute("INSERT INTO book_author(isbn, title, author_fn, author_ln) VALUES (%s, %s, %s, %s)",(isbn, title, author_fn, author_ln))
            else:
                existing_quant = 0
                existing_quant = exists[7]
                new_quantity = existing_quant + quantity
                cur.execute("UPDATE book_inventory SET quantity=%s WHERE isbn=%s AND book_status=%s",(new_quantity, isbn, bookStatus))
                cur.execute("INSERT INTO book_donations(isbn, title, book_status, donor_id, date_donated, quantity) VALUES (%s, %s, %s, %s, %s, %s)",(isbn, title, bookStatus, donorID, donationDate, quantity))

            cur.execute("SELECT * FROM book_inventory")
            data = cur.fetchall()
            print "printing book_inventory"
            for row in data:
                print row

            cur.execute("SELECT * FROM book_donations")
            data = cur.fetchall()
            print cur.rowcount
            print "printing donations"
            for row in data:
                print row;

            self.conn.commit()

            return cur

    
    def add_client(self, client_ID, organization_name, client_phone_num, email, street_address, city, state, zipCode, tokens, new_count, used_count):
        print "int add client"

        with self.conn:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO clients(client_id, organization_name, client_phone_num, client_email, client_street_address, client_city, client_state, client_zipcode, client_tokens, new_count, used_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(client_ID, organization_name, client_phone_num, email, street_address, city, state, zipCode, tokens, new_count, used_count))

            self.conn.commit()

            return cur

    def add_tokens(self, client_ID, token_amount):
        print "in add tokens"

        #client_tokens
        with self.conn:
            cur = self.conn.cursor()

            print client_ID
            token_amount = int(token_amount)

            cur.execute("SELECT * FROM clients WHERE client_id = %s",(client_ID))
            data = cur.fetchone()
            client_current_tokens = data[8]
            new_token_amount = client_current_tokens + token_amount
            cur.execute("UPDATE clients SET client_tokens = %s WHERE client_id = %s",(new_token_amount, client_ID))

            self.conn.commit()

            return cur

    def new_cash_donation(self, donor_ID, amount, donation_date):
        print "in cash donation"
        
        with self.conn:
            cur = self.conn.cursor()

            donor_ID = pymysql.escape_string( donor_ID )
            amount = pymysql.escape_string( amount )
            amount = float(amount)
            donation_date = pymysql.escape_string( donation_date )

            cur.execute("INSERT INTO cash_donations(donor_id, amount, date_donated) VALUES (%s, %s, %s)",(donor_ID, amount, donation_date))
            cur.execute("SELECT * FROM cash_reserves WHERE cash_id = 1")
            
            data = cur.fetchone()
            print cur.rowcount
            current_cash_reserves = data[0]
            new_cash = current_cash_reserves + amount;

            cur.execute("UPDATE cash_reserves SET cash_amount = %s WHERE cash_id = 1",(new_cash))

            # threshold for dispersing tokens will be $500
            if new_cash > 500:
                cur.execute("SELECT * FROM clients")
                row = cur.fetchone()
                while row is not None:
                    client_ID = row[0]
                    print client_ID
                    self.add_tokens(client_ID, 3)
                    row = cur.fetchone()

            self.conn.commit()

            return cur

    def purchase_new_book(self, volunteer_ID, isbn, title, reading_level, genre, book_status, edition, publisher, quantity, author_fn, author_ln, purchase_date, cost):
        print "in cash donation"
        
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
                print "transation cancelled"
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


