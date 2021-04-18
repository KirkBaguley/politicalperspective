import psycopg2
import psycopg2.extras

class UserDB:

    def __init__(self):
        self.connection = psycopg2.connect(database='ddjhsokue67o70', user='svxpxvoanaufdc', password='ba4dfaaf6c380974d6f07dcdfed8fff747a023644e8cee42124244cc79b428f0', host='ec2-35-174-35-242.compute-1.amazonaws.com', port='5432')
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def insertUser(self, fname, lname, age, email, password):
        data = [fname,lname,age,email,password]
        self.cursor.execute("INSERT INTO users (fname,lname,age,email,password) VALUES (%s, %s, %s, %s, %s);", data)
        self.connection.commit()

    def getOneUser(self,email):
        data = [email]
        self.cursor.execute("SELECT id, fname, lname FROM users WHERE email = %s;", data)
        user = self.cursor.fetchone()
        return user

    def verifyUser(self,email):
        data = [email]
        self.cursor.execute("SELECT password FROM users WHERE email = %s;", data)
        password = self.cursor.fetchone()
        return password
