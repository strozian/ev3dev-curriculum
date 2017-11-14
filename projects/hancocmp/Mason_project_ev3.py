# CSSE 120 Final Project
#
# Mason Hancock


import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time
import robot_controller as robo


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    while True:
        robot.loop_forever()
        robot.draw_pac



main()
