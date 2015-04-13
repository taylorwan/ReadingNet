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
        self.conn = pymysql.connect('localhost','user280', 'p4ssw0rd', 'project280' )

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

    def addDonor( self, donorID, phoneNum, email, firstName, lastName, DOB, streetAddress, zipCode, gender):
        print "in addDonor"
        cur = self.conn.cursor( pymysql.cursors.DictCursor )
        
        print donorID
        donorID = pymysql.escape_string( donorID )
        phoneNum = pymysql.escape_string( phoneNum )
        email = pymysql.escape_string( email )
        firstName = pymysql.escape_string( firstName )
        lastName = pymysql.escape_string( lastName )
        DOB = pymysql.escape_string( DOB )
        zipCode = pymysql.escape_string( zipCode )
        gender = pymysql.escape_string( gender )

        cur.execute("INSERT INTO donors (donor_id, phone_num, email, first_name, last_name, street_address, dob, zip_code, gender) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s )",(donorID, phoneNum, email, firstName, lastName, streetAddress, DOB, zipCode, gender))
        print "did we insert?"
        return CursorIterator( cur )


