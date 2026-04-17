from flask import Flask, request, make_response
from models import *
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from pathlib import Path

from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import bcrypt

#define the path to the env path starting from where app.py is
env_path = Path(__file__).resolve().parent.parent / ".env"

# Load all variables from .env
load_dotenv(dotenv_path=env_path)  

app = Flask(__name__)

#db configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///entries.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# jwt configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_TOKEN_LOCATION'] = ['headers']

#initialize db's connection to the app
db.init_app(app=app)

#JWT initialization
jwt = JWTManager(app)

migrate = Migrate(app, db)

#READ => get the resource on the root route
@app.route("/", methods=["GET"])
def index():
    return {"msg": "welcome to the journal entries platform"}

#READ => get the entries resource with pagination
#  GET /entries is a protected endpoint and requires verification of user identity
@jwt_required()
@app.route("/entries", methods=["GET"])
def get_journal_entries():

    # Extract the user ID from the JWT
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    #THE FOLLOWING HAPPENS WHEN THE USER'S ID IN JWT TOKEN IS NOT ACCEPTED
    if not user:
        return make_response({'error': '401 Unauthorized'}, 401)
    
    #THE FOLLOWING HAPPENS WHEN THE USER'S ID IN JWT TOKEN IS ACCEPTED
    
    #Define page and per page request parameters for the /entries endpoint
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    #query the db and paginate with paginate()
    pagination = JournalEntry.query.paginate(page=page, per_page=per_page, error_out=False)

    entries = pagination.items
    
    #Return a response
    #Returns pagination metadata=> page number, number of entries per page, entries etc.
    return make_response({
        "page": pagination.page,
        "per_page": pagination.per_page,
        "items": [JournalEntrySchema().dump(e) for e in entries]
    }, 200)


#CREATE => create entry resource
@app.route("/entries", methods=["POST"])
def create_journal_entries():
    
    try:
        #Deserializing incoming data
        incoming_data = JournalEntrySchema().load(request.get_json())

        db.session.add_all(incoming_data)
        db.session.commit()

        #Serializing => return serialized response to the client
        incoming_data_dict = JournalEntrySchema().dump(request.get_json())
        return make_response(incoming_data_dict,201)

    #Raise an error when trying to deserialize incoming data
    except ValidationError as err:
         return make_response({"error": f"could not load the data {err}"}, 404)

#UPDATE => update an entry resource
# PATCH /entries is a protected endpoint and requires verification of user identity
@jwt_required()
@app.route("/entries/<id>", methods=["PATCH"])
def update_journal_entries(id):

    # Extract the user ID from the JWT
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    #THE FOLLOWING HAPPENS WHEN THE USER'S ID IN JWT TOKEN IS NOT ACCEPTED
    if not user:
        return make_response({'error': '401 Unauthorized'}, 401)
    
    #THE FOLLOWING HAPPENS WHEN THE USER'S ID IN JWT TOKEN IS ACCEPTED

    try:
        #Deserializing incoming data
        incoming_data = JournalEntrySchema().load(request.get_json(), many=False)

        #get the entry in the db by id
        entry = JournalEntry.query.filter_by(id = id).first()

        #Check if entry does not exist in the db
        if not entry:
          return make_response({"error": f"entry of {id} not found in the database"},404)  

        #Update entry field if entry does not exists in the db
        entry.title = incoming_data["title"]
        entry.content = incoming_data["content"]

        db.session.commit()

        return make_response({"msg": f"data updated successfully"},200)
    
    #Raise an error when trying to update data in the db
    except Exception as e:
        return make_response({"error": f"could not update the data {e}"},404)



@app.route("/entries/<id>", methods=["DELETE"])
def delete_journal_entries(id):

    # Extract the user ID from the JWT
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    #THE FOLLOWING HAPPENS WHEN THE USER'S ID IN JWT TOKEN IS NOT ACCEPTED
    if not user:
        return make_response({'error': '401 Unauthorized'}, 401)
    
    #THE FOLLOWING HAPPENS WHEN THE USER'S ID IN JWT TOKEN IS ACCEPTED
    try:
        #get the entry in the db by id
        entry = JournalEntry.query.filter_by(id = id).first()

        #Check if entry does not exist in the db
        if not entry:
          return make_response({"error": f"entry of {id} not found in the database"},404)  

        #delete entry record if the entry exists in the db
        db.session.delete(id)
        db.session.commit()

        return make_response({"msg": f"data deleted successfully"},200)

    #Raise an error when trying to update data in the db
    except Exception as e:
        return make_response({"error": f"could not update the data {e}"},404)
    

#Implement authentication for a user using username and password
@app.route('/login', methods=['POST'])
def login():

    #Deserializing incoming data
    incoming_data = UserSchema().load(request.get_json(), many=False)

    print('Received data:', incoming_data['username'] , incoming_data['password'])

    #get the entry in the db by id
    user = User.query.filter_by(username=incoming_data['username']).first()

    #check if the user exists in the db when trying to log in
    # compare the hash password provided by the user and hash password stored in the db
    if user and bcrypt.check_password_hash(user.password, incoming_data['password']):

        access_token = create_access_token(identity=user.id)
        return make_response({'message': 'Login Success', 'access_token': access_token})
    else:
        return make_response({'message': 'Login Failed'}, 401)


