

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com

from tkinter import *


def main():
    find_and_go_to_color()


def find_and_go_to_color():
    left_speed = 600
    right_speed = 600
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=60, relief='raised')
    main_frame.grid()

    other_color_label_entry1 = ttk.Entry(main_frame, width=8)
    other_color_label_entry1.grid(row=1, column=4)
    other_color_button = ttk.Button(main_frame, text='Enter Other Color')
    other_color_button.grid(row=2, column=4)
    other_color_button['command'] = lambda: drive_to_color(mqtt_client, other_color_label_entry1)

    color_label_entry = ttk.Entry(main_frame, width=8)
    color_label_entry.grid(row=1, column=0)
    color_button = ttk.Button(main_frame, text="Enter Color")
    color_button.grid(row=2, column=0)
    color_button['command'] = lambda: seek_color(mqtt_client, color_label_entry)

    label_color = Message(main_frame, text='Choose this entry box to pick up a color', justify=CENTER)
    label_color.grid(row=0, column=0)

    label_color_other = Message(main_frame, text='Choose this entry box to drive to a \n color', justify=CENTER)
    label_color_other.grid(row=0, column=4)

    info_label = Message(main_frame, text='Be careful to only enter colors on the Pixy Camera', justify=CENTER)
    info_label.grid(row=0, column=2)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=2)
    forward_button['command'] = lambda: drive_forward(mqtt_client, right_speed,
                                                      left_speed)
    root.bind('<Up>',
              lambda event: drive_forward(mqtt_client, right_speed, left_speed))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=1)

    left_button['command'] = lambda: drive_left(mqtt_client, right_speed, left_speed)
    root.bind('<Left>',
              lambda event: drive_left(mqtt_client, right_speed, left_speed))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=2)
    stop_button['command'] = lambda: stop(mqtt_client)
    root.bind('<space>', lambda event: stop(mqtt_client))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=3)
    right_button['command'] = lambda: drive_right(mqtt_client, right_speed, left_speed)
    root.bind('<Right>',
              lambda event: drive_right(mqtt_client, right_speed, left_speed))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=2)
    back_button['command'] = lambda: drive_backward(mqtt_client, right_speed, left_speed)
    root.bind('<Down>',
              lambda event: drive_backward(mqtt_client, right_speed, left_speed))

    up_button = ttk.Button(main_frame, text="Grab")
    up_button.grid(row=5, column=1)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<q>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Lower")
    down_button.grid(row=6, column=1)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<w>', lambda event: send_down(mqtt_client))

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=3)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=3)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    root.mainloop()


def drive_forward(mqtt_client, right_speed, left_speed):
    print('drive_forward')
    mqtt_client.send_message('drive_forward', [right_speed, left_speed])


def drive_backward(mqtt_client, right_speed, left_speed):
    print('drive_backward')
    mqtt_client.send_message('drive_backward', [right_speed, left_speed])


def drive_left(mqtt_client, right_speed, left_speed):
    print('drive_left')
    mqtt_client.send_message('drive_left', [right_speed-200, left_speed-200])


def drive_right(mqtt_client, right_speed, left_speed):
    print('drive_right')
    mqtt_client.send_message('drive_right', [right_speed-200, left_speed-200])


def stop(mqtt_client):
    print('stop')
    mqtt_client.send_message('stop')


def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")


def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


def seek_color(mqtt_client, color):
        print("finding color")
        mqtt_client.send_message('choose_pixy_mode', [color.get()])


def drive_to_color(mqtt_client, other_color_entry1):
        print('driving to color')
        mqtt_client.send_message('pixy_mode_for_drive', [other_color_entry1.get()])
main()
