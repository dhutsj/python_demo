import sqlite3

db_file_path = 'demo.db'


class DBManager(object):
    def __init__(self, **params):
        self.db = params['db_file_path']
        self.conn = None
        self.cursor = None
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(DBManager, "_instance"):
            DBManager._instance = object.__new__(cls)
        return DBManager._instance

    def connect(self):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()

        return self.conn, self.cursor

    def execute(self, sql):
        print(sql)
        try:
            conn, cursor = self.connect()
            cursor.execute(sql)
            conn.commit()
            return cursor.fetchall()
        except Exception as e:
            print(e)
            self.conn.rollback()
            exit(1)
        finally:
            self.close_db()

    def close_db(self):
        self.conn.close()


if __name__ == '__main__':
    s1 = DBManager(db_file_path=db_file_path)
