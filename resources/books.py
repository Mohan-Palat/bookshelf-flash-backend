import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict


# first argument is blueprints name
# second argument is it's import_name
book = Blueprint('books', 'book')

@book.route('/user/<id>', methods=['GET'])
def getBooksByUser(id):
    ## find All the Books Belonging to the userud
    #user_id = session.get('user_id')

    try:
        books = [model_to_dict(book) for book in models.Book.select().where(models.Book.user == id)]
        return jsonify(data=books, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@book.route('/', methods=['GET'])
def getBooks():
    ## find All the Books
    #user_id = session.get('user_id')
    #print(user_id)
    try:
        books = [model_to_dict(book) for book in models.Book.select()]
        print(books)
        return jsonify(data=books, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@book.route('/<id>', methods=["GET"])
#@login_required
def getBook(id):
    print(id, 'reserved word?')
   
    book = models.Book.get_by_id(id)
    print(book.__dict__)
    return jsonify(data=model_to_dict(book), status={"code": 200, "message": "Success"})


#Delete Route
@book.route('/<id>', methods=["Delete"])
def deleteBook(id):
    query = models.Book.delete().where(models.book.id==id)
    query.execute()
    return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})    

#Update Route
@book.route('/<id>', methods=["PUT"])
def updateBook(id):
    payload = request.get_json()
    query = models.Book.update(**payload).where(models.Book.id==id)
    query.execute()
    return jsonify(data=model_to_dict(models.Book.get_by_id(id)), status={"code": 200, "message": "resource updated successfully"})


#Create ROUTE
@book.route('/', methods=["POST"])
def postBook():
    ## see request payload anagolous to req.body in express
    payload = request.get_json()
    print(type(payload), 'payload')
    book = models.Book.create(**payload)
    ## see the object
    print(book.__dict__)
    ## Look at all the methods
    print(dir(book))
    # Change the model to a dict
    print(model_to_dict(book), 'model to dict')
    book_dict = model_to_dict(book)
    return jsonify(data=book_dict, status={"code": 201, "message": "Success"})        
