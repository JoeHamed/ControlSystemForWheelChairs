import tkinter
from customtkinter import *
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


def var1_set(text):
    var1.set(f"{text}")
    app.update()


def var2_set(text):
    var2.set(f"{text}")
    app.update()


def SSH_initialize():
    # making sure that ssh connection is established before running any script
    os.startfile(
        "C:\\Users\\youse\\Desktop\\Eyes-Position-Estimator-Mediapipe-master\\Eye_Tracking_part4\\SSH_initialize.bat")


def loading_animation(var, stop_event):
    loading_texts = ["Connection is being established.. ", "Connection is being established..."]
    while not stop_event.is_set():
        for text in loading_texts:
            if stop_event.is_set():
                break
            var.set(text)
            app.update()
            sleep(0.5)


def second_mode():
    stop_event = threading.Event()
    thread1 = threading.Thread(target=loading_animation, args=(var1, stop_event))
    thread1.start()

    thread2 = threading.Thread(target=run_batch_file, args=(
        r'C:\Users\youse\Desktop\Eyes-Position-Estimator-Mediapipe-master\Eye_Tracking_part4\test2run.bat',))
    thread2.start()
    sleep(5)
    thread3 = threading.Thread(target=run_batch_file, args=(
        r'C:\Users\youse\Desktop\Eyes-Position-Estimator-Mediapipe-master\Eye_Tracking_part4\socketconn2run.bat',))
    thread3.start()

    thread2.join()
    thread3.join()
    stop_event.set()
    var1_set("Connected!")
    thread1.join()
    var1_set("Mode OFF")


def third_mode():
    stop_event = threading.Event()
    thread1 = threading.Thread(target=loading_animation, args=(var2, stop_event))
    thread1.start()

    thread2 = threading.Thread(target=run_batch_file, args=(
        r'C:\Users\youse\Desktop\Eyes-Position-Estimator-Mediapipe-master\Eye_Tracking_part4\main_M3run.bat',))
    thread2.start()
    sleep(5)
    # due to an issue with timing between YOLO and the socket connection
    # (using OS.startfile instead of another thread)
    os.startfile(
        "C:\\Users\\youse\\Desktop\\Eyes-Position-Estimator-Mediapipe-master\\Eye_Tracking_part4\\socketconn2run.bat")

    thread2.join()
    stop_event.set()
    var2_set("Connected!")
    thread1.join()
    var2_set("Mode OFF")


# ========== GUI ===========

# Create main window

app = CTk()
app.geometry("400x700")
app.title("Mode Switch")
set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
set_appearance_mode("system")  # light or dark depending on your system
set_default_color_theme("MoonlitSky.json")

var1 = tkinter.StringVar()
var2 = tkinter.StringVar()
var1.set("Mode OFF")
var2.set("Mode OFF")

# Create frame

frame = CTkFrame(master=app, width=380, height=640, corner_radius=20, border_width=3, fg_color="#2B2B2B")
frame.pack(expand=True, padx=10, pady=10)
frame.pack_propagate(0)


# Create Buttons

btn1 = CTkButton(master=frame, text="2nd Mode", corner_radius=20, border_width=3, height=100, width=300,
                 font=("Courier", 28, "bold"), command=second_mode, fg_color="#1F6AA5", hover_color="#14487E",
                 border_color="#14487E", text_color="#FFFFFF")
btn2 = CTkButton(master=frame, text="3rd Mode", corner_radius=20, border_width=3, height=100, width=300,
                 font=("Courier", 28, "bold"), command=third_mode, fg_color="#1F6AA5", hover_color="#14487E",
                 border_color="#14487E", text_color="#FFFFFF")

# Create labels

label1 = CTkLabel(master=frame, textvariable=var1, font=("Courier", 16, "bold"), text_color="#FFFFFF", pady=20)
label2 = CTkLabel(master=frame, textvariable=var2, font=("Courier", 16, "bold"), text_color="#FFFFFF", pady=20)
label3 = CTkLabel(master=app, text="Quit Mode by pressing 'Q' button", font=("Courier", 18, "bold"),
                  text_color="#FFFFFF", pady=20)

# Packing

btn1.pack(pady=(60, 20))
label1.pack()
btn2.pack(pady=(20, 20))
label2.pack()
label3.pack(pady=(20, 20))

SSH_initialize()

app.mainloop()
