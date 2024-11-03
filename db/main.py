import signal
from database import DatabaseConnection
from controller import Controller

def main() -> None: 
    db: DatabaseConnection = DatabaseConnection()
    controller: Controller = Controller(db)
    
    def stop_controller(signum, frame):
        controller.stop()
    
    signal.signal(signal.SIGINT, stop_controller)
    signal.signal(signal.SIGTERM, stop_controller)
    
    controller.run()
    db.close_connectionUsers()

if __name__ == "__main__":
    main()