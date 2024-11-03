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
            self.db.connectUsers()
            print("Fethcing tasks...")
            users = self.db.get_users()
            self.updateStartDB(users)         
            time.sleep(1)
            self.db.close_connectionUsers()
            time.sleep(1)
            
    def updateStartDB(self, users) -> None:
        self.db.update_users(users)

    def updateEndDB(self, users) -> None:
        self.db.end_users(users)

    def stop(self) -> None:
        print("Stopping controller and closing database connection...")
        self.running = False
        time.sleep(3) # Se espera que las tasks que se han detenido a mano se actualicen en la base de datos
        self.db.close_connectionUsers()
        exit()