import csv
import sqlite3

con = sqlite3.connect("avas.db")
cursor = con.cursor()


# query = "CREATE TABLE IF NOT EXISTS sys_command (id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
# cursor.execute(query)

# For Applications

# query = "INSERT INTO sys_command VALUES (null,'discord', 'C:\\Users\\acer\\AppData\\Local\\Discord\\app-1.0.9163\\Discord.exe')"
# cursor.execute(query)
# con.commit()

# query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
# cursor.execute(query)

# query = "INSERT INTO web_command VALUES (null,'youtube', 'https://www.youtube.com')"
# cursor.execute(query)
# con.commit()

# Create a table with the desired columns
#cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')



# Specify the column indices you want to import (0-based index)
# Example: Importing the 1st and 3rd columns
desired_columns_indices = [0, 30]

# # Read data from CSV and insert into SQLite table for the desired columns
with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
     csvreader = csv.reader(csvfile)
     for row in csvreader:
         selected_data = [row[i] for i in desired_columns_indices]
         cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# # Commit changes and close connection
con.commit()
con.close()