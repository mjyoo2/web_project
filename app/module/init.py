def initdb(database):
    database.execute('delete from wishlist;')
    database.execute('delete from trade;')
    database.execute('delete from user;')
    database.execute('ALTER TABLE trade AUTO_INCREMENT = 1')
    database.commit()

    sql_command = ['insert into user value(\'admin\', \'관리자\', \'password\', 10000);']
    for i in range(50):
        sql_command.append('insert into user value(\'id{}\', \'name{}\', \'password{}\', 10000);'.format(i, i, i))
    for command in sql_command:
        database.execute(command)
        database.commit()

    sql_command = []
    for i in range(400):
        sql_command.append('insert into trade value(0, \'title{}\', \'description{}\', \'item{}\', 3000, \'id{}\', NULL, 1, 10);'.format(i, i, i, i%50))

    for command in sql_command:
        database.execute(command)
        database.commit()

    sql_command = []
    for i in range(50):
        for j in range(10):
            sql_command.append('insert into wishlist value(\'id{}\', {});'.format(i, (i + 2 * j) % 50 + 1))

    for command in sql_command:
        database.execute(command)
        database.commit()

from app.module.database import Database

if __name__ == '__main__':
    database = Database()
    initdb(database)