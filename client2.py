# Gui part of client
import time
import threading
import socket
from tkinter import *
from tkinter import scrolledtext

import psutil

host = '127.0.0.1'
port = 1230
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
print("Waiting for server to connect .. >>> ")
name = "Client"


def recv_txt():
    while True:
        print("Waiting for incoming texts, ")
        display.insert(INSERT, sock.recv(1024).decode('utf-8'))


def get_typed_text():
    print(typed_text.get(1.0, END))
    sock.sendall(typed_text.get(1.0, END).encode())
    typed_text.delete(1.0, END)


def clock():
    time_string = time.strftime("%H:%M:%S")
    time_.config(text=time_string)
    time_.after(100, clock)


def battery_life():
    while True:
        battery = psutil.sensors_battery()
        # plugged = battery.power_plugged
        percent = str(battery.percent)
        battery_st.config(text=f"Bat - {percent} %")
        time.sleep(10)


root = Tk()
root.geometry("450x250")
root.title("CLIENT GUI")
main_frame = Frame(root, bg='blue')
main_frame.place(rely=0.01, relx=0.01, relwidth=0.98, relheight=0.98)
coming_txt = Frame(main_frame, bg='Red')
display = scrolledtext.ScrolledText(coming_txt, bg="Gray")
typing_txt = Frame(main_frame, bg='Red')
typed_text = scrolledtext.ScrolledText(typing_txt, bg="Gray")
status_frame = Frame(root, bg="Gray")
address = Label(status_frame, bg="Yellow", text=name)
exit_b = Button(status_frame, bg="Yellow", text="EXIT", command=root.quit)
time_ = Label(status_frame, bg="Yellow", font=("times", 13, "bold"))
send_but = Button(root, bg='Yellow', text="SEND", command=get_typed_text)
battery_st = Label(status_frame, bg="Yellow", text="B - STS")

send_but.place(rely=0.87, relx=0.84, relwidth=0.12, relheight=0.09)
status_frame.place(rely=0.03, relx=0.029, relwidth=0.93, relheight=0.109)
address.place(rely=0.01, relx=0.28, relwidth=0.14, relheight=0.95)
battery_st.place(rely=0.01, relx=0.57, relwidth=0.14, relheight=0.95)
exit_b.place(rely=0.01, relx=0.90, relwidth=0.1, relheight=0.95)
time_.place(rely=0.01, relx=0.0009, relwidth=0.17, relheight=0.95)
coming_txt.place(rely=0.15, relx=0.02, relwidth=0.95, relheight=0.4)
display.place(rely=0.006, relx=0.004, relwidth=0.994, relheight=0.98)
typing_txt.place(rely=0.57, relx=0.02, relwidth=0.8, relheight=0.4)
typed_text.place(rely=0.01, relx=0.006, relwidth=0.99, relheight=0.98)
clock()
battery_thread = threading.Thread(target=battery_life, daemon=True)
battery_thread.start()
p1 = threading.Thread(target=recv_txt, daemon=True)
p1.start()
root.mainloop()

# run.recv_txt()
