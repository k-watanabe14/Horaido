from flask import Blueprint, request, render_template, flash, session, redirect, url_for, g
from werkzeug.exceptions import abort
from app.auth import login_required
from app.models import Book, History, User, TagMaps, Tags
from app import db
from app.auth import load_logged_in_user
import datetime
from dateutil.relativedelta import relativedelta
from app.forms import BookForm
from app.common import display_errors

# Define the blueprint: 'register', set its url prefix: app.url/register
mod_book = Blueprint('book', __name__, url_prefix='/book')


@mod_book.route('/<int:book_id>')
@login_required
def index(book_id):

    book = Book.query.filter_by(id=book_id).first()
    tags = TagMaps.query.filter_by(book_id=book.id).join(Tags).add_columns(Tags.tag_name)
    histories = History.query.filter_by(book_id=book.id).join(User).add_columns(User.username)

    # Page for Detail of book
    return render_template('book/index.html', book=book, tags=tags, histories=histories)


@mod_book.route('/<int:book_id>/borrow', methods=('GET', 'POST'))
@login_required
def borrow(book_id):

    book = Book.query.filter_by(id=book_id).first()

    if request.method == 'POST':
        error = None

        if error is not None:
            flash(error)
        else:
            user_id = session.get('user_id')
            checkout_date = datetime.datetime.today()
            due_date = (datetime.datetime.today() + relativedelta(months=1))
            return_date = None

            # Add history data into Rental History
            history_data = History(book_id, user_id, checkout_date, due_date, return_date)
            db.session.add(history_data)

            # Update book data in a book record
            borrower = User.query.filter_by(id=user_id).first()
            book.borrower_id = borrower.id
            book.checkout_date = checkout_date

            db.session.commit()

            flash("「" + book.title + "」を借りました。")

            return redirect(url_for('index'))

    return render_template('book/borrow.html', book=book)


@mod_book.route('/<int:book_id>/return', methods=('GET', 'POST'))
@login_required
def return_(book_id):

    book = Book.query.filter_by(id=book_id).first()

    if request.method == 'POST':
        error = None

        if error is not None:
            flash(error)
        else:
            user_id = session.get('user_id')
            history = History.query.filter(History.user_id==user_id, History.book_id==book_id).first()

            # Update return date in a rental_history record
            history.return_date = datetime.datetime.today()

            # Update Book data in a book record
            book.borrower_id = None
            book.checkout_date = None

            db.session.commit()

            flash("「" + book.title + "」を返しました。")

            return redirect(url_for('index'))

    return render_template('book/return.html', book=book)

# TODO: Add function to edit book tags
@mod_book.route('/<int:book_id>/edit', methods=('GET', 'POST'))
@login_required
def edit(book_id):

    book = Book.query.filter_by(id=book_id).first()

    form = BookForm()

    if form.validate_on_submit():

        # Update date in a book record
        book.isbn = request.form['isbn']
        book.title = request.form['title']
        book.author = request.form['author']
        book.publisher_name = request.form['publisher_name']
        book.sales_date = request.form['sales_date']
        if 'book_image' in request.files:
            book.image_url = get_new_image_url(request.files)

        db.session.commit()

        flash('編集しました')
        return redirect(url_for('book.index', book_id=book_id))

    else:
        display_errors(form.errors.items)

    return render_template('book/edit.html', book=book, form=form)