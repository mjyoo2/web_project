# user table is consist of id, name, password, money.

def check_id_db(database, id):
    try:
        database.commit()
        sql_command = 'select * from user where id=\'{}\''.format(id)
        query = database.executeAll(sql_command)
    except:
        database.valid = False
    if query:
        return True
    else:
        return False

def register_db(database, id, name, password):
    try:
        sql_command_prev = 'select * from user where id=\'{}\''.format(id)
        query_prev = database.executeAll(sql_command_prev)
    except:
        database.valid = False
    if query_prev:
        return False
    try:
        sql_command = 'insert into user value(\'{}\', \'{}\', \'{}\', 0)'.format(id, password, name)
        database.execute(sql_command)
        database.commit()
    except:
        database.valid = False
    return True

def login_db(database, id, password):
    try:
        database.commit()
        sql_command = 'select * from user where id=\'{}\' and password=\'{}\''.format(id, password)
        query = database.executeAll(sql_command)
    except:
        database.valid = False
    if query:
        return True
    else:
        return False

def get_info_db(database, id):
    try:
        database.commit()
        sql_command = 'select * from user where id=\'{}\''.format(id)
        query = database.executeAll(sql_command)
        return query[0]['ID'], query[0]['NAME'], query[0]['MONEY']
    except:
        database.valid = False
        return '', '', 0


