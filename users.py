import secrets
from flask import session, abort, request
# Flaw 4 fix (add): from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def login(username, password):
    sql = "SELECT id, password FROM endusers WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    if not user.password == password:
        return False

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
    admin = 0;
    try:
        sql = "INSERT INTO endusers (username, password, admin) VALUES (:username,:password, :admin)"
        db.session.execute(
            sql, {"username": username, "password": password, "admin":admin})
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

def user_id():
    return session.get("user_id", 0)

def get_id_with_name(username):
    sql = "SELECT id FROM endusers WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user_id = result.fetchone()[0]
    return user_id

def get_name():
    id = user_id()
    sql = "SELECT username FROM endusers WHERE id=:id"
    result = db.session.execute(sql, {"id": id})
    user_name = result.fetchone()[0]
    return user_name

# Flaw 3 fix (add)
# def user_accessing_own_info(username):
#     return user_id() == get_id_with_name(username)

def is_admin():
    id = user_id()
    sql = "SELECT admin FROM endusers WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    admin = result.fetchone()[0]
    return admin==1

# Flaw 1 fix (add)
# def check_csrf():
#     if session["csrf_token"] != request.form["csrf_token"]:
#         abort(403)
