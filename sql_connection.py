import mysql.connector as conn
mydb=conn.connect(host="localhost",user="root",password="123456") ###workbench user,password
print(mydb,"connection established............")

my_db=mydb.cursor()
# my_db.execute("create database airline_ticket")
my_db.execute("use airline_ticket")

##---show database
# my_db.execute("SHOW DATABASES")
# for x in my_db:
#   print(x)

##---show tables
# my_db.execute("SHOW TABLES")
# for x in my_db:
#   print(x)
my_db.execute("describe UserData")


my_db.close()