import sqlite3 as sql

# Connect to database
con = sql.connect('data.db')

# Get a cursor to the database
cur = con.cursor()

# Drop the user table if it exists
cur.execute('DROP TABLE IF EXISTS User')

con.commit()

# Create the User table
cur.execute('''CREATE TABLE User(
    User_id INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT NOT NULL)
    ''')

con.commit()

con.close()
