import mysql.connector
from mysql.connector import Error


def create_connection():
    """Establish connection to the MySQL database"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='PharmacyManagement',
            user='root',
            password='admin'
        )
        if connection.is_connected():
            print('Connected to the Database')
            return connection
        else:
            print('Failed to connect to the database')
            return None
    except Error as e:
        print(f"Error: {e}")
        return None


def close_connection(connection):
    """Close the database connection"""
    if connection and connection.is_connected():
        connection.close()
        print("Connection closed")
