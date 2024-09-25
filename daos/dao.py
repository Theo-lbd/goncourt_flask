import mysql.connector

class DAO:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='127.0.0.1',
            database='goncourt_book',
            user='root',
            password='b2voz7rEehsiLhJaXyRW'  # Remplace par ton mot de passe
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
