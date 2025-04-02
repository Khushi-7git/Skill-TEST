import sqlite3
def create_db():
    conn=sqlite3.connect('profile.db')
    cursor=conn.cursor()
    cursor.execute(''' CREATE TEBL IF NOT EXISTS profile ('
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_text TEXT''
    sentiment_scoe REAL)''')
    conn.commit()
    conn,close()
if __name__=="__main__":
     create_db ()
        