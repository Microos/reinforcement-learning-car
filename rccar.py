"""
This class controls the RC car itself. It's intended to be the real-world
version of the carmunk simulation.
"""
import RPi.GPIO as GPIO
import time
import random
import numpy as np

# Constants
LEFT_PIN = 13
RIGHT_PIN = 15
FORWARD_PIN = 12
BACKWARD_PIN = 11
ITER_PAUSE = 1  # Time to pause between actions for observation.
MOVE_DURATION = 0.15  # Time to apply forward/backward force.
STEERING_DELAY = 0.5  # Time to wait after we move before straightening.

class RCCar:
    def __init__(self):
        print("Setting up GPIO pins.")
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(BACKWARD_PIN, GPIO.OUT)  # Backwards.
        GPIO.setup(FORWARD_PIN, GPIO.OUT)  # Forwards.
        GPIO.setup(LEFT_PIN, GPIO.OUT)  # Left.
        GPIO.setup(RIGHT_PIN, GPIO.OUT)  # Right.

        # Just to make sure.
        GPIO.output(BACKWARD_PIN, 0)
        GPIO.output(FORWARD_PIN, 0)
        GPIO.output(LEFT_PIN, 0)
        GPIO.output(RIGHT_PIN, 0)

    def step(self, action):
        self.perform_action(action)

        # Now that we've moved, check/recover if crashed.
        while self.car_is_crashed(self.get_readings()):
            self.recover()

    def cleanup_gpio(self):
        print("Cleaning up GPIO pins.")
        GPIO.cleanup()

    def get_readings(self):
        """
        TODO!
        """
        readings = []
        for i in range(3):
            readings.append(random.randint(4, 14))
        print(readings)
        return np.array([readings])

    def recover(self):
        # Back up and turn to the left to try to get away from the obstacle.
        for i in range(4):
            self.perform_action(0, True)

    def perform_action(self, action, reverse=False):
        print("Performing an action: %d" % action)
        if action == 0:  # Turn left.
            GPIO.output(LEFT_PIN, 1)
        elif action == 2:  # Turn right.
            GPIO.output(RIGHT_PIN, 1)

        # Now that the wheel is turned (or not), move a bit.
        if reverse:
            GPIO.output(BACKWARD_PIN, 1)
        else:
            GPIO.output(FORWARD_PIN, 1)

        # Pause...
        time.sleep(MOVE_DURATION)

        # Now turn off the power.
        GPIO.output(BACKWARD_PIN, 0)
        GPIO.output(FORWARD_PIN, 0)

        # Wait a bit longer before turning off the direction.
        time.sleep(STEERING_DELAY)
        GPIO.output(LEFT_PIN, 0)
        GPIO.output(RIGHT_PIN, 0)

        # Pause just to see what's going on.
        time.sleep(ITER_PAUSE)

    def car_is_crashed(self, readings):
        return False  # Debug.
        # If any of the readings show less than 5cm, we're crashed.
        for reading in readings[0]:
            if reading < 5:
                return True
        return False


if __name__ == '__main__':
    pass