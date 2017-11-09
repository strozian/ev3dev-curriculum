# CSSE 120 Final Project
#
# Mason Hancock
# Project will take in a color from the user in a tKinter GUI and will use the pixy cam to find that color.
# The robot will drive to that color and then return the location of that color to the tkinter GUI

import tkinter
from tkinter import ttk
from tkinter import *

import mqtt_remote_method_calls as com
from PIL import Image, ImageTk

def main():
    print('------------------------------------------------------------')
    print('Main')
    print('------------------------------------------------------------')
    x=320
    y=200
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title('Final Project')

    main_frame = ttk.Frame(root, padding=20)
    main_frame.grid()

    image = Image.open("PacMan_R.gif")
    photo = ImageTk.PhotoImage(image)
    # label = Label(image=photo)
    # label.image = photo  # keep a reference!
    # label.grid()
    canvas = tkinter.Canvas(main_frame, background="lightgray", width=640, height=400)
    canvas.grid(columnspan=2)
    canvas.create_image(x, y, image=photo)

    y_button = ttk.Checkbutton(main_frame, text='Yellow')
    y_button.grid(column=0, row=1)
    y_button['command'] = lambda: yellow(y_button)

    button = ttk.Checkbutton(main_frame, text='Red')
    button.grid(column=1, row=1)
    button['command'] = lambda: red(button)

    root.mainloop()

# Robot drive commands:
    root.bind('<Up>', lambda event: drive_forward(mqtt_client, 600, 600))
    root.bind('<Left>', lambda event: drive_left(mqtt_client, 600, 600))
    root.bind('<space>', lambda event: stop(mqtt_client))
    root.bind('<Right>', lambda event: drive_right(mqtt_client, 600, 600))
    root.bind('<Down>', lambda event: drive_backward(mqtt_client, 600, 600))
    root.bind('<u>', lambda event: send_up(mqtt_client))
    root.bind('<j>', lambda event: send_down(mqtt_client))

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))


def drive_forward(mqtt_client, right_speed, left_speed):
    mqtt_client.send_message('drive_forward', [right_speed, left_speed])


def drive_backward(mqtt_client, right_speed, left_speed):
    mqtt_client.send_message('drive_backward', [right_speed, left_speed])


def drive_left(mqtt_client, right_speed, left_speed):
    mqtt_client.send_message('drive_left', [right_speed, left_speed])


def drive_right(mqtt_client, right_speed, left_speed):
    mqtt_client.send_message('drive_right', [right_speed, left_speed])


def stop(mqtt_client):
    mqtt_client.send_message('stop')


# Arm command callbacks
def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")


# Quit and Exit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


def yellow(button):
    state = button.instate(['selected'])
    print('Yellow', state)


def red(button):
    state = button.instate(['selected'])
    print('Red', state)




main()
