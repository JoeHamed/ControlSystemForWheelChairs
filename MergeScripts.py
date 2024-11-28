import subprocess
from time import sleep
import threading
import os

def run_batch_file(file_path):
    try:
        process = subprocess.Popen([file_path])
        process.wait()  # Wait for the process to complete
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running {file_path}: {e}")


def main():
    try:
        mode_id = int(input("Enter the mode number (2 or 3): "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    if mode_id == 2:
        thread1 = threading.Thread(target=run_batch_file, args=(
        r'C:\Users\youse\Desktop\Eyes-Position-Estimator-Mediapipe-master\Eye_Tracking_part4\test2run.bat',))
        thread1.start()
        sleep(5)
        thread2 = threading.Thread(target=run_batch_file, args=(
            r'C:\Users\youse\Desktop\Eyes-Position-Estimator-Mediapipe-master\Eye_Tracking_part4\socketconn2run.bat',))
        thread2.start()
    elif mode_id == 3:
        thread1 = threading.Thread(target=run_batch_file, args=(
        r'C:\Users\youse\Desktop\Eyes-Position-Estimator-Mediapipe-master\Eye_Tracking_part4\main_M3run.bat',))
        thread1.start()
        sleep(5)
        #  due to an issue with timing between YOLO and the socket connection
        #  (using OS.startfile instead of another thread)
        os.startfile("C:\\Users\\youse\\Desktop\\Eyes-Position-Estimator-Mediapipe-master\\Eye_Tracking_part4\\socketconn2run.bat")
    else:
        print("Invalid mode number. Please enter 2 or 3.")
        return

    # Optionally, join the threads if you want to wait for them to finish\
    thread1.join()
    try:
        thread2.join()
    except:
        pass

if __name__ == "__main__":
    main()


