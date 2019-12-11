def register_trade(database, title, des, item_name, item_num, price, seller):
    try:
        sql_command = 'insert into trade value(0, \'{}\', \'{}\', \'{}\', {}, \'{}\', NULL, 1, {});'.format(title, des, item_name, price, seller, item_num)
        database.execute(sql_command)
        database.commit()
    except:
        database.valid=False
    return

def get_trades(database):
    try:
        database.commit()
        sql_command = 'select * from trade;'
        query = database.executeAll(sql_command)
    except:
        database.valid = False
    return query

def get_trade(database, trade_id):
    try:
        database.commit()
        sql_command = 'select * from trade where t_id = {};'.format(trade_id)
        query = database.executeAll(sql_command)
    except:
        database.valid = False
    return query

def get_sell_trades(database, id):
    try:
        database.commit()
        sql_command = 'select * from trade where seller = \'{}\';'.format(id)
        query = database.executeAll(sql_command)
    except:
        database.valid = False
    return query

def get_buy_trades(database, id):
    try:
        database.commit()
        sql_command = 'select * from trade where buyer = \'{}\';'.format(id)
        query = database.executeAll(sql_command)
    except:
        database.valid = False
    return query