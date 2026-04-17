from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from marshmallow import Schema, fields, ValidationError, post_load, validates, validates_schema, validate
from pprint import pprint

#create metadata instance to provide naming conventions for constraints
metadata = MetaData(naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})

#db initialization
db = SQLAlchemy(metadata=metadata)

#Create user model for db constraints and validation
class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    #create a relationship to implement => Get a all journal entries related to a user 
    # => user.journal_entries
    
    journal_entries = db.relationship(
        'JournalEntry',
        back_populates = 'user', 
        cascade = 'all,delete-orphan'
    )

    #Format the object instance with __repr__ method
    def __repr__(self):
        return f'<User {self.username}>'
    
#create a user schema for validating user details during deserialization 
class UserSchema(Schema):

    id = fields.Integer()
    username = fields.String(validate= validate.Range(3,80),required=True)
    password = fields.String(validate= validate.Range(8,), required=True)


#Create user model for db constraints and validation
class JournalEntry(db.Model):

    __tablename__ = "journal_entries"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True, nullable=False)
    content = db.Column(db.String(50), nullable=False)

    #user_id is the foreign key referencing the id field in the users table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    #create a relationship to implement => Get a user related to a journal entry 
    # => journal_entry.user
    user = db.relationship(
        'User', 
        back_populates = 'journal_entries'
    )

    #Format the object instance with __repr__ method
    def __repr__(self):
        return f'<User {self.title}, {self.content}>'

#create journal entries schema for validating user details during deserialization 
class JournalEntrySchema(Schema):

    id = fields.Integer()
    title = fields.String(required=True)
    content = fields.String(required=True)

    #Use @validates_schema to validate the incoming title and content fields
    # checks if there is an entry already existing in the db
    @validates_schema
    def check_entry_duplicates(self,data, **kwargs):
        
        existing = JournalEntry.query.filter_by(
            title= data["title"],
            content= data["content"]
        ).first()

        if existing:
            raise ValidationError(
                "Journal entry already exists"
        )

    #Use @post_load to set the data into an object after passing validation
    @post_load
    def make_entry(self, data, **kwargs):
        return JournalEntry(**data)




