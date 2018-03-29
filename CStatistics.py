import sqlite3

# NOT FINISHED STATISTICS CLASS FOR CREATING STATISTICS ABOUT ACHIVEMENTS OF THE NEURAL NETWORK

class CStatistics:

    def __init__(self):
        self.conn = sqlite3.connect('data.db')

        c = self.conn.cursor()

        c.execute('CREATE TABLE IF NOT EXISTS `testing` ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, `epoche` INTEGER, `is_digit` INTEGER DEFAULT -1 )')

    def addRow(self):

        c = self.conn.cursor()

        c.execute("INSERT INTO testing VALUES (NULL,101,3)")


    def save(self):
        self.conn.commit()
        self.conn.close()
