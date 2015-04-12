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

    def search( self, query ):
        print "in search in database"
        cur = self.conn.cursor( pymysql.cursors.DictCursor )
        query = pymysql.escape_string( query )
        cur.execute( 'SELECT * FROM levels'.format( query ) )

        return CursorIterator( cur )
