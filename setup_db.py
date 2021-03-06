import sqlite3 as sql

# Connect to database
con = sql.connect('database.db')

# Get a cursor to the database
cur = con.cursor()

# Drop the user table if it exists
cur.execute('DROP TABLE IF EXISTS User')

# Drop the messages table if it exists
cur.execute('DROP TABLE IF EXISTS Messages')

# Create the User table
cur.execute('''CREATE TABLE User(
    User_id INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT NOT NULL)
    ''')

# Create the Messages table
cur.execute('''CREATE TABLE Messages(
    Message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT NOT NULL,
    Content TEXT)
    ''')

con.commit()

con.close()
