def get_user_info(database):
    database.commit()
    sql_command = 'select * from user;'
    query = database.executeAll(sql_command)
    return query

def delete_user_info(database, id_list):
    database.commit()
    for id in id_list:
        sql_command = 'delete from user where id=\'{}\';'.format(id)
        database.executeAll(sql_command)
    return