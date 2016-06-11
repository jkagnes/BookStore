import requests, FlaskBookstore

from FlaskBookstore.models.book import Book



class BookRepository(object):

    def __init__(self):
        self.serviceBaseURL = "https://www.googleapis.com/books/v1/volumes?key=AIzaSyBMLo8kvt6jeLIzUFbZPEueZ7ZJqefYehY"
   
    def get_books_new(self):
        serviceURL = self.serviceBaseURL + "&q=subject:fiction&orderBy=newest&maxResults=25&printType=books&filter=paid-ebooks"
        results = requests.get(serviceURL)
        books = results.json()
        bookList = []
        for book in books["items"]:
            try:
                id = book["id"]
                title = book["volumeInfo"]["title"]  
                pageCount = book["volumeInfo"]["pageCount"]  
                author = book["volumeInfo"]["authors"][0]
                publisher = book["volumeInfo"]["publisher"]
                publishedDate = book["volumeInfo"]["publishedDate"]
                description = book["volumeInfo"]["description"]
                category = book["volumeInfo"]["categories"][0]
                smallThumbnail = book["volumeInfo"]["imageLinks"]["smallThumbnail"]
                thumbnail = book["volumeInfo"]["imageLinks"]["thumbnail"]
                price = book["saleInfo"]["retailPrice"]["currencyCode"] + " " + str(book["saleInfo"]["retailPrice"]["amount"])
                bookList.append(Book(id, title, author, publisher, publishedDate,description, category,smallThumbnail,thumbnail, price, pageCount))
            except Exception as e:
                print(e)

        return bookList


    def get_books(self,category):
        serviceURL = self.serviceBaseURL + "&q=subject:" + category + "&maxResults=25&printType=books&filter=paid-ebooks"
        results = requests.get(serviceURL)
        books = results.json()
        bookList = [];
        for book in books["items"]:
            try:
                id = book["id"]
                title = book["volumeInfo"]["title"]  
                pageCount = book["volumeInfo"]["pageCount"] 
                author = book["volumeInfo"]["authors"][0]
                publisher = book["volumeInfo"]["publisher"]
                publishedDate = book["volumeInfo"]["publishedDate"]
                description = book["volumeInfo"]["description"]
                category = book["volumeInfo"]["categories"][0]
                smallThumbnail = book["volumeInfo"]["imageLinks"]["smallThumbnail"]
                thumbnail = book["volumeInfo"]["imageLinks"]["thumbnail"]
                price = book["saleInfo"]["retailPrice"]["currencyCode"] + " " + str(book["saleInfo"]["retailPrice"]["amount"])
                bookList.append(Book(id, title, author, publisher, publishedDate,description, category,smallThumbnail,thumbnail, price, pageCount))
            except Exception as e:
                print(e)
                        
        return bookList


    def get_book(self,bookId):
        serviceURL = "https://www.googleapis.com/books/v1/volumes/" + bookId + "?key=AIzaSyBMLo8kvt6jeLIzUFbZPEueZ7ZJqefYehY"
        results = requests.get(serviceURL)
        book = results.json()
        
        try:
            id = book["id"]
            title = book["volumeInfo"]["title"]  
            pageCount = book["volumeInfo"]["pageCount"]    
            author = book["volumeInfo"]["authors"][0]
            publisher = book["volumeInfo"]["publisher"]
            publishedDate = book["volumeInfo"]["publishedDate"]
            description = book["volumeInfo"]["description"]
            category = book["volumeInfo"]["categories"][0]
            smallThumbnail = book["volumeInfo"]["imageLinks"]["smallThumbnail"]
            thumbnail = book["volumeInfo"]["imageLinks"]["thumbnail"]
            price = book["saleInfo"]["retailPrice"]["amount"]
           
            return Book(id, title, author, publisher, publishedDate,description, category,smallThumbnail,thumbnail, price, pageCount)
        except Exception as e:
            print(e)

        