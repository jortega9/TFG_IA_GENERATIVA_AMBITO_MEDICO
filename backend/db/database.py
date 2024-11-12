import mysql.connector
import datetime
import os
from dotenv import load_dotenv
from typing import List, Dict
import json

class DatabaseConnection:
    def __init__(self) -> None:
        load_dotenv()
        self.connUser = None 

    def insert_user(self, user) -> None:
        self.connectDB()
        cursor = self.connUser.cursor()
        query = """
            INSERT INTO user (
                uuid_user, name, username, email, password, secret, date, last_updated, last_login, uuid_group, validated, token, is_active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(
            query, 
                (
                    user.uuid_user,
                    user.name,
                    user.username, 
                    user.email, 
                    user.password, 
                    user.secret, 
                    user.date, 
                    user.last_update, 
                    user.last_login, 
                    user.uuid_group, 
                    user.validated, 
                    user.token,
                    user.is_active,
                )   
            )
            self.connUser.commit()
        except Exception as e:
            self.connUser.rollback()
            raise Exception("insert_user: " + str(e))
        finally:
            cursor.close()
            self.close_connectionDB()

    def update_user_login(self, user_id, date, token) -> None:
        self.connectDB()
        cursor = self.connUser.cursor()
        query = """
        UPDATE user 
        SET last_updated = %s, last_login = %s, token = %s, is_active = 1 
        WHERE uuid_user = %s
        """
        try:
            cursor.execute(query, (date, date, token, user_id))
            self.connUser.commit()
        except Exception as e:
            raise Exception("update_user_login: " + str(e))
        finally: 
            cursor.close()   
            self.close_connectionDB()

    def update_user_logout(self,uuid, date) -> None:
        self.connectDB()
        cursor = self.connUser.cursor()
        query = """
        UPDATE user 
        SET last_updated = %s, last_login = %s, token = NULL, is_active = 0 
        WHERE uuid_user = %s
        """
        try:
            print("uuid: ", uuid)
            cursor.execute(query, (date, date, uuid))
            self.connUser.commit()
        except Exception as e:
            raise Exception("update_user_logout: " + str(e))
        finally:    
                cursor.close()
                self.close_connectionDB()

    def get_active_user(self, uuid) -> dict:
        self.connectDB()
        cursor = self.connUser.cursor(dictionary=True) 
        query = """SELECT * FROM user WHERE uuid_user = %s AND is_active = 1"""
        print("query: ", query)
        print("uuid: ", uuid)
        cursor.execute(query, (uuid,))
        user = cursor.fetchone()
        print("user: ", user)
        cursor.close()
        self.close_connectionDB()
        return user

    def delete_user(self, uuid) -> None:
        self.connectDB()
        cursor = self.connUser.cursor()
        query = """
        DELETE FROM user WHERE uuid_user = %s
        """
        try:
            cursor.execute(query, (uuid,))
            self.connUser.commit()
        except Exception as e:
            raise Exception("delete_user: " + str(e))
        finally:
            cursor.close()
            self.close_connectionDB()

    def get_user_exist(self, identifier) -> bool:
        self.connectDB()
        cursor = self.connUser.cursor()
        query = """SELECT * FROM user 
                    WHERE email = %s OR username = %s
                """   
        cursor.execute(query, (identifier, identifier))   
        user = cursor.fetchone()
        cursor.close()
        self.close_connectionDB()
        return user is not None




    def get_users(self) -> List[Dict]:
        self.connectDB()
        cursor = self.connUser.cursor()
        query = """SELECT * FROM user """   
        cursor.execute(query)   
        users = cursor.fetchall()
        cursor.close()
        print("users: ", users)
        cursor.close()
        self.close_connectionDB()
        return users
    
    def get_user_identifier(self, identifier) -> dict:
        self.connectDB()
        cursor = self.connUser.cursor()
        query = """SELECT * FROM user 
                    WHERE email = %s OR username = %s
                """   
        cursor.execute(query, (identifier, identifier))   
        user = cursor.fetchone()
        cursor.close()
        self.close_connectionDB()
        
        if user is None:
            return None
        
        columns = [desc[0] for desc in cursor.description]
        return dict(zip(columns, user))


    def update_user_account(self, user, uuid) -> None:
        self.connectDB()
        cursor = self.connUser.cursor()
        query = """
        UPDATE user
        SET name = %s,
            username = %s,
            email = %s
        WHERE uuid_user = %s
        """
        try:
            cursor.execute(query, (user.name, user.username, user.email, uuid))
            self.connUser.commit()
        except Exception as e:
            raise Exception("update_user_account: " + str(e))
        finally:
            cursor.close()
            self.close_connectionDB()

    def get_user_info(self, uuid) -> dict:
        self.connectDB()
        cursor = self.connUser.cursor(dictionary=True)  # Configura el cursor para que devuelva un diccionario
        query = """SELECT name, username, email, password FROM user WHERE uuid_user = %s"""
        cursor.execute(query, (uuid,))
        user = cursor.fetchone()  # Obtiene solo un registro
        cursor.close()
        self.close_connectionDB()
        return user  

    def close_connectionDB(self) -> None:
        self.connUser.close()
        
    def connectDB(self) -> None:
        print(f"DB_HOST {os.getenv('DB_HOST')}")
        print(f"DB_USER {os.getenv('DB_USER')}")
        print(f"DB_PASSWORD {os.getenv('DB_PASSWORD')}")
        print(f"DB_NAME {os.getenv('DB_NAME')}")
            
        try:
            self.connUser = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME"),
                collation="utf8mb4_unicode_ci" 
            )
            print("Connected to the database")
        except mysql.connector.Error as err:
            print(f"Error: {err}")