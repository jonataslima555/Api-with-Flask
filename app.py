from flask import Flask, jsonify, request
from models import User, Books, db
from peewee import IntegrityError
app = Flask(__name__)


@app.route('/create_users', methods=['POST'])
def create_users():
    data = request.get_json()

    name = data.get('name')
    password = data.get('password')

    if not name or not password:
        return jsonify({'error': 'name and password are required'}), 400

    try:
        new_user = User.create_user(name=name, password=password)
        return jsonify({
            'message': 'User created successfully',
            'user': {
                'id': new_user.id,
                'name': new_user.name
            }
        }), 201

    except IntegrityError as e:
        return jsonify({'error': 'User already exists or IntegrityError'}), 400





@app.route('/create_books', methods=['POST'])
def create_books():
    data = request.get_json()

    user_id = data.get('user_id')
    book_name = data.get('book_name')

    if not user_id or not book_name:
        return jsonify({'error': 'user_id and book_name are required'}), 400
    
    try:

        user = User.get(User.id == user_id)

        new_book = Books.create_book(user=user, name=book_name)

        return jsonify({
            'message': 'Book created successfully',
            'book': {
                'id': new_book.id,
                'name': new_book.name,
                'user': {
                    'id': user.id,
                    'name': user.name
                }
            }
        }), 201
    
    except User.DoesNotExist:
        return jsonify({'error': 'User not found'}), 404
    except IntegrityError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/books', methods=['GET'])
def get_all_books():

    books = Books.select()

    books_list = [{
        'id': book.id,
        'name': book.name,
        'user': {
            'id': book.user.id,
            'name': book.user.name
        }
    } for book in books]

    return jsonify(books_list)


@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    try:
        book = Books.get(Books.id == id)

        return jsonify({
            'id': book.id,
            'name': book.name,
            'user': {
                'id': book.user.id,
                'name': book.user.name
            }
        })
    except Books.DoesNotExist:

        return jsonify({'error': 'Book not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)