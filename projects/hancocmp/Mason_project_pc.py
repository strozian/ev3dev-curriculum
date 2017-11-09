# CSSE 120 Final Project
#
# Mason Hancock
# Project will take in a color from the user in a tKinter GUI and will use the pixy cam to find that color.
# The robot will drive to that color and then return the location of that color to the tkinter GUI

import tkinter
from tkinter import ttk
from tkinter import *
import time

import mqtt_remote_method_calls as com
from PIL import Image, ImageTk


def main():
    print('------------------------------------------------------------')
    print('Main')
    print('------------------------------------------------------------')
    print('Use the arrow keys to move the robot, space to stop, and q to quit')

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title('Final Project')

    main_frame = ttk.Frame(root, padding=20)
    main_frame.grid()
    pac = PacMan()
    canvas = tkinter.Canvas(main_frame, background="lightgray", width=640, height=400)
    canvas.grid(columnspan=2)
    pac.sprite = canvas.create_image(pac.x, pac.y, image=pac.U)

    y_button = ttk.Checkbutton(main_frame, text='Yellow')
    y_button.grid(column=0, row=1)
    y_button['command'] = lambda: yellow(y_button)

    button = ttk.Checkbutton(main_frame, text='Red')
    button.grid(column=1, row=1)
    button['command'] = lambda: red(button)


# Robot drive commands:
    root.bind('<Up>', lambda event: drive_forward(mqtt_client, 600, 600, canvas, pac))
    root.bind('<Left>', lambda event: drive_left(mqtt_client, 600, 600, canvas, pac))
    root.bind('<space>', lambda event: stop(mqtt_client))
    root.bind('<Right>', lambda event: drive_right(mqtt_client, 600, 600, canvas, pac))
    root.bind('<Down>', lambda event: drive_backward(mqtt_client, 600, 600, canvas, pac))
    root.bind('<q>', lambda event: quit_program(mqtt_client, True))

    root.mainloop()


def drive_forward(mqtt_client, right_speed, left_speed, canvas, pac):
    if pac.direction == 'right':
        mqtt_client.send_message('turn_degrees', [90, 600])
        mqtt_client.send_message('drive_forward', [right_speed, left_speed])
    if pac.direction == 'left':
        mqtt_client.send_message('turn_degrees', [-90, 600])
        mqtt_client.send_message('drive_forward', [right_speed, left_speed])
    if pac.direction == 'down':
        mqtt_client.send_message('turn_degrees', [180, 600])
        mqtt_client.send_message('drive_forward', [right_speed, left_speed])
    pac.direction = 'up'
    canvas.delete(pac.sprite)
    pac.sprite = canvas.create_image(pac.x, pac.y, image=pac.U)


def drive_backward(mqtt_client, right_speed, left_speed, canvas, pac):
    if pac.direction == 'right':
        mqtt_client.send_message('turn_degrees', [-90, 600])
        mqtt_client.send_message('drive_forward', [right_speed, left_speed])
    if pac.direction == 'left':
        mqtt_client.send_message('turn_degrees', [90, 600])
        mqtt_client.send_message('drive_forward', [right_speed, left_speed])
    if pac.direction == 'up':
        mqtt_client.send_message('turn_degrees', [180, 600])
        mqtt_client.send_message('drive_forward', [right_speed, left_speed])
    pac.direction = 'down'
    canvas.delete(pac.sprite)
    pac.sprite = canvas.create_image(pac.x, pac.y, image=pac.D)


def drive_left(mqtt_client, right_speed, left_speed, canvas, pac):
    if pac.direction == 'right':
        mqtt_client.send_message('turn_degrees', [180, 600])
        mqtt_client.send_message('drive_forward', [right_speed, left_speed])
    if pac.direction == 'up':
        mqtt_client.send_message('turn_degrees', [90, 600])
        mqtt_client.send_message('drive_forward', [right_speed, left_speed])
    if pac.direction == 'down':
        mqtt_client.send_message('turn_degrees', [-90, 600])
        mqtt_client.send_message('drive_forward', [right_speed, left_speed])
    pac.direction = 'left'
    canvas.delete(pac.sprite)
    pac.sprite = canvas.create_image(pac.x, pac.y, image=pac.L)


def drive_right(mqtt_client, right_speed, left_speed, canvas, pac):
    if pac.direction == 'left':
        mqtt_client.send_message('turn_degrees', [180, 600])
        mqtt_client.send_message('drive_forward', [right_speed, left_speed])
    if pac.direction == 'up':
        mqtt_client.send_message('turn_degrees', [-90, 600])
        mqtt_client.send_message('drive_forward', [right_speed, left_speed])
    if pac.direction == 'down':
        mqtt_client.send_message('turn_degrees', [90, 600])
        mqtt_client.send_message('drive_forward', [right_speed, left_speed])
    pac.direction = 'right'
    canvas.delete(pac.sprite)
    pac.sprite = canvas.create_image(pac.x, pac.y, image=pac.R)


def stop(mqtt_client):
    mqtt_client.send_message('stop')


# Quit button callbacks
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


class PacMan(object):
    def __init__(self):
        image_r = Image.open("PacMan_R.gif")
        image_l = Image.open("PacMan_L.gif")
        image_u = Image.open("PacMan_U.gif")
        image_d = Image.open("PacMan_D.gif")

        self.R = ImageTk.PhotoImage(image_r)
        self.L = ImageTk.PhotoImage(image_l)
        self.U = ImageTk.PhotoImage(image_u)
        self.D = ImageTk.PhotoImage(image_d)
        self.direction = 'up'
        self.sprite = ''
        self.x = 320
        self.y = 200

main()
