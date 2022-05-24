# Imports
from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api, abort, request

# Create app and api
app = Flask(__name__)
api = Api(app)

# Data base
BOOKS = {
    '1': {
        'isbn': '744586',
        'title': 'Cien años de soledad',
        'description': 'Lorem insup lol.',
        'autor': 'Gabriel Garcia Marquez'
    },
    '2': {
        'isbn': '7894546',
        'title': 'De animales a dioses',
        'description': 'Lorem insup lol.',
        'autor': 'Yuval Noah Harari'
    }
}

# Aborts the request and returns an error
def abort_if_book_doesnt_exits(book_id):
    if book_id not in BOOKS:
        abort(404, message='El libro con id {} no existe'.format(book_id))

# Returns the whole book list
class BookList(Resource):
    def get(self):
        return jsonify({'data': BOOKS}) # Returns as json in data variables

    # Metodo para agregar nuevo libro
    def post(self):
        # Getting the request as json format
        json = request.get_json(force=True)

        # Index to post the new book
        index = len(BOOKS) + 1

        # Putting the new book in the database
        BOOKS.update( {'{}'.format(index): json } )

        # Returining the ID to the user
        return 'Libro agregado correctamente con ID: ' + str(index)

# Returns an especific id book
class Book(Resource):
    def get(self, book_id):
            abort_if_book_doesnt_exits(book_id)
            return make_response( jsonify(BOOKS[book_id]), 200 ) # Returns a response as json with some info code

    def put(self, book_id):
        # Getting the request as json format
        json = request.get_json(force=True)

        # If the id donesn't exist, then quit
        abort_if_book_doesnt_exits(book_id)

        # Replace the information of the book
        BOOKS.update( {'{}'.format(book_id): json} )

        # Return the whole collection
        return jsonify(BOOKS)

class Authors(Resource):
    pass

class Generes(Resource):
    pass

# Add resources as REST arquitecture
api.add_resource(BookList, '/books')
api.add_resource(Book, '/books/<book_id>') #<> means it's a variable
api.add_resource(Authors, '/authors')
api.add_resource(Generes, '/generes')

if __name__ == '__main__':
    app.run(debug=True)
