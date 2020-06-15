from flask import Blueprint, request, render_template, flash, redirect, url_for, g
from werkzeug.exceptions import abort
from app.auth import login_required
from app.models import Book
from app import db
import requests
 
# Define the blueprint: 'register', set its url prefix: app.url/register
mod_register = Blueprint('register', __name__, url_prefix='/register')


@mod_register.route('/')
def index():
    return render_template('register/index.html')


@mod_register.route('/isbn', methods=('GET', 'POST'))
def isbn():
    isbn = request.args.get('isbn')
    book_data =[]

    if request.method == 'POST' and isbn is None:
        isbn = request.form['isbn']
        error = None

        if not isbn:
            error = 'isbn is required.'

        if error is not None:
            flash(error)
        else:
            return redirect(url_for('register.isbn', isbn = isbn))

    if isbn is not None:
        url = 'https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404?applicationId=1053085901834686387&isbn=' + isbn
        response = requests.get(url)
        book_data = response.json()['Items'][0]['Item']

        if request.method == 'POST':
            title = request.form['title']
            author = request.form['author']
            publisher_name = request.form['publisher_name']
            sales_date = request.form['sales_date']
            image_url = book_data['largeImageUrl']
            donor = request.form['donor']

            data = Book(isbn, title, author, publisher_name, sales_date, image_url, donor)
            db.session.add(data)
            db.session.commit()

            return redirect(url_for('register.success'))

    return render_template('register/isbn.html', isbn = isbn, book_data = book_data)


@mod_register.route('/manual')
def manual():

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        publisher_name = request.form['publisher_name']
        sales_date = request.form['sales_date']
        image_url = None
        donor = request.form['donor']

        data = Book(isbn, title, author, publisher_name, sales_date, image_url, donor)
        db.session.add(data)
        db.session.commit()

        return redirect(url_for('register.success'))

    return render_template('register/manual.html')


@mod_register.route('/success')
def success():
    return render_template('register/success.html')
    