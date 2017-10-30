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

    def drive_inches(self, inches_target, speed_deg_per_second):
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        assert left_motor.connected
        assert right_motor.connected
        distance_degrees = inches_target * 360 / 4
        left_motor.run_to_rel_pos(speed_sp=speed_deg_per_second, position_sp=distance_degrees)
        right_motor.run_to_rel_pos(speed_sp=speed_deg_per_second, position_sp=distance_degrees)
        right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        left_motor.stop(stop_action='brake')
        right_motor.stop(stop_action="brake")

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        assert left_motor.connected
        assert right_motor.connected
        distance = degrees_to_turn*5
        left_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=-distance)
        right_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=distance)
        right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        left_motor.stop(stop_action='brake')
        right_motor.stop(stop_action="brake")

    def arm_calibration(self):
        arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        assert arm_motor.connected
        touch_sensor = ev3.TouchSensor()
        assert touch_sensor
        arm_motor.run_forever(speed_sp=900)
        while not touch_sensor.is_pressed:
            time.sleep(0.01)
        arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()
        arm_revolutions_for_full_range = 14.2
        arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range*360)
        arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()
        arm_motor.position = 0  # Calibrate the down position as 0 (this line is correct as is).

    def arm_up(self):
        arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        assert arm_motor.connected
        touch_sensor = ev3.TouchSensor()
        assert touch_sensor
        arm_motor.run_forever(speed_sp=900)
        while not touch_sensor.is_pressed:
            time.sleep(0.01)
        arm_motor.stop(stop_action='brake')
        ev3.Sound.beep().wait()

    def arm_down(self):
        arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        assert arm_motor.connected
        touch_sensor = ev3.TouchSensor()
        assert touch_sensor
        arm_motor.run_to_abs_pos(position_sp=0, speed_sp=900)
        arm_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes running
        ev3.Sound.beep().wait()

    def shutdown(self):
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        left_motor.stop(stop_action='brake')
        right_motor.stop(stop_action="brake")
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        ev3.Sound.speak('Goodbye').wait()