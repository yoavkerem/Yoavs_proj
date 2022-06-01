import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="Yoav Kerem",
  password="yoavkay25",
  database="wordsdb"
)

mycursor = mydb.cursor()
#mycursor.execute("CREATE DATABASE wordsdb")
#mycursor.execute("CREATE TABLE PaintedWords(word VARCHAR(50),paintID INT PRIMARY KEY AUTO_INCREMENT)")
"""sql = "INSERT INTO PaintedWords (word) VALUES (%s)"
val = [
  ['שעון'],
  ['טפטוף'],
  ['תיבה'],
  ['נר'],
  ['גמד'],
  ['אוטו'],
  ['חמור'],
  ['שקיעה'],
  ['דגל'],
  ['אבטיח'],
  ['עץ דקל'],
  ['בניין'],
  ['רמזור'],
  ['איש שלג'],
  ['טורנדו'],
  ['גמל'],
  ['קומקום'],
  ['עציץ'],
  ['משאית'],
  ['מנוף'],
  ['פלוץ'],
  ['גול'],
  ['כפפה'],
  ['חגורה'],
  ['זיקוקים'],
  ['קרחת'],
  ['בייגלה'],
  ['תולעת'],
  ['תמנון'],
  ['תרמיל'],
]

mycursor.executemany(sql, val)
mydb.commit()"""



#mycursor.execute("SELECT * FROM Paint")
#for x in mycursor:
#  print(x)