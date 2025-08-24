from gpiozero import TonalBuzzer
from time import sleep

tb = TonalBuzzer(17)  # or whichever GPIO you use (Signal pin)

# Dot
tb.play('A4')  # Pick a note; A4 is 440 Hz
sleep(0.1)
tb.stop()
sleep(0.1)

# Dash
tb.play('A4')
sleep(0.3)
tb.stop()
sleep(0.1)
