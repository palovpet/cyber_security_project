import secrets
from flask import session, abort, request
# Flaw 4 fix (add): from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def login(username, password):
    sql = "SELECT id, password FROM endusers WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    print(user.password)
    print(user.password == password)

# Flaw 4 fix (replace previous if not)
#      if not check_password_hash(user.password, password):
#         return False

    session["user_id"] = user[0]
    session["user_name"] = username

# Flaw 1 fix (add)
#     session["csrf_token"] = secrets.token_hex(16)
    
    return True

def logout():
    del session["user_id"]


def signin(username, password):
    try:
        sql = "INSERT INTO endusers (username,password) VALUES (:username,:password)"
        db.session.execute(
            sql, {"username": username, "password": password})
        db.session.commit()
    except:
        return False
    return True

# Flaw 4 fix (replace method with this)
#     hash_value = generate_password_hash(password)

#     try:
#         sql = "INSERT INTO endusers (username,password) VALUES (:username,:password)"
#         db.session.execute(
#             sql, {"username": username, "password": hash_value})
#         db.session.commit()
#     except:
#         return False
#     return True

# Flaw 3 fix (add)
# def user_id():
#     return session.get("user_id", 0)

# Flaw 1 fix (add)
# def check_csrf():
#     if session["csrf_token"] != request.form["csrf_token"]:
#         abort(403)
