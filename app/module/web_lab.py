def web_lab_insert(database, id, depart, name, address, phone):
    sql_command = 'insert into student values({}, \'{}\', \'{}\', \'{}\', \'{}\');'.format(id, depart, name, address, phone)
    database.execute(sql_command)
    return

def web_lab_get(database):
    sql_command = 'select * from student;'
    query = database.executeAll(sql_command)
    return query

def web_lab_delete(database, depart):
    sql_command = 'delete from student where depart=\'{}\';'.format(depart)
    query = database.executeAll(sql_command)
    return query

def web_lab_revise(database, depart, new_depart):
    sql_command = 'update student set depart=\'{}\' where depart=\'{}\';'.format(new_depart, depart)
    query = database.executeAll(sql_command)
    return query