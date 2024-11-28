import tkinter
from customtkinter import *
import subprocess
from time import sleep
import threading
import os
import schedule
import threading
from tkvideo import tkvideo
from PIL import Image, ImageTk


phone_number = ''
run_maps_script = False


def raise_above_all(app):
    # program window to stay above all other windows
    app.attributes('-topmost', 1)
    app.attributes('-topmost', 0)


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


def var3_set(text):
    var3.set(f"{text}")
    app.update()


def var4_set(text):
    var4.set(f"{text}")
    app.update()


def ssh_initialize():
    # making sure that ssh connection is established before running any script
    os.startfile(
        "C:\\Users\\youse\\Desktop\\Eyes-Position-Estimator-Mediapipe-master\\Eye_Tracking_part4\\SSH_initialize.bat")


def second_mode():
    var1_set("Connection is being established.. ")
    thread1 = threading.Thread(target=run_batch_file, args=(
        r'C:\Users\youse\Desktop\Eyes-Position-Estimator-Mediapipe-master\Eye_Tracking_part4\test2run.bat',))
    thread1.start()
    sleep(10)
    thread2 = threading.Thread(target=run_batch_file, args=(
        r'C:\Users\youse\Desktop\Eyes-Position-Estimator-Mediapipe-master\Eye_Tracking_part4\hardwarePWMservo.bat',))
    thread2.start()
    var1_set("Connected!")
    thread1.join()
    thread2.join()
    var1_set("Mode OFF")


def third_mode():
    var2_set("Connection is being established.. ")
    thread1 = threading.Thread(target=run_batch_file, args=(
        r'C:\Users\youse\Desktop\Eyes-Position-Estimator-Mediapipe-master\Eye_Tracking_part4\main_M3run.bat',))
    thread1.start()
    sleep(10)
    #  due to an issue with timing between YOLO and the socket connection
    #  (using OS.startfile instead of another thread)
    os.startfile(
        "C:\\Users\\youse\\Desktop\\Eyes-Position-Estimator-Mediapipe-master\\Eye_Tracking_part4\\hardwarePWMservo.bat")
    var2_set("Connected!")
    thread1.join()
    var2_set("Mode OFF")


def send_location():
    thread1 = threading.Thread(target=run_batch_file, args=(
        r'C:\Users\youse\Desktop\Eyes-Position-Estimator-Mediapipe-master\Eye_Tracking_part4\OpenMaps.bat',))
    thread1.start()
    thread1.join()
    var4_set("sending location ...")


def get_phone_number():
    global phone_number
    global run_maps_script

    run_maps_script = False
    try:
        if data_entry.get():  # if there is an input
            try:
                if int(data_entry.get()):  # Check if the number has any letters
                    if len(data_entry.get()) == 11:  # Check if the number consists of 11 numbers
                        if data_entry.get()[:2] == "01":  # Check if the first two numbers are 0 and 1
                            phone_number = data_entry.get()  # Finally take the phone number
                            var4_set("Number accepted !")
                            run_maps_script = True
                        else:
                            var4_set("Thats not a valid number !")
                            run_maps_script = False
                    else:
                        var4_set("Have to be 11 numbers !")
                        run_maps_script = False
            except:
                var4_set("Only numbers !")
                run_maps_script = False
        else:
            var4_set("No phone number entered !")
            run_maps_script = False
    except:
        pass
    if run_maps_script:
        # first time to run the script is kept in a variable
        os.environ["VALUE_TO_PASS"] = phone_number  # Set an environment variable with the value of the number
        # Run OpenMaps.py with the environment variable
        subprocess.run(["python", "OpenMaps.py"], env=os.environ)
        raise_above_all(app)
    else:
        pass

def run_scheduler():
    while True:
        schedule.run_pending()
        sleep(1)
def scheduler_thread():
    # Schedule the job every 30 minutes
    schedule.every(3).minutes.do(get_phone_number)
    # Run the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

# ========== GUI ===========

background_img = CTkImage(light_image=Image.open("background.png"),
                          dark_image=Image.open("background.png"), size=(1075, 756))
check_mark_img = CTkImage(light_image=Image.open("check-mark.png"),
                          dark_image=Image.open("check-mark.png"), size=(20, 20))
eyetracker_img = CTkImage(light_image=Image.open("eyetracker.png"),
                          dark_image=Image.open("eyetracker.png"), size=(50, 50))
walking_img = CTkImage(light_image=Image.open("walking.png"),
                          dark_image=Image.open("walking.png"), size=(50, 50))

