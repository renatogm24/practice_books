from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

class Author:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorites = []
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO authors ( name , created_at, updated_at ) VALUES ( %(name)s , NOW() , NOW() );"
        return connectToMySQL('core_books').query_db( query, data )
    
    @classmethod
    def get_author_with_favorites(cls, data):
        query = "SELECT * FROM authors LEFT JOIN favorites ON authors.id = favorites.author_id left join books on books.id = favorites.book_id WHERE authors.id = %(id)s;"
        results = connectToMySQL('core_books').query_db(query, data)
        author = cls(results[0])
        for bookAux in results:
            book_data = {
                "id" : bookAux["books.id"],
                "title" : bookAux["title"],
                "num_pages" : bookAux["num_pages"],
                "created_at" : bookAux["books.created_at"],
                "updated_at" : bookAux["books.updated_at"],
            }
            author.favorites.append( book.Book( book_data ) )
        return author
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM authors;"
        results = connectToMySQL('core_books').query_db(query)
        authors = []
        for author in results:
            authors.append( cls(author) )
        return authors

    @classmethod
    def get_authors_with_not_favorites_by_book(cls, data):
        query = "select distinct authors.id, authors.name, authors.created_at, authors.updated_at from authors left join favorites on authors.id = favorites.author_id left join books on books.id = favorites.book_id where authors.id not in (select authors.id as id from authors left join favorites on authors.id = favorites.author_id left join books on books.id = favorites.book_id where book_id = %(id)s);"
        results = connectToMySQL('core_books').query_db(query, data)
        authors = []
        for author in results:
            authors.append( cls( author ) )
        return authors