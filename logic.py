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

    def search( self, isbn, title, author, publisher):
        print "In search" 
        cur = self.conn.cursor( pymysql.cursors.DictCursor )
        isbn = pymysql.escape_string( isbn )
        title = pymysql.escape_string( title )
        author = pymysql.escape_string( author )
        publisher = pymysql.escape_string( publisher )
        print isbn
        print title
        print author 
        print publisher
        #cur.execute("SELECT * FROM book_inventory WHERE title like '%%title%' AND isbn like '%%isbn%' AND author like '%%author%' AND publisher like '%%publisher%'",(title, isbn, author, publisher))
        cur.execute("SELECT * FROM book_inventory WHERE title = %s AND isbn = %s AND author = %s AND publisher = %s",(title, isbn, author, publisher))

        return CursorIterator( cur )

    def addDonor( self, donorID, firstName, lastName, DOB, gender, phoneNum, email, streetAddress, city, state, zipCode):
        print "in addDonor"
        
        with self.conn:
            cur = self.conn.cursor()
            
            donorID = pymysql.escape_string( donorID )
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
        print "seeing all levels hopefully"
        with self.conn:      
            cur = self.conn.cursor()  

            cur.execute("SELECT * FROM reading_levels")
            data = cur.fetchall()
            print cur.rowcount

            for row in data :
                print row

    def see_all_donors(self):
        print "seeing all donors hopefully"
        with self.conn:
            cur = self.conn.cursor()

            cur.execute("SELECT * FROM donors")
            data = cur.fetchall()
            print cur.rowcount

            for row in data:
                print row

    def see_all_volunteers(self):
        print "seeing all volunteers hopefully"
        with self.conn:
            cur = self.conn.cursor()

            cur.execute("SELECT * FROM volunteers")
            data = cur.fetchall()
            print cur.rowcount

            for row in data:
                print row

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
            print "printing exists"
            print exists
            print type(quantity)
            print "printing the quantity of books just donated: "
            print quantity

            if exists == None:
                print "in none"
                cur.execute("INSERT INTO book_inventory(isbn, title, reading_level, genre_type, book_status, edition, publisher, quantity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(isbn, title, readingLevel, genre, bookStatus, edition, publisher, quantity))
                cur.execute("INSERT INTO book_donations(book_donation_id, isbn, title, book_status, donor_id, date_donated, quantity) VALUES (%s, %s, %s, %s, %s, %s)",(isbn, title, bookStatus, donorID, donationDate, quantity))
            else:
                print "in else"
                existing_quant = 0
                existing_quant = exists[7]
                print "printing existing quant: "
                print existing_quant
                print "printing quantity of books just donated: "
                print quantity
                new_quantity = existing_quant + quantity
                print quantity
                cur.execute("UPDATE book_inventory SET quantity=%s WHERE isbn=%s AND book_status=%s",(new_quantity, isbn, bookStatus))


            cur.execute("SELECT * FROM book_inventory")
            
            data = cur.fetchall()
            print "printing book_inventory"
            for row in data:
                print row

            cur.execute("SELECT * FROM book_donations")
            data = cur.fetchall()
            print "printing donations"
            for row in data:
                print row;

            self.conn.commit()

            return cur








