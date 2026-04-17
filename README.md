# Notes App Project

This is a python Flask-based backend application that demonstrates a one-to-many relationship between a user and a journal entry. A user can be linked to multiple journal entries and a single journal entry belongs to a single user. 

Authentication of a user has also been implemented using JSON Web Token(JWT); and Notes app API data is validated at both the database level and schema level to enable valid data stored in the database and correct serialization and deserialization respectively.

The following are ways you can interact with the Notes Application Backend API which is implemented by an SQLITE engine. Some of the endpoints are protected by JWT.

- **Retrieving all entries from the database(Protected endpoint)**
All entries can be retrieved from the database and paginated(To determine the number of entries to return on a particular page)

```bash
GET /entries?page=<int>&per_page=<int> #get all entries
```

- **Create a particular entry in the database**. 
```bash
entry_payload = {

    "title": <String>
    "content": <Text>
}
```

```bash
POST /entries/{id}
```

- **Update a particular entry in the database(Protected endpoint)**. Specify the **id** of the entry item you want to delete from the database.
```bash
DELETE /entries/{id} 
```

- **Delete a particular entry in the database(Protected endpoint)**. Specify the **id** of the entry item you want to delete from the database.
```bash
DELETE /entries/{id} 
```
- **Authenticate a particular user by logging in**. Specify the username and password of the user as the payload. Logging in implements password hashing with **bcrypt** for security purposes.

```bash
DELETE /login
```
```bash
user_payload = {

    "username": <String>
    "password": <String>
}
```

## Prerequisites
Ensure you have installed Python in your machine:

```bash
python --version
```

**Optional**:Create and activate the Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate   # Windows
```

Fork [this repository](git@github.com:joshua-odero/flask-c10-summative-lab-sessions-and-jwt-clients.git) , then clone it to your preferred destination with the following command:

```bash
git clone <your SSH/Http path>
```

## Installing dependencies
Switch to the app directory using the **cd** command, Use the **pip** to install the core project dependencies from pypi like :
- **Flask** which is the main framework for the web app development in python
- **Flask-Migrate** for database version control without losing crucial data
- **marshmallow** which adds a layer of data integrity to the database by validating incoming data and data from the Flask application
- **flask_jwt_extended** to manage authentication flow of the user
- **flask_bcrypt** to manage hashing and storing of user passwords
- **python-dotenv** to secure secret keys in .env file

```bash
cd flask-c10-summative-lab-sessions-and-jwt-clients
```

```bash
pip install <package_name>
```
or 

[Use the packages in the Pipfile](./Pipfile) to install all packages in the virtual environment:
```bash
pipenv install
```


## Running the project
Inside the project directory, and depending on where the .pyfile is located, execute the following command to run a .py script . Use **python** or **python3** commands depending on your OS:

```bash
python3 <example_file.py> #OR python3 <example_file.py>
```

### STEP 1: Run the Flask application
**NOTE:** **Run the Flask app first** to test your frontend application interaction with the application's API:

```bash
python app.py #python3 app.py
```

### STEP 2: Set up the database and create tables
To set up the database to run locally, run:

```bash
flask db init
```
Upgrade to migrate to the the latest version of the database:

```bash
flask db upgrade head
```

### STEP 3: Populate the database
Run [seed.py](./server/seed.py) on your terminal to populate sample data and use it to test the API's data:

```bash
python seed.py #python3 seed.py
```
