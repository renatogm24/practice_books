from flask import render_template, request, redirect

from flask_app.models import author
from flask_app.models import book

from flask_app import app


@app.route('/books')
def list_books():
    return render_template("books/index.html",all_books=book.Book.get_all())

@app.route('/books/<int:id>')
def book_with_favorite(id):
    data = {
        "id": id,
    }
    authors = author.Author.get_authors_with_not_favorites_by_book(data)
    bookAux = book.Book.get_books_with_favorites(data)
    print(authors)
    print(bookAux)
    return render_template("books/list_favorites.html",book=bookAux, authors=authors)

@app.route('/books/save',methods=['POST'])
def create_book():
    data = {
        "title":request.form['title'],
        "num_pages":request.form['num_pages'],
    }
    book.Book.save(data)
    return redirect('/books')

@app.route('/books/add_favorite',methods=['POST'])
def add_favorite_book():
    data = {
        "author_id":request.form['author_id'],
        "book_id":request.form['book_id'],
    }
    id = request.form['book_id']
    book.Book.save_favorite(data)
    return redirect(f'/books/{id}')

