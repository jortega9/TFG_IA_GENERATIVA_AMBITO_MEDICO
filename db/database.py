import mysql.connector
import datetime
import os
from dotenv import load_dotenv
from typing import List, Dict
import json

class DatabaseConnection:
    def __init__(self) -> None:
        load_dotenv()

    def insert_user(self, user) -> None:
        cursor = self.connUser.cursor()
        query = """
        INSERT INTO user (uuid_user, username, email, password, secret, date, last_update, last_login, uuid_group, validated, token, is_active)
        VALUES (${user})
        """
        # args = json.dumps(user.tp_arguments_desc.__dict__)
        try:
            cursor.execute(
            query, 
            (
                user.uuid_user, 
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
                # str(args)
            )
        )
        except Exception as e:
            raise Exception("insert_user: " + str(e))
        self.connUser.commit()

    def delete_user(self, uuid_user) -> None:
        cursor = self.connUser.cursor()
        query = """
        DELETE FROM user WHERE uuid_user = %s
        """
        try:
            # Ejecutar la consulta con el valor de uuid_user
            cursor.execute(query, (uuid_user,))
        except Exception as e:
            raise Exception("delete_user: " + str(e))
        self.connUser.commit()



    def get_users(self) -> List[Dict]:
        cursor = self.connUser.cursor()
        query = """SELECT * FROM user """   
        cursor.execute(query)   
        users = cursor.fetchall()
        cursor.close()
        print("users: ", users)
        return users
    
    def get_user_identifier(self, identifier) -> List[Dict]:
        cursor = self.connUser.cursor()
        query = """SELECT * FROM user 
                    WHERE email = %s OR username = %s
                """   
        cursor.execute(query, (identifier, identifier))   
        users = cursor.fetchall()
        cursor.close()
        print("user: ", identifier)
        return users

    def update_user_account(self, user) -> None:
        cursor = self.connUser.cursor()
        query = """
        UPDATE user
        SET name = %s,
            email = %s,
            password = %s,
        WHERE uuid_user = %s
        """

        cursor.execute(query, (user.name, user.email, user.password, user.uuid_user))
        self.connUser.commit()

    # def endUsers(self, user: Dict) -> None:
        
    #     cursor = self.connUser.cursor()
    #     update_query = """
    #     UPDATE user
    #     SET tp_status = %s,
    #         tp_finish_date = %s,
    #         tp_arguments_desc = %s
    #     WHERE tp_uid = %s
    #     """
    #     insert_query = """
    #     INSERT INTO tasks_completed (tc_uid, tc_task_type, tc_uid_depend, tc_status, tc_creation_date, tc_initial_date, tc_finish_date, tc_actual_attempt, tc_max_attempts, tc_working_machine, tc_priority, tc_arguments_desc)
    #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    #     """
    #     with open('/etc/machine-id', 'r') as f:
    #         machine_id = f.read().strip()
    
    #     args = json.dumps(user.tp_arguments_desc.__dict__)
    #     try:
    #         cursor.execute(update_query, (config.get("finished_status"),datetime.datetime.now(), str(args) ,user.tp_uid))
    #     except Exception as e:
    #         raise Exception("tasks_pending: " + str(e))
    #     try:
    #         cursor.execute(insert_query, (user.tp_uid, user.tp_user_type, user.tp_uid_depend, config.get("finished_status"), user.tp_creation_date, user.tp_initial_date, user.tp_finish_date, user.tp_actual_attemps + 1, user.tp_max_attemps, machine_id, user.tp_priority, str(args)))
    #     except Exception as e:
    #         raise Exception("tasks: " + str(e))
    #     self.connUser.commit()
        
    # def updateError(self, user: Dict, error: Exception) -> None:
    #     cursor = self.connUser.cursor()
    #     query = """
    #     UPDATE tasks_pending
    #     SET tp_status = %s,
    #         tp_status_error = %s
    #     WHERE tp_uid = %s
    #     """
    #     cursor.execute(query, (config.get("error_status"), str(error), user[0]))
    #     self.connUser.commit()        

    def close_connectionUser(self) -> None:
        self.connUser.close()
        
    def connectUser(self) -> None:
        self.connUser = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )