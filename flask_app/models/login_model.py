# import the function that will return an instance of a connection ////////
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re                                                               # Import REGEX

TARGETDATABASE = 'dojo_survey_db'                                       # Designates the database we are using
TABLENAME = "users"                                                     # Designates the table we are using
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')      # Pattern for email validatiom

# //// USERS CLASS ////////////////////////////////////////////////////////
class LoginUsers:
    def __init__( self , data ):                                        # Constructor function
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # //// FLASH ///////////////////////////////////////////////////////////

    @staticmethod
    def validate_login_user_create_data(data:dict):
        is_valid = True
        # //// Validate User First Name ///////
        if len(data['first_name']) < 2:
            flash("First Name must be at least 2 characters in length","error_login_user_first_name")
            is_valid = False
        elif not data['first_name'].isalpha():
            flash("First Name must be letters only","error_login_user_first_name")
            is_valid = False

        # //// Validate User Last Name ////////
        if len(data['last_name']) < 2:
            flash("Last Name must be at least 2 characters in length","error_login_user_last_name")
            is_valid = False
        elif not data['last_name'].isalpha():
            flash("Last Name must be letters only","error_login_user_last_name")
            is_valid = False

        # //// Validate User Email ////////
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address", "error_login_user_email")
            is_valid = False
        elif LoginUsers.get_one_by_email(data):
            flash("Invalid email already registered", "error_login_user_email")
            is_valid = False
        
        # //// Validate Password ////////
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters in length", "error_login_user_password")
            is_valid = False
        
        # //// Validate Confirm Password ////////
        if data['password'] != data['confirm_password']:
            flash("Password and Confirm Password do not match", "error_login_user_confirm_password")
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

    # **** Get One by Email Class Method **********************************
    # @Returns: an instance of the class
    @classmethod
    def get_one_by_email(cls, data:dict):
        query = "SELECT * FROM " + TABLENAME +" WHERE email = %(email)s;"
        results = connectToMySQL(TARGETDATABASE).query_db(query, data)  # Call the connectToMySQL function with the target db
                                                                        # result is a list of a single dictionary
        if len(results) == 0:
            return False
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