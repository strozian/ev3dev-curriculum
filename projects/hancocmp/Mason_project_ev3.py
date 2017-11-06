# CSSE 120 Final Project
#
# Mason Hancock



import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time


def main():
    ev3.Sound.beep().wait()
    print('Main')


main()