# Create main window

app = CTk()
app.geometry("1024x720")
app.title("Mode Switch")
# set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
set_appearance_mode("system")  # light or dark depending on your system
# set_default_color_theme("MoonlitSky.json")
app.resizable(False, False)

var1 = tkinter.StringVar()
var2 = tkinter.StringVar()
var3 = tkinter.StringVar()
var4 = tkinter.StringVar()
var1.set("Mode OFF")
var2.set("Mode OFF")
var3.set('Enter the phone number :')
var4.set("")


# Create frame

# frame = CTkFrame(master=app, width=1024, height=680, corner_radius=40, border_width=6)
# frame.grid()
# frame.grid_propagate(0)


# Create background
bg_label = CTkLabel(master=app, image=background_img, text="")
bg_label.grid(column=0, row=0, columnspan=4, pady=0, rowspan=4, padx=0)

# player = tkvideo("livebackground.mp4", bg_label, loop=1)
# player.play()
# bg_label.grid()

# Create Buttons

# btn1 = CTkButton(master=frame, text="2nd Mode", corner_radius=20, fg_color="#008DDA", hover_color="#ACE2E1",
#                  border_width=3, border_color="#41C9E2", height=100, width=200, font=("Courier", 28, "bold"), text_color="#F7EEDD", command=second_mode)

btn1 = CTkButton(master=app, text="2nd Mode", corner_radius=20,
                 border_width=3, height=100, width=200, font=("Courier", 32, "bold"), command=second_mode,
                 image=eyetracker_img, compound='top', bg_color='#ffffff', fg_color="#8389ac", hover_color="#b4bcec",
                 border_color="#53576f")
btn2 = CTkButton(master=app, text="3rd Mode", corner_radius=20,
                 border_width=3, height=100, width=200, font=("Courier", 32, "bold"), command=third_mode,
                 image=walking_img, compound='top', bg_color='#ffffff', fg_color="#8389ac", hover_color="#b4bcec",
                 border_color="#53576f")
btn3 = CTkButton(master=app, text="", corner_radius=200,
                 border_width=3, height=30, width=82, font=("Courier", 32, "bold"), command=get_phone_number,
                 image=check_mark_img, compound='top', bg_color='#ffffff', fg_color="#8389ac", hover_color="#b4bcec",
                 border_color="#53576f")

# Create Entries
data_entry = CTkEntry(master=app, width=400, font=("Courier", 15, "bold"),
                      text_color="#ffffff", corner_radius=200, bg_color="#ffffff", placeholder_text_color="#b4bcec",
                      border_color="#53576f", fg_color="#b4bcec")
# Create labels

label1 = CTkLabel(master=app, textvariable=var1, font=("Courier", 16, "bold"), text_color='#000000', bg_color='#ffffff')
label2 = CTkLabel(master=app, textvariable=var2, font=("Courier", 16, "bold"), text_color='#000000', bg_color='#ffffff')
label3 = CTkLabel(master=app, text="Quit Mode by pressing 'Q' button", font=("Courier", 18, "bold"),
                  text_color='#000000', bg_color='#ffffff')
label4 = CTkLabel(master=app, textvariable=var3, font=("Courier", 24, "bold"), text_color='#000000', bg_color='#ffffff')
label5 = CTkLabel(master=app, textvariable=var4, font=("Courier", 18, "bold"), text_color='#000000', bg_color='#ffffff')


# Grid
btn1.grid(column=0, row=1, columnspan=1, rowspan=2, pady=10, padx=0)
label1.grid(column=0, row=2, columnspan=1, rowspan=1, pady=0, padx=0)

btn2.grid(column=1, row=1, columnspan=1, pady=10, rowspan=2, padx=0)
label2.grid(column=1, row=2, columnspan=1, pady=0, rowspan=1, padx=0)

label4.grid(column=0, row=0, columnspan=2, pady=0, rowspan=2, padx=340)
data_entry.grid(column=0, row=1, columnspan=2, pady=0, rowspan=1, padx=0)
label5.grid(column=0, row=2, columnspan=2, pady=0, rowspan=1, padx=0)

btn3.grid(column=1, row=1, columnspan=2, pady=20, rowspan=1, padx=250, sticky='e')

label3.grid(column=0, row=4, columnspan=2, pady=0, rowspan=1, padx=0)



ssh_initialize()
# app.after(20000, get_phone_number)  # sends location every X milliseconds
# if run_maps_script:
#     scheduler_thread()
app.mainloop()

