"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
# import math
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()

        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor.connected
        assert self.touch_sensor

        self.running = True

    def drive_inches(self, inches_target, speed_deg_per_second):
        distance_degrees = inches_target * 360 / 4
        self.left_motor.run_to_rel_pos(speed_sp=speed_deg_per_second, position_sp=distance_degrees)
        self.right_motor.run_to_rel_pos(speed_sp=speed_deg_per_second, position_sp=distance_degrees)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action="brake")

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        distance = degrees_to_turn*5
        self.left_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=-distance)
        self.right_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=distance)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action="brake")

    def arm_calibration(self):
        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()
        arm_revolutions_for_full_range = 14.2
        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range*360)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()
        self.arm_motor.position = 0  # Calibrate the down position as 0 (this line is correct as is).

    def arm_up(self):
        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action='brake')
        ev3.Sound.beep().wait()

    def arm_down(self):
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=900)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes running
        ev3.Sound.beep().wait()

    def drive_forward(self, right_speed_entry, left_speed_entry):
        self.right_motor.run_forever(speed_sp=right_speed_entry)
        self.left_motor.run_forever(speed_sp=left_speed_entry)

    def drive_backward(self, right_speed_entry, left_speed_entry):
        self.right_motor.run_forever(speed_sp=-right_speed_entry)
        self.left_motor.run_forever(speed_sp=-left_speed_entry)

    def drive_right(self, right_speed_entry, left_speed_entry):
        self.right_motor.run_forever(speed_sp=right_speed_entry)
        self.left_motor.run_forever(speed_sp=-left_speed_entry)

    def drive_left(self, right_speed_entry, left_speed_entry):
        self.right_motor.run_forever(speed_sp=-right_speed_entry)
        self.left_motor.run_forever(speed_sp=left_speed_entry)

    def stop(self):
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')

    def shutdown(self):
        self.running = False
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action="brake")
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        ev3.Sound.speak('Goodbye').wait()

    def loop_forever(self):
        while self.running:
            time.sleep(.01)

