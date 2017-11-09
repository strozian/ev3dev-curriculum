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
    canvas.create_image(300, 200, image=photo)

    y_button = ttk.Checkbutton(main_frame, text='Yellow')
    y_button.grid(column=0, row=1)
    y_button['command'] = lambda: yellow(y_button)

    button = ttk.Checkbutton(main_frame, text='Red')
    button.grid(column=1, row=1)
    button['command'] = lambda: red(button)

    root.mainloop()


def yellow(button):
    state = button.instate(['selected'])
    print('Yellow', state)


def red(button):
    state = button.instate(['selected'])
    print('Red', state)


main()
