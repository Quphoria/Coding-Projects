class DB:
    def __init__(self):
        import sqlite3
        self.conn = sqlite3.connect('sqlite.db')
    def load(self):
        self.c = self.conn.cursor()
    def save(self):
        self.conn.commit()
    def exit(self):
        self.conn.close()
    def run_sql(self,sql,argument=None):
        if argument:
            data = self.c.execute(sql,argument)
        else:
            data = self.c.execute(sql)
        return data
    def run_many_sql(self,sql,argument):
        return self.c.executemany(sql,argument)
