# ////////////////////////////////////////////////////////
# USERS CONTROLLER
# ////////////////////////////////////////////////////////

from flask_app import app
from flask import render_template, session, redirect, request
from flask_app.models import login_model

# //// SHOW /////////////////////////////////////

@app.route('/')                                                         # Main Page
def root():
    print("******** in index *******************")
    if 'lu_id' in session:                                              # check if user is logged in
        print("User is logged in, rerouting to dashboard")
        return redirect("/dashboard")
    return render_template("index.html")

@app.route('/logout')                                                   # Logout User
def logout():
    del session['lu_id']
    return redirect("/")

# //// FORM POST /////////////////////////////////

@app.route('/registration/post', methods=['POST'])                      # Function that handles regisstration form data
def registration_post():
    print("**** In Registration POST ****")
    data = {
        **request.form
    }
    if not login_model.LoginUsers.validate_login_user_create_data(data):    # If a login field is invalid, redirect to root
        return redirect('/')
    
    # **** Start hashing the password ********
    pw_hash = login_model.LoginUsers.generate_password_hash(data['password'])
    data['password']=pw_hash                                            # Save the hashed password to data

    login_model.LoginUsers.create(data)                                 # Create User in the Login Database

    return redirect("/registration")

@app.route('/login/post', methods=['POST'])                             # Function that handles log in form data
def login_post():
    print("**** In Login POST ****")
    data = {
        **request.form
    }
    print(data)
    if not login_model.LoginUsers.validate_login_user_login_data(data): # Check if login data is valid
        return redirect("/")                                            # If login is invalid, redirect to root with flash errors
    else:                                                               # Else login the user
        user = login_model.LoginUsers.get_one_by_email(data)            # Retrieve user using email
        print(user.first_name,user.last_name,user.email)
        session['lu_id'] = user.id                                      # Set Login User ID to user id

    return redirect("/dashboard")

# //// CREATE ////////////////////////////////////

@app.route('/registration')                                             # This routh shows a sucessful registration
def registration():
    print("**** In registration Creat Login User ****")
    return render_template("registration_success.html")

# @app.route('/post', methods=['POST'])                         # Retrieve the input values from create form
# def post():
#     print("**** In / Post Retrieval **************")
#     data = {                                                            # Create Data Dictionary from values in form
#         'name': request.form['name'],
#         'email': request.form['email'],
#         'location': request.form['location'],
#         'fav_language': request.form['fav_language'],
#         'comment' : request.form['comment']
#     }
#     print(data)

#     if not users_model.Users.validate_user_create_data(data):
#         return redirect("/")

#     id = users_model.Users.create(data)                                 # Insert User in to database
#     data['id'] = id                                                     # Memorize ID of created User

#     user = users_model.Users.get_one(data)                              # get an instance of the created user
#     ("Newly created user instance: ", user)

#     print("**** Retrieving All Users *******************")
#     all_users = users_model.Users.get_all()                             # Get all instances of users from the database
#     return render_template("user_show.html", user = user, all_users = all_users)

# //// RETRIEVE ////////////////////////////////////

@app.route('/dashboard')                                                    # DASHBOARD
def Dashboard():
    print("******** in dashboard *******************")
    if not 'lu_id' in session:                                              # Check if user is logged in
        print("User is not logged in, redirect to root login")
        return redirect("/")                                                # If not logged in, redirect to root login
    data = {
        'id': session['lu_id']
    }
    print("data:")
    print(data)
    user = login_model.LoginUsers.get_one(data)                             # Retrive user's info from db and make a user instance
    print("User:")
    print(user)
    return render_template("dashboard.html", user=user)                     # Pass user's info to the Dashboard

# @app.route('/users/')
# @app.route('/users')                                                    # Read All Users Page
# def users():
#     print("**** Retrieving Users *******************")
#     all_users = users_class.Users.get_all()                             # Get all instances of users from the database
#     return render_template("read_all.html", all_users = all_users)

# @app.route('/users/<int:id>')                                           # Retrive the data from one specified user
# def users_id (id):
#     print ("*********** In users id ******************")
#     data = {
#         'id': id
#     }
#     user = users_class.Users.get_one(data)
#     return render_template("users_read_one.html", user=user)

# //// UPDATE ////////////////////////////////////

# @app.route('/users/<int:id>/update/post', methods=['POST'])             # Update a specified user's information
# def users_id_update_post(id):
#     print ("*********** In Users ID Edit POST *****************")
#     data = {                                                            # retrieve the data from the form
#         'id': id,
#         'first_name': request.form['first_name'],
#         'last_name': request.form['last_name'],
#         'email': request.form['email']
#     }
#     users_class.Users.update_one(data)
#     return redirect('/users')

# //// DELETE ////////////////////////////////////

# @app.route('/<int:id>/delete')                                    # Delete a specified user
# def users_id_delete(id):
#     print("******** IN DELETE ********************")
#     data = {
#         'id': id
#     }
#     users_model.Users.delete(data)
#     return redirect('/users')

# //// 404 CATCH //////////////////////////////////

# **** Ensure that if the user types in any route other than the ones specified, 
#           they receive an error message saying "Sorry! No response. Try again ****
@app.errorhandler(404) 
def invalid_route(e): 
    return "Sorry! No response. Try again."