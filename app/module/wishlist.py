def insert_wish_list(database, id, t_id):
    try:
        sql_command = 'insert into wishlist values(\'{}\', {});'.format(id, t_id)
        database.execute(sql_command)
        database.commit()
    except:
        database.valid = False
    return

def get_wish_list(database, id) :
    try:
        database.commit()
        sql_command = 'select * from wishlist join trade where wishlist.id=\'{}\' and wishlist.t_id=trade.t_id'.format(id)
        query = database.executeAll(sql_command)
    except:
        database.valid = False
    return query