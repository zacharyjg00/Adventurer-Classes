import mysql.connector

mydb = mysql.connector.connect(host = "localhost", user = "root", passwd = "root", port = 3306, database = "adventurer_matches")

mycursor = mydb.cursor()
mycursor.execute("select * from match_scores")

for x in mycursor:
   print(x)