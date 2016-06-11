"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask import url_for
from flask import request
from flask import redirect, session, flash
from FlaskBookstore import app
import FlaskBookstore

from FlaskBookstore import *

from FlaskBookstore.models.book import Book
from FlaskBookstore.models.cartline import Cartline
from FlaskBookstore.models.bookDatabase import BookDbRepository
from FlaskBookstore.models.formValidation import FormValidation
from FlaskBookstore.models.userDatabase import UserDbRepository


bookDb = BookDbRepository()
userDb = UserDbRepository()
formInputCheck = FormValidation()

shopping_cart={}

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""

    category = bookDb.get_categories()    
    bookList = bookDb.get_books_new()
    return render_template(
        'index.html',
        title = 'Home Page',
        year = datetime.now().year,
        books = bookList,
        categories = category
    )


@app.route('/list/<category>')
def list(category):    
    categ = bookDb.get_categories()
    bookList = bookDb.get_books(category)
    return render_template(
        'list.html',
        title = 'List books',
        year = datetime.now().year,
        category = category,
        books = bookList,
        categories = categ
    )


@app.route('/addCart', methods=['GET','POST'])
def addCart():
    category = bookDb.get_categories()    
    if request.method == "POST":
        bookId = request.form['bookId']
        returnUrl = request.form['returnUrl']
        
        if bookId in shopping_cart:
            cartLine=shopping_cart[bookId]
            cartLine.quantity += 1
        else:
            book = bookDb.get_book(bookId)
            cartLine = Cartline(book,1)
            shopping_cart[bookId] = cartLine
         
        totalValue = 0.0
        for key, line in shopping_cart.items():
            totalValue += line.quantity * line.book.price

        return render_template(
            'cart.html',
            title = 'Flask Bookstore: Your Cart',
            year = datetime.now().year,
            message = 'Shopping Cart Page.',
            shopping_cart = shopping_cart,
            totalValue = totalValue,
            returnUrl = returnUrl,
            categories = category
        )


@app.route('/removeCart', methods=['GET','POST'])
def removeCart():
    category = bookDb.get_categories()
    if request.method == "POST":
        bookId = request.form['bookId']
        returnUrl = request.form['returnUrl']
       
        if bookId in shopping_cart:
            del shopping_cart[bookId]
         
        totalValue = 0.0
        for key, line in shopping_cart.items():
            totalValue += line.quantity * line.book.price

        return render_template(
            'cart.html',
            title = 'Flask Bookstore: Your Cart',
            year = datetime.now().year,
            message = 'Shopping Cart Page.',
            shopping_cart = shopping_cart,
            totalValue = totalValue,
            returnUrl = returnUrl,
            categories = category
        )


@app.route('/cart', methods=['GET','POST'])
def cart():
    """Renders the cart page."""
    category = bookDb.get_categories()
    if request.method == "GET":       
        totalValue = 0.0
        for key, line in shopping_cart.items():
            totalValue += line.quantity * line.book.price

        return render_template(
            'cart.html',
            title = 'Flask Bookstore: Your Cart',
            year = datetime.now().year,
            message = 'Shopping Cart Page.',
            shopping_cart = shopping_cart,
            totalValue = totalValue,
            categories = category     
            )


