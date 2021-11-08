# import the function that will return an instance of a connection ////////
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

TARGETDATABASE = 'dojo_survey_db'                                               # Designates the database we are using
TABLENAME = "users"                                                             # Designates the table we are using
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')      # Pattern for email validatiom

# //// USERS CLASS ////////////////////////////////////////////////////////
class Users:
    def __init__( self , data ):                                        # Constructor function
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.location = data['location']
        self.fav_language = data['fav_language']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # //// FLASH ///////////////////////////////////////////////////////////

    @staticmethod
    def validate_user_create_data(data:dict):
        is_valid = True
        # //// Validate User Name ///////
        if len(data['name']) < 3:
            flash("Name must be at least 3 characters in length","error_user_name")
            is_valid = False
        # //// Validate User Email ////////
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address", "error_user_email")
            is_valid = False
        # //// Validate User Comments
        if len( data['comment'] ) < 3:
            flash("Comment must ve at least 3 characters in length","error_user_comment")
            is_valid = False
        elif len( data['comment'] ) > 255:
            flash("Comment must be < 255 characters in length", "error_user_comment")
            is_valid = False
        return is_valid

    # //// CREATE //////////////////////////////////////////////////////////

    # **** Insert One Method ***********************************************
    # @returns ID of created user
    @classmethod
    def create(cls, data ):
        query = "INSERT INTO " + TABLENAME +" ( name, email, location , fav_language , comment) VALUES ( %(name)s ,%(email)s, %(location)s , %(fav_language)s, %(comment)s );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(TARGETDATABASE).query_db( query, data )
        
    # //// RETRIEVE /////////////////////////////////////////////////////////

    # **** Get All Class Method *******************************************
    # @Returns: a list of instances of the class
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM " + TABLENAME + ";"
        results = connectToMySQL(TARGETDATABASE).query_db(query)        # Call the connectToMySQL function with the target db
        list_of_instances = []                                          # Initialize an empty list where we can store instances of the class
        for class_instance in results:                                  # Iterate over the db results and create instances of the cls objects
            list_of_instances.append( cls(class_instance) )             # Add each instance of the class to the list of instances
        return list_of_instances
    
    # **** Get One Class Method *******************************************
    # @Returns: an instance of the class
    @classmethod
    def get_one(cls, data:dict):
        query = "SELECT * FROM " + TABLENAME +" WHERE id = %(id)s;"
        results = connectToMySQL(TARGETDATABASE).query_db(query, data)  # Call the connectToMySQL function with the target db
                                                                        # result is a list of a single dictionary
        return cls(results[0])                                          # return an instance of the dictionary

    # //// UPDATE //////////////////////////////////////////////////////////

    # **** Update One Class Method *****************************************
    # @Returns: Nothing
    @classmethod
    def update_one(cls, data:dict):
        query = "UPDATE " + TABLENAME +" SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s WHERE id=%(id)s"
        return connectToMySQL(TARGETDATABASE).query_db(query, data)

    # //// DELETE //////////////////////////////////////////////////////////

    # **** Delete One Class Method *****************************************
    # @Returns: Nothing
    @classmethod
    def delete(cls, data:dict):
        query = "DELETE FROM " + TABLENAME + " WHERE id=%(id)s"
        return connectToMySQL(TARGETDATABASE).query_db(query, data)