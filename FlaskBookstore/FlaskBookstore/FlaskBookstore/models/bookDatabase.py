import sqlite3, FlaskBookstore

from FlaskBookstore.models.book import Book


class BookDbRepository(object):
    """description of class"""

    def __init__(self):
        self.__conn = sqlite3.connect(r'FlaskBookstore\data\bookstore.sqlite')


    def __del__(self):
        self.__conn.close()


    def get_categories(self):
        try:
            cursor = self.__conn.cursor()
            results = cursor.execute("SELECT category FROM book GROUP BY category HAVING COUNT(bookId) > 5")
            categories = results.fetchall()
            category = []
            for cat in categories:
                category.append(cat[0])
            return category
        except Exception as e:
            print(e)

    def get_books_new(self):
        try:
            cursor = self.__conn.cursor()
            results = cursor.execute("SELECT * FROM book WHERE publishedDate > date('2011-01-01') ORDER BY publishedDate DESC")
            books = results.fetchall()
            bookList = [];
            for book in books:
                try:
                    id = book[1]
                    title = book[2]  
                    pageCount = book[3] 
                    author = book[4]
                    publisher = book[5]
                    publishedDate = book[6]
                    description = book[7]
                    category = book[8]
                    smallThumbnail = book[9]
                    thumbnail = book[10]
                    price = book[11]
                    bookList.append(Book(id, title, author, publisher, publishedDate,description, category,smallThumbnail,thumbnail, price, pageCount))
                except Exception as e:
                    print(e)
            return bookList
        except Exception as e:
            print(e)


    def get_books(self,category):
        try:
            cursor = self.__conn.cursor()
            results = cursor.execute("select * from book where category like '%" + category + "%'")
            books = results.fetchall()
            bookList = [];
            for book in books:
                try:
                    id = book[1]
                    title = book[2]  
                    pageCount = book[3] 
                    author = book[4]
                    publisher = book[5]
                    publishedDate = book[6]
                    description = book[7]
                    category = book[8]
                    smallThumbnail = book[9]
                    thumbnail = book[10]
                    price = book[11]
                    bookList.append(Book(id, title, author, publisher, publishedDate,description, category,smallThumbnail,thumbnail, price, pageCount))
                except Exception as e:
                    print(e)                        
            return bookList
        except Exception as e:
            print(e)


    def get_book(self,bookId):
        try:
            cursor = self.__conn.cursor()
            results = cursor.execute("select * from book where bookId = '" + bookId + "'")
            book = results.fetchone()

            try:
                id = book[1]
                title = book[2]  
                pageCount = book[3] 
                author = book[4]
                publisher = book[5]
                publishedDate = book[6]
                description = book[7]
                category = book[8]
                smallThumbnail = book[9]
                thumbnail = book[10]
                price = book[11]

                return Book(id, title, author, publisher, publishedDate,description, category,smallThumbnail,thumbnail, price, pageCount)
            except Exception as e:
                print(e)

        except Exception as e:
            print(e)
