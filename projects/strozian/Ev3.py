import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time

ev3.Sound.speak('Find the color')


class MyDelegate(object):
    def __init__(self):
        self.robot = robo.Snatch3r()
        self.list_of_colors = ['blue', 'red', 'green', 'orange', 'purple']
        self.seeking_color = None
        self.test = False


    def seek_color(self):
        w = self.robot.pixy.value(3)
        while self.test:

            self.robot.drive_left(200, 200)
            if w > 5:
                self.robot.stop()

            while w > 5:
                self.robot.stop()
                ev3.Sound.speak(self.seeking_color).wait()
                time.sleep(.01)
                break

            w = self.robot.pixy.value(3)
            while w > 5:
                w = self.robot.pixy.value(3)
                x = self.robot.pixy.value(1)
                h = self.robot.pixy.value(4)
                print(w)
                print(x)
                print('This is h', h)

                if w > 5:

                    if x < 150:
                        self.robot.drive_left(100, 100)
                        time.sleep(.01)

                    if x > 170:
                        self.robot.drive_right(100, 100)
                        time.sleep(.01)

                    if x > 150:
                        if x < 170:
                            self.robot.stop()
                            self.robot.drive_forward(400, 400)
                            time.sleep(.5)
                            self.robot.stop()

                    if w > 55 and w != 255:
                        self.robot.stop()
                        time.sleep(.01)
                        self.robot.arm_up()
                        ev3.Sound.speak('I found it').wait()
                        self.test = False
                        break

    def drive_to_color(self):
        while self.test:
            w = self.robot.pixy.value(3)
            self.robot.drive_left(200, 200)

            if w > 5:
                self.robot.stop()

            while w > 5:
                self.robot.stop()
                ev3.Sound.speak(self.seeking_color).wait()
                time.sleep(.01)
                break

            w = self.robot.pixy.value(3)
            while w > 5:
                w = self.robot.pixy.value(3)
                x = self.robot.pixy.value(1)
                h = self.robot.pixy.value(4)
                print(w)
                print(x)
                print('This is h', h)

                if w > 5:

                    if x < 150:
                        self.robot.drive_left(100, 100)
                        time.sleep(.01)

                    if x > 170:
                        self.robot.drive_right(100, 100)
                        time.sleep(.01)

                    if x > 150:
                        if x < 170:
                            self.robot.stop()
                            self.robot.drive_forward(400, 400)
                            time.sleep(.5)
                            self.robot.stop()

                    if w > 80 and w != 255:
                        self.robot.stop()
                        time.sleep(.01)
                        self.robot.arm_down()
                        ev3.Sound.speak('Payload delivered')
                        self.test = False
                        break

    def choose_pixy_mode(self, color_to_get):
        test = False
        for i in range(len(self.list_of_colors)):
            if color_to_get == self.list_of_colors[i]:
                s = i+1
                self.robot.pixy.mode = "SIG" + str(s)
                print(self.robot.pixy.mode)
                self.seeking_color = str(self.list_of_colors[i])
                ev3.Sound.speak(str(self.robot.pixy.mode)).wait()
                time.sleep(.01)
                self.test = True
                test = True
                self.seek_color()
        if test is False:
            ev3.Sound.speak("Incorrect Input")
            print('Incorrect input')

    def pixy_mode_for_drive(self, color_to_drive_to):
        test = False
        for i in range(len(self.list_of_colors)):
            if color_to_drive_to == self.list_of_colors[i]:
                s = i + 1
                self.robot.pixy.mode = "SIG" + str(s)
                print(self.robot.pixy.mode)
                self.seeking_color = str(self.list_of_colors[i])
                time.sleep(.01)
                ev3.Sound.speak(str(self.robot.pixy.mode)).wait()
                time.sleep(.01)
                self.test = True
                test = True
                self.drive_to_color()

        if test is False:
            ev3.Sound.speak("Incorrect Input")
            print('Incorrect input')

    def drive_right(self, right_speed, left_speed):
        self.robot.drive_right(right_speed, left_speed)

    def drive_backward(self, right_speed, left_speed):
        self.robot.drive_backward(right_speed, left_speed)

    def drive_left(self, right_speed, left_speed):
        self.robot.drive_left(right_speed, left_speed)

    def drive_forward(self, right_speed, left_speed):
        self.robot.drive_forward(right_speed, left_speed)

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

main()
