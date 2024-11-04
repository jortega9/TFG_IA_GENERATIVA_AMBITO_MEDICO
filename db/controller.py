from database import DatabaseConnection

import json
import time

class Controller:
    def __init__(self, db: DatabaseConnection) -> None:
        self.db = db
        self.running = True
        
    def run(self) -> None:
        print("Controller is running...")
        
        while self.running:
            self.db.connectUser()
            print("Fethcing users...")
            users = self.db.get_users()
            self.updateStartDB(users)         
            time.sleep(1)
            self.db.close_connectionUser()
            time.sleep(1)
            
    def updateStartDB(self, users) -> None:
        self.db.update_user_account(users)

    def updateEndDB(self, users) -> None:
        self.db.end_users(users)

    def stop(self) -> None:
        print("Stopping controller and closing database connection...")
        self.running = False
        time.sleep(3) 
        self.db.close_connectionUser()
        exit()