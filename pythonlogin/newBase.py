import mysql.connector as mariadb
from passlib.hash import sha256_crypt
def initDatabase():
	mariadb_connection = mariadb.connect(user='root', password='rootpassword', host='assassins-db', port='3306')

	cur = mariadb_connection.cursor()
	try:
		cur.execute('DROP DATABASE Assassins')
	except:
		pass
	cur.execute('CREATE DATABASE Assassins')
	cur.execute('USE Assassins')
	try:
		cur.execute('DROP TABLE first')
	except:
		pass
	cur.execute('CREATE TABLE first (`uid` INT(11) AUTO_INCREMENT PRIMARY KEY, `username` VARCHAR(100), `email` VARCHAR(100), `password` VARCHAR(200), `photo` longblob);')

	mariadb_connection.commit()
	cur.close()