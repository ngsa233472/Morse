import RPi.GPIO as GPIO
import time

BUZZER_PIN = 17  # change to the pin you connected Signal to

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

def beep(frequency, duration):
    pwm = GPIO.PWM(BUZZER_PIN, frequency)
    pwm.start(50)  # 50% duty cycle
    time.sleep(duration)
    pwm.stop()

# Example: play a Morse dot (high pitch short), dash (low pitch long)
beep(1000, 0.1)  # dot
beep(1000, 0.3)  # dash

GPIO.cleanup()
