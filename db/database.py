import mysql.connector
import datetime
import os
from dotenv import load_dotenv
from typing import List, Dict
import json

with open("/home/luxor/proyects/visionTask/src/utils/config.json") as f:
    config = json.load(f)

class DatabaseConnection:
    def __init__(self) -> None:
        load_dotenv()

    def get_users(self, users_amount: int) -> List[Dict]:
        cursor = self.connTask.cursor()
        query = """SELECT * FROM user
                    WHERE (tp_status = %s OR tp_status = %s) AND tp_task_type LIKE %s
                    AND tp_actual_attempt < tp_max_attempts ORDER BY tp_priority DESC
                    LIMIT %s
                """   
        cursor.execute(query, (config["pending_status"],config["error_status"], config["tp_task_type"],task_amount))   
        users = cursor.fetchmany(users_amount)
        cursor.close()
        print("users: ", users)
        return users

    def update_users(self, users: List[Dict]) -> None:
        cursor = self.connTask.cursor()
        query = """
        UPDATE user
        SET tp_status = %s,
            tp_initial_date = %s,
            tp_actual_attempt = tp_actual_attempt + 1,
            tp_working_machine = %s
        WHERE tp_uid = %s
        """
        with open('/etc/machine-id', 'r') as f:
            machine_id = f.read().strip()
        for user in users:
            cursor.execute(query, (config.get("in_progress_status"),datetime.datetime.now(), machine_id, user[0]))
        self.connTask.commit()
 
    def endUsers(self, user: Dict) -> None:
        
        cursor = self.connTask.cursor()
        update_query = """
        UPDATE user
        SET tp_status = %s,
            tp_finish_date = %s,
            tp_arguments_desc = %s
        WHERE tp_uid = %s
        """
        insert_query = """
        INSERT INTO tasks_completed (tc_uid, tc_task_type, tc_uid_depend, tc_status, tc_creation_date, tc_initial_date, tc_finish_date, tc_actual_attempt, tc_max_attempts, tc_working_machine, tc_priority, tc_arguments_desc)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        with open('/etc/machine-id', 'r') as f:
            machine_id = f.read().strip()
       
        args = json.dumps(user.tp_arguments_desc.__dict__)
        try:
            cursor.execute(update_query, (config.get("finished_status"),datetime.datetime.now(), str(args) ,user.tp_uid))
        except Exception as e:
            raise Exception("tasks_pending: " + str(e))
        try:
            cursor.execute(insert_query, (user.tp_uid, user.tp_user_type, user.tp_uid_depend, config.get("finished_status"), user.tp_creation_date, user.tp_initial_date, user.tp_finish_date, user.tp_actual_attemps + 1, user.tp_max_attemps, machine_id, user.tp_priority, str(args)))
        except Exception as e:
            raise Exception("tasks: " + str(e))
        self.connTask.commit()
        
    def updateError(self, user: Dict, error: Exception) -> None:
        cursor = self.connTask.cursor()
        query = """
        UPDATE tasks_pending
        SET tp_status = %s,
            tp_status_error = %s
        WHERE tp_uid = %s
        """
        cursor.execute(query, (config.get("error_status"), str(error), user[0]))
        self.connTask.commit()        

    def close_connectionTask(self) -> None:
        self.connTask.close()
        
    def connectTask(self) -> None:
        self.connTask = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )