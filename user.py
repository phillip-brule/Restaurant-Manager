import pyodbc 

def read(conn):
    print("Reading")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM restaurant")
    for row in cursor:
        print(f'row = {row}')
    print()

def create(conn):
    print("Creating")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO restaurant(name) VALUES(?);",
        ('Phills Restaurant'))
    conn.commit()
    read(conn)
def update(conn):
    print("Updating")
    cursor = conn.cursor()
    cursor.execute("UPDATE restaurant SET name = ? WHERE name = ?;",
        ('New restaurant','Phills Restaurant'))
    conn.commit()
    read(conn)

conn = pyodbc.connect(
    "Driver={SQL Server Native Client 11.0}"
    "Server=localhost;"
    "PORT=5432;"
    "Database=RestaurantManager;"
    "Trusted_Connection=yes;"
    "UID=postgres;"
    "PWD=dovakin"
)

read(conn)
create(conn)
update(conn)

class User:
    def __init__(self, id, name, phoneNumber, email):
        self.id = id
        self.name = name
        self.phoneNumber = phoneNumber
        self.email = email