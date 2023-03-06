from flask_mysqldb import MySQL
import MySQLdb.cursors

mysql = MySQL()

def MySQLGet(request):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(request)
    return cursor.fetchall()
