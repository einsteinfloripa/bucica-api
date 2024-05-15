from schedule import run_pending
from time import sleep

def update_attendance_loop():
    while True:
        run_pending()
        sleep(5)
    