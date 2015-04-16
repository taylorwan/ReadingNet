# third party modules
from flask import (Flask, render_template, request)
import pymysql

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

@app.route( '/' )
def splash():
    return render_template( 'index.html' )

@app.route( '/volunteer', methods=['GET'] )
def volunteer():
	return render_template( 'volunteer.html' )

@app.route( '/browse', methods=['GET'] )
def client():
	return render_template( 'search.html' )

@app.route( '/donor', methods=['GET'] )
def donor():
	return render_template( 'donor.html' )

# ????? do we need this
# @app.route( '/search', methods=['GET'] )
# def splash():
#     return render_template( 'search.html' )

@app.route('/search', methods=['GET'] )
def results():
    isbn = request.args.get( 'isbn' )
    title = request.args.get( 'title' )
    author_fn = request.args.get( 'author_fn' )
    author_ln = request.args.get( 'author_ln' )
    publisher = request.args.get( 'publisher' )
    status = request.args.get( 'status' )

    if isbn == "": 
    	isbn = "IS NOT NULL"
    if title == "":
    	title = "IS NOT NULL"
    if author_fn == "":
    	author_fn = "IS NOT NULL"
    if author_ln =="":
    	author_ln = "IS NOT NULL"
    if publisher == "":
    	publisher = "IS NOT NULL"
    if status == "":
    	status = "IS NOT NULL"

    data = db.search(isbn, title, author_fn, author_ln, publisher, status)
    return render_template('search_results.html', data=data)

@app.route('/buy_books', methods=['GET', 'POST'])
def buy_books():
	if request.method == 'POST':

		checked_numbers = request.form.getlist('numbers')
		keys = request.form.getlist('keys')
		combo = []
		
		for number in checked_numbers:
			combo.append( number )
		
		count = 0
		for key in keys:
			combo[count] += "_" + key
			count += 1		

		db.process_purchase(combo)
		return render_template('success.html')
	else:
		return render_template('/search.html')

@app.route('/checkout', methods=['GET'])
def checkout():
	return render_template('get_info.html')

@app.route('/checkout_info', methods=['POST'])
def checkout_info():
	if request.method == 'POST':
		client_ID = request.form['client_ID']
		error = db.checkout(client_ID, False)	
		return render_template('success.html')
	else:
		return render_template('/search.html')


@app.route('/see_all_levels', methods=['GET', 'POST'])
def see_all_levels():
	if request.method == 'POST':
		data, colnames = db.see_all_levels();
		return render_template('results.html', data=data, colnames=colnames)
	else:
		return render_template('/volunteer.html')

@app.route('/see_all_donors', methods=['GET', 'POST'])
def see_all_donors():
	if request.method == 'POST':
		data, colnames = db.see_all_donors();
		return render_template( 'results.html', data=data, colnames=colnames )
	else:
		return render_template('/volunteer.html')

@app.route('/see_all_volunteers', methods=['GET', 'POST'])
def see_all_volunteers():
	if request.method == 'POST':
		data, colnames = db.see_all_volunteers();
		return render_template( 'results.html', data=data, colnames=colnames )
	else:
		return render_template('/volunteer.html')

@app.route('/see_all_book_inventory', methods=['GET', 'POST'])
def see_all_book_inventory():
	if request.method == 'POST':
			data, colnames = db.see_all_book_inventory()
			return render_template( 'results.html', data=data, colnames=colnames)
	else:
		return render_template('/volunteer.html')

@app.route('/see_all_donations', methods=['GET', 'POST'])
def see_all_donations():
	if request.method == 'POST':
			data, colnames = db.see_all_donations()
			return render_template('results.html',data=data, colnames=colnames)
	else:
		return render_template('/volunteer.html')

@app.route('/see_all_cash_donations', methods=['GET', 'POST'])
def see_all_cash_donations():
	if request.method == 'POST':
		data, colnames = db.see_all_cash_donations()
		return render_template('results.html',data=data, colnames=colnames)
	else:
		return render_template('/volunteer.html')


@app.route('/see_cash_reserves', methods=['GET', 'POST'])
def see_cash_reserves():
	if request.method == 'POST':
		data, colnames = db.see_cash_reserves()
		return render_template('results.html',data=data, colnames=colnames)
	else:
		return render_template('/volunteer.html')

@app.route('/add_genre', methods=['GET','POST'] )
def add_genre():
	if request.method == 'POST':
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
		donorID = request.form[ 'donorID' ]
		
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

@app.route('/add_new_client', methods=['GET','POST'])
def add_new_client():
	if request.method == 'POST':
		client_ID = request.form[ 'client_ID' ]
		organization_name = request.form[ 'organization_name' ]
		client_phone_num = request.form[ 'client_phone_num' ]
		email = request.form[ 'email' ]
		street_address = request.form[ 'street_address' ]
		city = request.form[ 'city' ]
		state = request.form[ 'state' ]
		zipCode = request.form[ 'zipCode' ]
		tokens = request.form[ 'tokens' ]
		new_count = request.form[ 'new_count' ]
		used_count = request.form[ 'used_count' ]
		
		db.add_client(client_ID, organization_name, client_phone_num, email, street_address, city, state, zipCode, tokens, new_count, used_count)

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

@app.route('/add_new_cash_donation', methods=['GET', 'POST'])
def add_new_cash_donation():
	if request.method == 'POST':
		donor_ID = request.form[ 'donorID' ]
		amount = request.form[ 'amount' ]
		donation_date = request.form[ 'donation_date' ]

		db.new_cash_donation(donor_ID, amount, donation_date)
		return render_template('success.html')
	else:
		return render_template('/volunteer.html')

