import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="Yoav Kerem",
  password="yoavkay25",
  database="wordsdb"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM PaintedWords")
myresult = mycursor.fetchtwo()

print(myresult)