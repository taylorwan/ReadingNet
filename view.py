# third party modules
from flask import (Flask, render_template, request)

# project modules
import config
from logic import Database

# instanciate application and database object
app = Flask(__name__)
db = Database(config)


# configure the web abb according to the config object
app.host = config.APP_HOST
app.port = config.APP_PORT
app.debug = config.APP_DEBUG


@app.route( '/', methods=['GET'] )
def splash():
    print "loading search"
    return render_template( 'search.html' )

@app.route( '/search', methods=['GET'] )
def results():
    isbn = request.args.get( 'isbn' )
    title = request.args.get( 'title' )
    author = request.args.get( 'author' )
    publisher = request.args.get( 'publisher' )

    if isbn == "": 
    	isbn = "IS NOT NULL"
    if title == "":
    	title = "IS NOT NULL"
    if author == "":
    	author = "IS NOT NULL"
    if publisher == "":
    	publisher = "IS NOT NULL"

    results = db.search( isbn, title, author, publisher)
    print "routing to results"
    return render_template( 'results.html', results = results )

if __name__ == '__main__':
    app.run()
