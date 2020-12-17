from flask import Flask, jsonify, session, g
from flask_cors import CORS
from flask_login import LoginManager ############# added this line


DEBUG = True
PORT = 8000
import models
from resources.books import book # adding this line
from resources.users import user # adding this line
# Initialize an instance of the Flask class.
login_manager = LoginManager() # sets up the ability to set up the session


# This starts the website!
app = Flask(__name__)

app.secret_key = "LJAKLJLKJJLJKLSDJLKJASD" ## Need this to encode the session
login_manager.init_app(app) # set up the sessions on the app


@login_manager.user_loader # decorator function, that will load the user object whenever we access the session, we can get the user
# by importing current_user from the flask_login
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None
###################### added these lines


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

##http://localhost:8000/api/mybooks/user/1 
CORS(book, origins=['http://localhost:3000'], supports_credentials=True) # adding this line
app.register_blueprint(book, url_prefix='/api/books') # adding this line
app.register_blueprint(book, url_prefix='/api/mybooks') # adding this line

CORS(user, origins=['http://localhost:3000'], supports_credentials=True) # adding this line
app.register_blueprint(user, url_prefix='/api') # adding this line

# The default URL ends in / ("mybookshelf.com/").
@app.route('/')
def index():
    return 'Welcome to My Bookshelf'

@app.route('/json')
def user():
    return jsonify(username="vdighe", email='vdighe@gmail.com', fullname='Vaishali Dighe-Phanse')    


@app.route('/api/profile', methods=['GET'])
def getProfile():
    user_id = session.get('user_id')

    if user_id:
        user = User.query.filter_by(id=user_id).first()
        return jsonify({'userId': user_id,
                        })

    return jsonify({'userId': '',  'fullName': '', 'location': ''})


# Run the app when the program starts!
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
