from flask import render_template, request, redirect

from flask_app.models import author
from flask_app.models import book

from flask_app import app

@app.route('/')
def index():
    return redirect("/authors")

@app.route('/authors')
def list_authors():
    return render_template("authors/index.html",all_authors=author.Author.get_all())

@app.route('/authors/<int:id>')
def author_with_favorite(id):
    data = {
        "id": id,
    }
    books = book.Book.get_books_with_not_favorites_by_author(data)
    print(books)
    return render_template("authors/list_favorites.html",author=author.Author.get_author_with_favorites(data), books=books)

@app.route('/authors/save',methods=['POST'])
def create():
    data = {
        "name":request.form['name'],
    }
    author.Author.save(data)
    return redirect('/authors')

@app.route('/authors/add_favorite',methods=['POST'])
def add_favorite():
    data = {
        "author_id":request.form['author_id'],
        "book_id":request.form['book_id'],
    }
    id = request.form['author_id']
    book.Book.save_favorite(data)
    return redirect(f'/authors/{id}')