@app.route('/change_request', methods=['GET', 'POST'])
def change_request_status():
	if request.method == 'POST':
		request_id = request.form['request_id' ]
   	 	status = request.form['status' ]
		db.change_request_status(request_id, status);

		return render_template('success.html')
	else:
		return render_template('/volunteer.html')

@app.route('/purchase_new_book', methods=['GET', 'POST'])
def purchase_new_book():
	if request.method == 'POST':
		volunteer_ID = request.form[ 'volunteer_ID' ]
		isbn = request.form[ 'isbn' ]
		title = request.form[ 'title' ]
		reading_level = request.form[ 'reading_level' ]
		genre = request.form[ 'genre' ]
		book_status = request.form[ 'book_status' ]
		edition = request.form[ 'edition' ]
		publisher = request.form[ 'publisher' ]
		quantity = request.form[ 'quantity' ]
		author_fn = request.form[ 'author_fn' ]
		author_ln = request.form[ 'author_ln' ]
		purchase_date = request.form[ 'purchase_date']
		cost = request.form[ 'cost']
		
		db.purchase_new_book(volunteer_ID, isbn, title, reading_level, genre, book_status, edition, publisher, quantity, author_fn, author_ln, purchase_date, cost) 		
		return render_template('success.html')
	else:
		return render_template('/volunteer.html')

@app.route('/add_tokens', methods=['GET', 'POST'])
def add_tokens():
	if request.method == 'POST':
		client_ID = request.form[ 'client_ID' ]
		token_amount = request.form[ 'token_amount' ]

		db.add_tokens(client_ID, token_amount)
		return render_template('success.html')
	else:
		return render_template('/volunteer.html')


### Queries Taylor 4.14

@app.route( '/queries')
def show_queries():
    return render_template( 'queries.html')

# 4
@app.route('/author_donators', methods=['GET', 'POST'])
def author_donators():
	data, colnames = db.author_donators();
	return render_template( 'results.html', data=data, colnames=colnames )

# 5
@app.route('/most_recent_donor', methods=['GET', 'POST'])
def most_recent_donor():
	data, colnames = db.most_recent_donor();
	return render_template( 'results.html', data=data, colnames=colnames )

# 6
@app.route('/avg_tokens', methods=['GET', 'POST'])
def avg_tokens():
	data, colnames = db.avg_tokens();
	return render_template( 'results.html', data=data, colnames=colnames )

@app.route('/min_tokens', methods=['GET', 'POST'])
def min_tokens():
	data, colnames = db.min_tokens();
	return render_template( 'results.html', data=data, colnames=colnames )

@app.route('/max_tokens', methods=['GET', 'POST'])
def max_tokens():
	data, colnames = db.max_tokens();
	return render_template( 'results.html', data=data, colnames=colnames )

# 7
@app.route('/book_per_genre', methods=['GET', 'POST'])
def book_per_genre():
	data, colnames = db.book_per_genre();
	return render_template( 'results.html', data=data, colnames=colnames )

@app.route('/book_per_level', methods=['GET', 'POST'])
def book_per_level():
	data, colnames = db.book_per_level();
	return render_template( 'results.html', data=data, colnames=colnames )

@app.route('/book_per_genre_level', methods=['GET', 'POST'])
def book_per_genre_level():
	data, colnames = db.book_per_genre_level();
	return render_template( 'results.html', data=data, colnames=colnames )


# 8
@app.route('/top_book', methods=['GET', 'POST'])
def top_book():
	data, colnames = db.top_book();
	return render_template( 'results.html', data=data, colnames=colnames )

# 9
@app.route('/target_donors', methods=['GET', 'POST'])
def target_donors():
	data, colnames = db.target_donors();
	return render_template( 'results.html', data=data, colnames=colnames )

# 10
@app.route('/purchased_selected_genres', methods=['GET', 'POST'])
def purchased_selected_genres():
	data, colnames = db.purchased_selected_genres();
	return render_template( 'results.html', data=data, colnames=colnames )

# 11
# 12

# 13
@app.route('/volunteer_purchases_last_month', methods=['GET', 'POST'])
def volunteer_purchases_last_month():
	data, colnames = db.volunteer_purchases_last_month();
	return render_template( 'results.html', data=data, colnames=colnames )

# 14
@app.route('/purchased_from_specified_author', methods=['GET', 'POST'])
def purchased_from_specified_author():
	data, colnames = db.purchased_from_specified_author();
	return render_template( 'results.html', data=data, colnames=colnames )

# 15
@app.route('/publisher_filter', methods=['GET', 'POST'])
def publisher_filter():
	data, colnames = db.publisher_filter();
	return render_template( 'results.html', data=data, colnames=colnames )

# 16
# @app.route('/#', methods=['GET', 'POST'])
# def #():
	# data, colnames = db.#();
	# return render_template( 'results.html', data=data, colnames=colnames )

# 17
@app.route('/books_clients_ratio', methods=['GET', 'POST'])
def books_clients_ratio():
	data, colnames = db.books_clients_ratio();
	return render_template( 'results.html', data=data, colnames=colnames )

# 18
@app.route('/clients_with_requests', methods=['GET', 'POST'])
def clients_with_requests():
	data, colnames = db.clients_with_requests();
	return render_template( 'results.html', data=data, colnames=colnames )

if __name__ == '__main__':
    app.run()
