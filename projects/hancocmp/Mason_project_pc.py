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
    print('Use the arrow keys to move the robot, space to stop, and q to quit')


# Creates a tkinter GUI
    root = tkinter.Tk()
    root.title('Final Project: Robot Pac-Man')

    main_frame = ttk.Frame(root, padding=20)
    main_frame.grid()

    canvas = tkinter.Canvas(main_frame, background="lightgray", width=640, height=400)
    canvas.grid(columnspan=2)

# Creates a Pac Man object using the tkinter canvas
    pac = PacMan(canvas)
    pac.sprite = pac.canvas.create_image(pac.x, pac.y, image=pac.U)
    pac.update_score()
    pac.mqtt_client.connect_to_ev3()

# Adds quit button to GUI
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=1,column=2)
    q_button['command'] = (lambda: quit_program(pac.mqtt_client, True))

# Robot drive commands and quit command:
    root.bind('<Up>', lambda event: drive_forward(pac.mqtt_client, 600, 600, pac))
    root.bind('<Left>', lambda event: drive_left(pac.mqtt_client, 600, 600, pac))
    root.bind('<space>', lambda event: stop(pac.mqtt_client, pac))
    root.bind('<Right>', lambda event: drive_right(pac.mqtt_client, 600, 600, pac))
    root.bind('<Down>', lambda event: drive_backward(pac.mqtt_client, 600, 600, pac))
    root.bind('<q>', lambda event: quit_program(pac.mqtt_client, True))

    root.mainloop()


# Drive commands that rotate the robot to the appropritate direction and drives forward
def drive_forward(mqtt_client, right_speed, left_speed, pac):
    if pac.direction == 'right':
        mqtt_client.send_message('turn_degrees', [90, 600])
        mqtt_client.send_message('drive_forward', [right_speed, left_speed])
    if pac.direction == 'left':
        mqtt_client.send_message('turn_degrees', [-90, 600])
        mqtt_client.send_message('drive_forward', [right_speed, left_speed])
    if pac.direction == 'down':
        mqtt_client.send_message('turn_degrees', [180, 600])
        mqtt_client.send_message('drive_forward', [right_speed, left_speed])
    if pac.direction == 'up':
        mqtt_client.send_message('drive_forward', [right_speed, left_speed])
    pac.direction = 'up'
    pac.canvas.delete(pac.sprite)
    pac.sprite = pac.canvas.create_image(pac.x, pac.y, image=pac.U)
    pac.playing = True


def drive_backward(mqtt_client, right_speed, left_speed, pac):
    if pac.direction == 'right':
        mqtt_client.send_message('turn_degrees', [-90, 600])
        mqtt_client.send_message('drive_forward', [right_speed, left_speed])
    if pac.direction == 'left':
        mqtt_client.send_message('turn_degrees', [90, 600])
        mqtt_client.send_message('drive_forward', [right_speed, left_speed])
    if pac.direction == 'up':
        mqtt_client.send_message('turn_degrees', [180, 600])
        mqtt_client.send_message('drive_forward', [right_speed, left_speed])
    if pac.direction == 'down':
        mqtt_client.send_message('drive_forward', [right_speed, left_speed])
    pac.direction = 'down'
    pac.canvas.delete(pac.sprite)
    pac.sprite = pac.canvas.create_image(pac.x, pac.y, image=pac.D)
    pac.playing = True


def drive_left(mqtt_client, right_speed, left_speed, pac):
    if pac.direction == 'right':
        mqtt_client.send_message('turn_degrees', [180, 600])
        mqtt_client.send_message('drive_forward', [right_speed, left_speed])
    if pac.direction == 'up':
        mqtt_client.send_message('turn_degrees', [90, 600])
        mqtt_client.send_message('drive_forward', [right_speed, left_speed])
    if pac.direction == 'down':
        mqtt_client.send_message('turn_degrees', [-90, 600])
        mqtt_client.send_message('drive_forward', [right_speed, left_speed])
    if pac.direction == 'left':
        mqtt_client.send_message('drive_forward', [right_speed, left_speed])
    pac.direction = 'left'
    pac.canvas.delete(pac.sprite)
    pac.sprite = pac.canvas.create_image(pac.x, pac.y, image=pac.L)
    pac.playing = True


