import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time

ev3.Sound.speak('Find the color')

class MyDelegate(object):
    def __init__(self):
        self.robot = robo.Snatch3r()
        self.list_of_colors = ['blue', 'red', 'green', 'yellow', 'orange']
        self.seeking_color = None
        self.test = False

    def seek_color(self):

        x = self.robot.pixy.value(1)
        y = self.robot.pixy.value(2)
        w = self.robot.pixy.value(3)
        h = self.robot.pixy.value(4)
        if w > 5:
            self.robot.stop()
            ev3.Sound.speak(self.seeking_color).wait()
            time.sleep(.01)
        while self.test:
            if w > 5:
                print(w)
                if x < 150:
                    self.robot.drive_left(100, 100)
                if x > 170:
                    self.robot.drive_right(100, 100)
                if x > 150:
                    if self.robot.pixy.value(1) < 170:
                        self.robot.stop()



    def choose_pixy_mode(self, color_to_get):

        for i in range(len(self.list_of_colors)):
            if color_to_get == self.list_of_colors[i]:
                s = i+1
                self.robot.pixy.mode = "SIG" + str(s)
                print(self.robot.pixy.mode)
                self.seeking_color = str(self.list_of_colors[i])
                ev3.Sound.speak('SIG').wait()
                ev3.Sound.speak(str(s)).wait()
                self.test = True
                self.seek_color()

        if self.test is False:
            ev3.Sound.speak("Incorrect Input")
            print('Incorrect input')



    def drive_right(self, right_speed, left_speed):
        self.robot.drive_right(right_speed, left_speed)

    def drive_backward(self, right_speed, left_speed):
        self.robot.drive_backward(right_speed,left_speed)

    def drive_left(self, right_speed, left_speed):
        self.robot.drive_left(right_speed,left_speed)

    def drive_forward(self, right_speed, left_speed):
        self.robot.drive_forward(right_speed,left_speed)

    def stop(self):
        self.robot.stop()

    def shutdown(self):
        ev3.Sound.speak('Shutting Down')
        self.test = False
        self.robot.shutdown()


    def arm_up(self):
        self.robot.arm_up()

    def arm_down(self):
        self.robot.arm_down()



def main():
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()
    my_delegate.robot.loop_forever()


    # while True:
        # width = robot.pixy.value(3)
        # x = robot.pixy.value(1)
        # y = robot.pixy.value(2)
        # if width > 10:
        #     ev3.Sound.speak('I found the color').wait()
        #     robot.drive_forward()
        # time.sleep(1)
        # if width > 300:
        #     break


    print("Goodbye!")



main()

