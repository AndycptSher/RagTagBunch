# from neo4j import GraphDatabase, RoutingControl
import os
import sqlite3
import math


# URI = "neo4j+s://"+os.environ["connection_uri"]+".databases.neo4j.io"
# AUTH = ("neo4j", os.environ["auth"]+"https://youtu.be/dQw4w9WgXcQ")
# with GraphDatabase.driver(URI, auth=AUTH) as driver:
#   items = driver.execute_query(
#     """
#     match (n) return (n)
#     """, database_="neo4j", routing_=RoutingControl.READ)
#   for item in items[0]:
#     print(item)
#   ...

# CRUD
# create
# remove
# update
# delete
def display_records(records:list[tuple]):
  print(records)
  def string_display(string: str):
    if (l:=len(string) > 20):
      return string[:17] + "..."
    return string
    
  def float_display(num:float, precision: int=3):
    if not isinstance(precision, int):
      raise TypeError(f"precision must be an integer, not {type(precision)}")
    if precision < 0:
      raise ValueError(f"Precision must be a positive integer, not {precision}")

    if precision > 10:
      raise ValueError("Precision cannot be greater than 10")
    
    if len(str(num)) < 5 + precision:
      return str(num)
    power = math.floor(math.log(num, 10))
    return f"{num / 10 ** power:.{precision-1}f}e{int(power)}"

  def int_display(num:int):
    if len(str(num)) < 8:
      return str(num)
    return f"{num / 10 ** (power:=math.floor(math.log(num, 10))):.{3}f}e{power}"
  
  for record in records:
    for attribute in record:
      if isinstance(attribute, float):
        print(f"{float_display(attribute):>9}", end=" | ")
      elif isinstance(attribute, str):
        print(f"{string_display(attribute):<20}", end=" | ")
      elif isinstance(attribute, int):
        print(f"{int_display(attribute):>8}", end=" | ")
    print()
  ...


display_records([(1.4521, "Hello", 10), (0.0000042252, "World", 891873598470), (179479.2442, "Hello World and other things", 2030000)])



# connection = sqlite3.connect(":memory:")
connection = sqlite3.connect("test.db")
cursor = connection.cursor()
# cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
# cursor.execute("CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, title TEXT, content TEXT, user_id INTEGER, FOREIGN KEY(user_id) REFERENCES users(id))")

# cursor.execute("INSERT INTO users VALUES (1, 'John')")
# cursor.execute("INSERT INTO users VALUES (2, 'Mary')")
# cursor.execute("INSERT INTO users VALUES (3, 'Alice')")

display_records(cursor.execute("select * from users").fetchall())


# cursor.execute("INSERT INTO posts VALUES (0, 'testing', 'this is a testing messgage', 0)")
# cursor.execute("""INSERT INTO users VALUES (0, 'Admin')""")
# cursor.execute("""INSERT INTO users VALUES (4, 'blake')""")
# cursor.execute("INSERT INTO posts VALUES (1, 'my first post', 'Hello',1)")
# cursor.execute("INSERT INTO posts VALUES (2, 'getting the hang of things', '*!',1)")
# cursor.execute("INSERT INTO posts VALUES (3, 'whaaaa', 'uifnvrownvowrv',4)")


# connection.commit()

display_records(cursor.execute("SELECT * FROM posts").fetchall())


display_records(cursor.execute("""
select * 
from posts
INNER JOIN users ON users.id == posts.user_id
where (users.name == "blake"
or users.name == "Admin")
""").fetchall())

connection.close()

print("hey")