from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

class Book:
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.num_pages = data['num_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorites_by = []
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO books ( title , num_pages, created_at, updated_at ) VALUES ( %(title)s , %(num_pages)s , NOW() , NOW() );"
        return connectToMySQL('core_books').query_db( query, data )
    
    @classmethod
    def get_books_with_favorites(cls, data):
        query = "SELECT * FROM books LEFT JOIN favorites ON books.id = favorites.book_id left join authors on authors.id = favorites.author_id WHERE books.id = %(id)s;"
        results = connectToMySQL('core_books').query_db(query, data)
        book = cls(results[0])
        for authorAux in results:
            author_data = {
                "id" : authorAux["authors.id"],
                "name" : authorAux["name"],
                "created_at" : authorAux["authors.created_at"],
                "updated_at" : authorAux["authors.updated_at"],
            }
            book.favorites_by.append( author.Author( author_data ) )
        return book
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"
        results = connectToMySQL('core_books').query_db(query)
        books = []
        for book in results:
            books.append( cls(book) )
        return books

    @classmethod
    def get_books_with_not_favorites_by_author(cls, data):
        query = "select distinct books.id, books.title, books.num_pages, books.created_at, books.updated_at from books left join favorites on books.id = favorites.book_id left join authors on authors.id = favorites.author_id where books.id not in (select books.id as id from books left join favorites on books.id = favorites.book_id left join authors on authors.id = favorites.author_id where author_id = %(id)s);"
        results = connectToMySQL('core_books').query_db(query, data)
        books = []
        for book in results:
            books.append( cls( book ) )
        return books

    @classmethod
    def save_favorite(cls, data ):
        query = "INSERT INTO favorites ( author_id , book_id ) VALUES ( %(author_id)s , %(book_id)s );"
        return connectToMySQL('core_books').query_db( query, data )