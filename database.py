from flask_mysqldb import MySQL
import MySQLdb.cursors

mysql = MySQL()

def MySQLGet(request, data):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(request, data)
    return cursor.fetchall()

def MySQLExecute(request, data):
    cursor = mysql.connection.cursor()
    cursor.execute(request, data)
