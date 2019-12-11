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

def delete_trades(database, t_ids):
    for t_id in t_ids:
        sql_command = 'delete from trade where t_id = {}'.format(t_id)
        database.execute(sql_command)
        database.commit()
    return

def purchase_trade(database, t_ids, amounts, id):
    sum = 0
    amounts_list = []
    for idx, t_id in enumerate(t_ids):
        sql_command = 'select * from trade where t_id = {};'.format(t_id)
        query = database.executeAll(sql_command)
        amounts_list.append((query[0]['price'], query[0]['seller'], query[0]['item_num']))
        if amounts[idx] > query[0]['item_num']:
            return -1
        sum += query[0]['price'] * amounts[idx]

    sql_command = 'select * from user where id = \'{}\';'.format(id)
    query = database.executeAll(sql_command)
    if query[0]['MONEY'] < sum:
        return -1

    sql_command = 'update user set money = money - {} where id = \'{}\';'.format(sum, id)
    database.execute(sql_command)
    database.commit()

    for idx, t_id in enumerate(t_ids) :
        sql_command = 'update trade set item_num = item_num - {} where t_id = {}'.format(amounts[idx], t_id)
        print(sql_command)
        database.execute(sql_command)
        database.commit()

        if amounts_list[idx][2] - amounts[idx] == 0:
            sql_command = 'update trade set valid = 0 where t_id = {};'.format(t_id)
            database.execute(sql_command)
            database.commit()

        sql_command = 'update user set money = money + {} where id = \'{}\';'.format(amounts_list[idx][0], amounts_list[idx][1])
        database.execute(sql_command)
        database.commit()

    return 0