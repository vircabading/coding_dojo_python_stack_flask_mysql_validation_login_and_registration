import pymysql.cursors

class MySQLConnection:
    def __init__(self, db):
        self.connection = pymysql.connect(
            host = 'localhost',
            user = 'root', 
            password = 'root',#YOUR PASSWORD HERE INSTEAD OF 'root'
            db = db,
            charset = 'utf8mb4',
            cursorclass = pymysql.cursors.DictCursor,
            autocommit = True
        )
    def query_db(self,query,data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
                cursor.execute(query)
                if query.lower().strip().startswith("select"):
                    # **** SELECT queries will return the data from the database as a LIST OF DICTIONARIES ********
                    return cursor.fetchall()
                elif query.lower().strip().startswith("insert"):
                    # **** INSERT queries will return the ID NUMBER of the row inserted ********
                    return cursor.lastrowid
                # **** UPDATE and DELETE queries will return nothing ********
            except Exception as e:
                print("Something went wrong", e)
                return False
            finally:
                self.connection.close()

def connectToMySQL(db):
    return MySQLConnection(db)