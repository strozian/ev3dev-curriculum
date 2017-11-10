

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


def main():
    find_and_go_to_color()


def find_and_go_to_color():
    left_speed = 600
    right_speed = 600
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()
    root = tkinter.Tk()
    root.title("MQTT Remote")
    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()
    color_label = ttk.Label(main_frame, text="Color you want")
    color_label.grid(row=0, column=0)
    color_label_entry = ttk.Entry(main_frame, width=8)
    color_label_entry.grid(row=1, column=0)
    color_button = ttk.Button(main_frame, text="Enter Color")
    color_button.grid(row=2, column=0)
    color_button['command'] = lambda: seek_color(mqtt_client, color_label_entry)
    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    forward_button['command'] = lambda: drive_forward(mqtt_client, right_speed,
                                                      left_speed)
    root.bind('<Up>',
              lambda event: drive_forward(mqtt_client, right_speed, left_speed))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)

    left_button['command'] = lambda: drive_left(mqtt_client, right_speed, left_speed)
    root.bind('<Left>',
              lambda event: drive_left(mqtt_client, right_speed, left_speed))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    stop_button['command'] = lambda: stop(mqtt_client)
    root.bind('<space>', lambda event: stop(mqtt_client))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    right_button['command'] = lambda: drive_right(mqtt_client, right_speed, left_speed)
    root.bind('<Right>',
              lambda event: drive_right(mqtt_client, right_speed, left_speed))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    back_button['command'] = lambda: drive_backward(mqtt_client, right_speed, left_speed)
    root.bind('<Down>',
              lambda event: drive_backward(mqtt_client, right_speed, left_speed))

    up_button = ttk.Button(main_frame, text="Grab")
    up_button.grid(row=5, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<q>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Lower")
    down_button.grid(row=6, column=0)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<w>', lambda event: send_down(mqtt_client))

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
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
    mqtt_client.send_message('drive_left', [right_speed, left_speed])


def drive_right(mqtt_client, right_speed, left_speed):
    print('drive_right')
    mqtt_client.send_message('drive_right', [right_speed, left_speed])


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

def seek_color(mqtt_client,color):
        print("finding color")
        mqtt_client.send_message('choose_pixy_mode',[color.get()])

main()
