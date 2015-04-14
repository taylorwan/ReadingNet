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

@app.route('/see_all_levels', methods=['GET', 'POST'])
def see_all_levels():
	if request.method == 'POST':
		db.see_all_levels();
		return render_template( 'success.html' )
	else:
		return render_template('/volunteer.html')

@app.route('/see_all_donors', methods=['GET', 'POST'])
def see_all_donors():
	if request.method == 'POST':
		db.see_all_donors();
		return render_template( 'success.html' )
	else:
		return render_template('/volunteer.html')

@app.route('/see_all_volunteers', methods=['GET', 'POST'])
def see_all_volunteers():
	if request.method == 'POST':
		db.see_all_volunteers();
		return render_template( 'success.html' )
	else:
		return render_template('/volunteer.html')

@app.route('/see_all_book_inventory', methods=['GET', 'POST'])
def see_all_book_inventory():
	if request.method == 'POST':
			db.see_all_book_inventory()
			return render_template( 'success.html' )
	else:
		return render_template('/volunteer.html')

@app.route('/see_all_donations', methods=['GET', 'POST'])
def see_all_donations():
	if request.method == 'POST':
			db.see_all_donations()
			return render_template( 'success.html' )
	else:
		return render_template('/volunteer.html')

@app.route( '/volunteer', methods=['GET'] )
def load_forms():
	return render_template( 'volunteer.html')

@app.route( '/add_genre', methods=['GET','POST'] )
def add_genre():
	if request.method == 'POST':
		print "its a post"
		genre = request.form[ 'genre' ]
		desc = request.form[ 'description' ]
		db.add_genre(genre, desc)
		return render_template( 'success.html' )
	else:
		return render_template('/volunteer.html')
	

# Add a new donor to the database
# if any of the input fields are left blank, redirects to an error page
@app.route( '/add_new_donor', methods=['GET','POST'] )
def add_new_donor():
	if request.method == 'POST':
		print "its a post"
		donorID = request.form[ 'donorID' ]
		if donorID == "":
			render_template('/error.html')

		firstName = request.form[ 'firstName' ]
		if firstName =="":
			render_template('/error.html')
		
		lastName = request.form[ 'lastName' ]
		if lastName =="":
			render_template('/error.html')

		DOB = request.form[ 'DOB' ]
		if DOB =="":
			render_template('/error.html')

		gender = request.form[ 'gender' ]
		if gender =="":
			render_template('/error.html')

		phoneNum = request.form[ 'phoneNum' ]
		if phoneNum =="":
			render_template('/error.html')

		email = request.form[ 'email' ]
		if email =="":
			render_template('/error.html')

		streetAddress = request.form[ 'streetAddress' ]
		if streetAddress =="":
			render_template('/error.html')

		city = request.form[ 'city' ]
		if city =="":
			render_template('/error.html')

		state = request.form[ 'state' ]
		if state =="":
			render_template('/error.html')

		zipCode = request.form[ 'zipCode' ]
		if zipCode =="":
			render_template('/error.html')

		db.addDonor(donorID, firstName, lastName, DOB, gender, phoneNum, email, streetAddress, city, state, zipCode)
		return render_template( 'success.html' )
	
	else:
		return render_template('/volunteer.html')

@app.route('/add_new_volunteer', methods=['GET','POST'])
def add_new_volunteer():
	if request.method == 'POST':
		volunteerID = request.form[ 'volunteerID' ]
		if volunteerID == "":
			render_template('/error.html')

		firstName = request.form[ 'firstName' ]
		if firstName == "":
			render_template('/error.html')			

		lastName = request.form[ 'lastName' ]
		if lastName == "":
			render_template('/error.html')			

		DOB = request.form[ 'DOB' ]
		if DOB == "":
			render_template('/error.html')

		gender = request.form[ 'gender' ]
		if gender == "":
			render_template('/error.html')	

		phoneNum = request.form[ 'phoneNum' ]
		if phoneNum == "":
			render_template('/error.html')

		email = request.form[ 'email' ]
		if email == "":
			render_template('/error.html')

		streetAddress = request.form[ 'streetAddress' ]
		if streetAddress == "":
			render_template('/error.html')

		city = request.form[ 'city' ]
		if city == "":
			render_template('/error.html')			

		state = request.form[ 'state' ]
		if state == "":
			render_template('/error.html')

		zipCode = request.form[ 'zipCode' ]
		if zipCode == "":
			render_template('/error.html')


		db.add_volunteer(volunteerID, firstName, lastName, DOB, gender, phoneNum, email, streetAddress, city, state, zipCode)
		return render_template('success.html')

	else:
		return render_template('/volunteer.html')

@app.route('/add_reading_level', methods=['GET','POST'])
def add_reading_level():
	if request.method == 'POST':
		reading_level = request.form[ 'reading_level' ]
		db.add_reading_level(reading_level)
		return render_template('success.html')

@app.route('/add_new_book', methods=['GET', 'POST'])
def add_new_book():
	if request.method == 'POST':
		isbn = request.form[ 'isbn' ]
		title = request.form[ 'title' ]
		readingLevel = request.form[ 'readingLevel' ]
		genre = request.form[ 'genre' ]
		bookStatus = request.form[ 'bookStatus' ]
		edition = request.form[ 'edition' ]	
		publisher = request.form[ 'publisher' ]	
		quantity = request.form[ 'quantity' ]	
		author_fn = request.form[ 'author_fn' ]	
		author_ln = request.form[ 'author_ln' ]		
		donorID = request.form[ 'donorID' ]		
		donationDate = request.form[ 'donationDate' ]		

		db.add_book(isbn, title, readingLevel, genre, bookStatus, edition, publisher, quantity, author_fn, author_ln, donorID, donationDate)
		return render_template('success.html')
	else:
		return render_template('/volunteer.html')


if __name__ == '__main__':
    app.run()
