# Imports
#from server_test.common.auth import SECRET_KEY
from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api, abort, request
#from common.auth import token_requered
from functools import wraps
import jwt, datetime
import hmac, hashlib, time

#SECRET = 'Sh!! No se lo cuentes a nadie'


# Auth by Tokens
def token_requered(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-token') # get tokken by header
        #token = request.args.get("token")

        # There is not token
        if not token:
            return make_response(jsonify({'message': 'Token is missing!'}), 403)

        # Try to decode the token, it will raise error if it's incorrect
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
        except:
            return make_response(jsonify({'message': 'Token is invalid!'}), 403)

        return f(*args, **kwargs)

    return decorated

# Auth by HMAC
'''
def auth_required(func):
    def wrapper(self):
        try:
            hash_api = request.headers.get('X-HASH') # Get the headers
            hash_client = hmac.new(key=SECRET.encode(), digestmod=hashlib.sha1) # Set the hash algorithm
            hash_client.update(request.headers.get('X-UID').encode()) # Set the UID
            hash_client.update(request.headers.get('X-TIMESTAMP').encode()) # Set the TIMESTAMP (UNIX)
        
            # If hashes are the same, then give access to the function
            if hash_api == hash_client.hexdigest():
                return func(self)

        # An error occured trying to resolve the values necesarry for the hash
        except:
            return make_response('Please authenticate by HMAC on X headers!', 401, {'WWW-Autencticate': 'Basic reaml="Login Required"'})
        
        # Hashes are not a mach, return an error
        return make_response('Could not verify your login!', 401, {'WWW-Autencticate': 'Basic reaml="Login Required"'})

    return wrapper
'''

# Autentificación vía HTML
""" 
def auth_required(func):
    def wrapper(self):
        # print(request.authorization)

        # If the authentification is correct, then return the function that it wraps
        # If not, then return an error
        if request.authorization and request.authorization['username'] == 'carlos' and request.authorization['password'] == '1234':
            return func(self)
        return make_response('Could not verify your login!', 401, {'WWW-Autencticate': 'Basic reaml="Login Required"'})
    return wrapper
 """

# Create app and api
app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = "TopSecret"

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
    @token_requered
    def get(self):
        return jsonify({'data': BOOKS}) # Returns as json in data variables

    # Metodo para agregar nuevo libro
    @token_requered
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
    @token_requered
    def get(self, book_id):
            abort_if_book_doesnt_exits(book_id)
            return make_response( jsonify(BOOKS[book_id]), 200 ) # Returns a response as json with some info code
    
    @token_requered
    def put(self, book_id):
        # Getting the request as json format
        json = request.get_json(force=True)

        # If the id donesn't exist, then quit
        abort_if_book_doesnt_exits(book_id)

        # Replace the information of the book
        BOOKS.update( {'{}'.format(book_id): json} )

        # Return the whole collection
        return jsonify(BOOKS)

    @token_requered
    def delete(self, book_id):
        abort_if_book_doesnt_exits(book_id)
        del BOOKS[book_id]
        return jsonify(BOOKS)
        # return jsonify({'message':'successful delete'})

@app.route('/login')
def login():
    auth = request.authorization #username and password

    # Check the password for now
    if auth and auth.password == '1234':
        # Set the token, by username with expiration time and with the secret key
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        # Return the token to the client
        return jsonify({'token': token})

    # Error at verification
    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Requiered"'})

class Authors(Resource):
    pass

class Generes(Resource):
    pass

class Root(Resource):
    def get(self, resource_type):
        allowed_resource_types = [
            "books",
            "authors",
            "genres"
        ]
        if resource_type not in allowed_resource_types:
            abort(400, message="Error 404")

# Add resources as REST arquitecture
api.add_resource(BookList, '/books')
api.add_resource(Book, '/books/<book_id>') #<> means it's a variable
api.add_resource(Authors, '/authors')
api.add_resource(Generes, '/generes')
api.add_resource(Root, '/<resource_type>')


if __name__ == '__main__':
    app.run(debug=True)