@app.route('/checkout', methods=['GET','POST'])
def checkout():
    """Renders the checkout page."""

    if request.method == "GET":
        totalValue = 0.0
        for key, line in shopping_cart.items():
            totalValue += line.quantity * line.book.price

        if totalValue == 0.0:
            return redirect(url_for('home'))
        else:
            return render_template(
                'checkout.html',
                title = 'Checkout',
                year = datetime.now().year,
                message = 'Your checkout page.',
                )

    elif request.method == "POST":
        #get form values from client
        shipTo = request.form["shipto"]
        address_line1 = request.form["address_line1"]
        address_line2 = request.form["address_line2"]
        city = request.form["city"]
        state = request.form["state"]
        zip = request.form["zip"]
        country = request.form["country"]

        #validate form fields
        name_valid = formInputCheck.validate_name(shipTo)
        address_line1_valid = formInputCheck.validate_address(address_line1)
        if address_line2:
            address_line2_valid = formInputCheck.validate_address(address_line2)
        city_valid = formInputCheck.validate_city(city)
        state_valid = formInputCheck.validate_state(state)
        zip_valid = formInputCheck.validate_zip(zip)
        if country:
            country_valid = formInputCheck.validate_country(country)

        errorName = ""
        errorLine1 = ""
        errorLine2 = ""
        errorCity = ""
        errorState = ""
        errorZip = ""
        errorCountry = ""

        if name_valid and address_line1_valid and city_valid and state_valid and zip_valid:
            totalValue = 0.0
            for key, line in shopping_cart.items():
                totalValue += line.quantity * line.book.price

            return render_template(
                'completed.html',
                title = 'Checkout complete',
                year = datetime.now().year,
                message ='Your checkout page.',
                shopping_cart = shopping_cart,
                totalValue = totalValue,
                shipTo = shipTo,
                address_line1 = address_line1,
                address_line2 = address_line2,
                city = city,
                state = state,
                zip = zip,
                country = country
            )

        else:
            if not name_valid:
                errorName = "Invalid: Name contains illegal characters, must start with an alphabet and can contain spaces."
            if not address_line1_valid:
                errorLine1 = "Invalid: Address contain illegal characters."
            if address_line2 and not address_line2_valid:
                errorLine2 = "Invalid: Address contain illegal characters."
            if not city_valid:
                errorCity = "Invalid: City contain illegal characters, must contain only alphabets."
            if not state_valid:
                errorState = "Invalid: State contain illegal characters, must contain only alphabets."
            if not zip_valid:
                errorZip = "Invalid: Zip should contain atleast 5 digits, ex: 98034 or 98034-3678."
            if country and not country_valid:
                errorCountry = "Invalid: Country contain illegal characters, must contain only alphabets."

            return render_template(
                'checkout.html',
                title = 'Checkout',
                year = datetime.now().year,
                message = 'Your checkout page.',
                error_name = errorName,
                error_line1 = errorLine1,
                error_line2 = errorLine2,
                error_city = errorCity,
                error_state = errorState,
                error_zip = errorZip,
                error_country = errorCountry,
                name_entered = shipTo,
                line1_entered = address_line1,
                line2_entered = address_line2,
                city_entered = city,
                state_entered = state,
                zip_entered = zip,
                country_entered = country
                )


@app.route('/login', methods=['GET','POST'])
def login():
    """Renders the login page."""

    if request.method == "POST":
        userEmail = request.form['useremail']
        userpswd = request.form['password']

        userExists = userDb.validate_user(userEmail, userpswd)

        if not userExists:
            errormsg = 'Invalid credentials. Please try again.'
            return render_template('login.html', user_name = request.form['useremail'], login_error = errormsg)
        else:
            session['username'] = request.form['useremail']
            totalValue = 0.0
            for key, line in shopping_cart.items():
                totalValue += line.quantity * line.book.price

            if totalValue == 0.0:
                return redirect(url_for('home'))
            else:
                return redirect(url_for('checkout'))
    return render_template('login.html')


@app.route('/register', methods=['GET','POST'])
def register():
    """Renders the register page."""

    if request.method == "GET":
        return render_template('register.html')

    elif request.method == "POST":
        userName = request.form['user']
        email = request.form['email']
        password = request.form['pswd']

        name_valid = formInputCheck.validate_name(userName)
        errorName = ""

        if name_valid:
            userDb.add_user(userName, email, password)
            return redirect(url_for('login'))
        else:
            errorName = "Invalid: Name contains illegal characters, must start with an alphabet and can contain spaces."
            return render_template(
                'register.html',
                title = 'Register',
                year = datetime.now().year,
                name_entered = userName,
                error_name = errorName
                )


@app.route('/logout', methods=['GET','POST'])
def logout():
    """Renders the logout page."""

    session.pop('username', None)
    return redirect(url_for('home'))








