from db import db
import users

def thing_id(new_thing):
    things = view_things(users.user_id())
    for thing in things:
        thing_trimmed = str(thing[0]).strip(",(')")
        if thing_trimmed == new_thing:
            return thing[1]
    return -1


def add_new(thing):
    owner_id = users.user_id()
    hits = 0
    id = thing_id(thing)
    if id > 0:
        add_hits(id)
        return True
    else:
        try:
            sql = "INSERT INTO things (owner_id, thing, hits) VALUES (:owner_id, :thing, :hits)"
            db.session.execute(sql, {"owner_id": owner_id, "thing":thing, "hits": hits})
            db.session.commit()
            return True
        except:
            return False

def add_hits(id):
    sql = "UPDATE things SET hits = hits + 1 WHERE id =:id"
    db.session.execute(sql, {"id": id})
    db.session.commit()


def view_things(owner_id):
    sql = "SELECT thing, id FROM things WHERE owner_id=:owner_id"
    result = db.session.execute(sql, {"owner_id": owner_id})
    return result.fetchall()    

def view_top3(owner_id):
    sql = "SELECT thing FROM things WHERE owner_id=:owner_id ORDER BY hits DESC LIMIT 3"
    result = db.session.execute(sql, {"owner_id": owner_id})
    return result.fetchall()  

def search_things(criteria):
    owner_id = users.user_id()    
    return db.session.execute("SELECT thing FROM things WHERE owner_id='%s' AND thing LIKE '%%%s%%'" % (owner_id, criteria)).fetchall()

def get_everyones_things():
    return db.session.execute("SELECT e.username, t.thing FROM endusers e, things t WHERE e.id=t.owner_id").fetchall()
