# CSSE 120 Final Project
#
# Mason Hancock


import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time
import robot_controller as robo


def main():
    robot = robo.Snatch3r()
    btn = ev3.Button()
    btn.on_backspace = lambda state: robot.pac_stop()

    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    while True:
        if robot.right_motor.is_running:
            break

    while robot.pac_running:
        mqtt_client.send_message("draw")
        color = robot.color_sensor.color
        mqtt_client.send_message("check_color", [color])
        time.sleep(0.5)
        btn.process()


main()
