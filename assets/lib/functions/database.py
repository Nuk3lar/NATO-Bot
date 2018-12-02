# SQL Module
import MySQLdb

def TEST_RUN():
    from config.confmain import dbconnect
    db = dbconnect()
    db[0].close()


def get_users(db):
    get_users = "SELECT id FROM users"
    db[1].execute(get_users)
    return [item[0] for item in db[1].fetchall()]


def add_user(db, user, rank):
    query = "INSERT INTO users (id, name, rank, status) VALUES(%s, %s, %s, 'Active')"
    try: db[1].execute(query, insert)
    except:
        insert = (str(user.id), user.name.encode('utf-8'), rank, )
        db[1].execute(query, insert)


def get_user(db, user):
    query = "SELECT * FROM users WHERE id = %s"
    db[1].execute(query, (user.id, ))
    return list(([item for item in db[1].fetchall()])[0])


def set_mos(db, user, mos):
    query = "UPDATE users SET mos = %s WHERE id = %s"
    db[1].execute(query, (mos, user.id, ))
    

def set_callsign(db, user, callsign):
    query = "UPDATE users SET callsign = %s WHERE id = %s"
    db[1].execute(query, (callsign, user.id, ))


def set_descr(db, user, descr):
    query = "UPDATE users SET descr = %s WHERE id = %s"
    db[1].execute(query, (descr, user.id, ))

    
def get_status(db, user):
    query = "SELECT status FROM users WHERE id = %s"
    db[1].execute(query, (user.id, ))
    return ([item[0] for item in db[1].fetchall()])[0]


def set_status(db, user, status):
    query = "UPDATE users SET status = %s WHERE id = %s"
    db[1].execute(query, (status, user.id, ))


def get_ranks(db):
    query = "SELECT id, rank FROM users"
    db[1].execute(query, ( ))
    users_2 = {}
    dbout = db[1].fetchall()
    for user in dbout: users_2[user[0]] = user[1]
    return users_2

def update_user_rank(db, user, rank):
    query = "UPDATE users SET rank = %s WHERE id = %s"
    db[1].execute(query, (rank, user.id, ))