def drive_right(mqtt_client, right_speed, left_speed, pac):
    if pac.direction == 'left':
        mqtt_client.send_message('turn_degrees', [180, 600])
        mqtt_client.send_message('drive_forward', [right_speed, left_speed])
    if pac.direction == 'up':
        mqtt_client.send_message('turn_degrees', [-90, 600])
        mqtt_client.send_message('drive_forward', [right_speed, left_speed])
    if pac.direction == 'down':
        mqtt_client.send_message('turn_degrees', [90, 600])
        mqtt_client.send_message('drive_forward', [right_speed, left_speed])
    if pac.direction == 'right':
        mqtt_client.send_message('drive_forward', [right_speed, left_speed])
    pac.direction = 'right'
    pac.canvas.delete(pac.sprite)
    pac.sprite = pac.canvas.create_image(pac.x, pac.y, image=pac.R)
    pac.playing = True


def stop(mqtt_client, pac):
    mqtt_client.send_message('stop')
    pac.direction = 'stop'
    pac.playing = False


# Quit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        mqtt_client.send_message("pac_stop")
    mqtt_client.close()
    exit()


# Game over function that puts game over image on canvas and shuts down the program on the robot
def game_over(pac):
    pac.canvas.delete(pac.sprite)
    pac.canvas.create_image(320, 200, image=pac.end)
    print('GAME OVER. YOUR FINAL SCORE IS: ', end='')
    print(pac.score)
    print('Press ''q'' to exit')
    pac.mqtt_client.send_message("pac_stop")
    pac.mqtt_client.close()


class PacMan(object):
    def __init__(self, canvas):
        image_r = Image.open("PacMan_R.gif")
        image_l = Image.open("PacMan_L.gif")
        image_u = Image.open("PacMan_U.gif")
        image_d = Image.open("PacMan_D.gif")
        image_end = Image.open("Game_Over.gif")

        self.running = True
        self.R = ImageTk.PhotoImage(image_r)
        self.L = ImageTk.PhotoImage(image_l)
        self.U = ImageTk.PhotoImage(image_u)
        self.D = ImageTk.PhotoImage(image_d)
        self.end = ImageTk.PhotoImage(image_end)
        self.direction = 'up'
        self.sprite = ''
        self.x = 320
        self.y = 200
        self.canvas = canvas
        self.power = False
        self.score_wait = False  # used to put a pause between score updates
        self.playing = True
        self.power_time = 0
        self.wait_time = 0
        self.score = 0
        self.label = ttk.Label(text='')
        self.mqtt_client = com.MqttClient(self)

# Draw method updates the canvas and draws the new pac man sprite
    def draw(self):
        if self.direction == 'right':
            self.x += 8
            self.canvas.delete(self.sprite)
            self.sprite = self.canvas.create_image(self.x, self.y, image=self.R)
        if self.direction == 'left':
            self.x += -8
            self.canvas.delete(self.sprite)
            self.sprite = self.canvas.create_image(self.x, self.y, image=self.L)
        if self.direction == 'up':
            self.y += -8
            self.canvas.delete(self.sprite)
            self.sprite = self.canvas.create_image(self.x, self.y, image=self.U)
        if self.direction == 'down':
            self.y += 8
            self.canvas.delete(self.sprite)
            self.sprite = self.canvas.create_image(self.x, self.y, image=self.D)

# update_score method updates the label on the Tkinter GUI with the new score
    def update_score(self):
        if self.playing:
            score_s = 'Score: ' + str(self.score)
            self.label.destroy()
            self.label = ttk.Label(text=score_s)
            self.label.grid(row=0, column=2)

# check_color method recieves a color from the robot and performs the appropriate
# actions for that color
    def check_color(self, color):
        print(color)
        if self.power:
            self.power_time += 0.5
        if self.power_time > 10:
            self.power = False
            self.power_time = 0

        if self.score_wait:
            self.wait_time += 0.5
        if self.wait_time > -1:
            self.wait_time = 0
            self.score_wait = False

#        #White will represent normal pellets worth 10 points each
        if color == 6:
            if not self.score_wait:
                self.score += 10
                self.update_score()
                self.score_wait = True

#       #Blue will represent the power pellets worth 50 points and allows Pac Man(the robot)
        #  to eat the ghosts for a short time(10 seconds)
        if color == 2:
            if not self.score_wait:
                self.score += 50
                self.power = True
                self.update_score()
                self.score_wait = True
                self.mqtt_client.send_message("beep")
#       # Red will represent the ghosts. Hitting a ghost while powered
        # up gives 200 points, if a ghost is hit while not powered up, it results in a game over.
        if color == 5:
            if not self.score_wait:
                if self.power:
                    self.score += 200
                    self.update_score()
                else:
                    game_over(self)
                self.score_wait = True

main()
