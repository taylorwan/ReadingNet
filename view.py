# third party modules
from flask import (Flask, render_template, request)
import Tkinter
import tkMessageBox

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

@app.route( '/volunteer', methods=['GET'] )
def load_forms():
	print "loading the volunteer forms"
	return render_template( 'volunteer.html')


@app.route( '/add_new_donor', methods=['GET','POST'] )
def add_new_donor():
	print ("we are in")
	if request.method == 'POST':
		print "its a post"
		donorID = request.form[ 'donorID' ]
		if donorID == "":
			render_template('/error.html')
		phoneNum = request.form[ 'phoneNum' ]
		email = request.form[ 'email' ]
		firstName = request.form[ 'firstName' ]
		lastName = request.form[ 'lastName' ]
		DOB = request.form[ 'DOB' ]
		streetAddress = request.form[ 'streetAddress' ]
		zipCode = request.form[ 'zipCode' ]
		gender = request.form[ 'gender' ]
		print("the donor id is: " + donorID)
		db.addDonor(donorID, phoneNum, email, firstName, lastName, DOB, streetAddress, zipCode, gender)
		return render_template( 'success.html' )
	
	else:
		return render_template('/volunteer.html')

if __name__ == '__main__':
    app.run()
