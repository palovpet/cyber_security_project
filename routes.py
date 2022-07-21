
from flask import render_template, request, redirect
from app import app
import users
import things

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        return render_template("error.html", message="Wrong username or password")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("signin.html")
    if request.method == "POST":

# Flaw 1 fix (add)
#         users.check_csfr()

        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Passwords must match")
        if not users.signin(username, password1):
            return render_template("error.html", message="Username already in use or other error")
        users.login(username, password1)
        return redirect("/")        


@app.route("/allmythings/<name>")
def all_my_things(name):

# Flaw 3 fix (add)    
#     if not users.user_accessing_own_info(name):
#         return render_template("error.html", message="Buuu you are trying to hack into someone elses stuff")

    return render_template("allmythings.html", mythings=things.view_things(users.get_id_with_name(name)))

@app.route("/mythings", methods=["POST", "GET"])
def mythings():
    if request.method == "POST":

# Flaw 1 fix (add)
#         users.check_csfr()

        thing = request.form["thing"]
        if thing == "":
            return render_template("error.html", message="Can't be empty")
        if not things.add_new(thing):
            return render_template("error.html", message="Adding a new thing didn't work, try again")
        return redirect("/")    
    if request.method == "GET":
        return render_template("mythings.html", mythings=things.view_top3(users.user_id()), name=users.get_name(), result_found=False, emptyresult="")

@app.route("/searchmythings", methods=["POST"])
def search_my_things():

# Flaw 1 fix (add)
#         users.check_csfr()

    search_criteria = request.form["thing"]
    if search_criteria == "":
        return render_template("error.html", message="Can't be empty")
    search_result = things.search_things(search_criteria) 
    result_found = True
    emptyresult = ""
    if search_result == "No search results":
        result_found = False
        emptyresult = "This hasn't pissed you off yet! Maybe go and add it to list?"   
    return render_template("mythings.html", mythings=things.view_top3(users.user_id()), name=users.get_name(), result_found=result_found, search=things.search_things(search_criteria), emptyresult=emptyresult)            

@app.route("/admin", methods=["GET"])
def adminview():
    return render_template("admin.html", admin=users.is_admin(), everyonesthings=things.get_everyones_things())
