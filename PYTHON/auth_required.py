from flask_restful import  Resource
class BookList(Resource):
    @auth_required
    def get(self):
        return jsonify({'data': BOOKS})
