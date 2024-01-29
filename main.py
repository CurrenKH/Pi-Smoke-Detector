import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import os

# Button function
def buttonTrigger():
    
    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

    while True:
        inputValue = GPIO.input(40)
        if (inputValue == True):
            print("Alarm was triggered by high heat levels, which can lead to smoke in the facility!")
            print("Phone number will be called for further assistance soon.")
            print("--------------------------------------------------")
        time.sleep(0.5)
    GPIO.cleanup() # Clean up
    
# Buzzer function
def buzzTrigger():
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    BUZZER= 31
    buzzState = False

    GPIO.setup(BUZZER, GPIO.OUT)

    # Buzzer tone
    tone = GPIO.PWM(BUZZER, 500)

    while True:
        buzzState = not buzzState
        GPIO.output(BUZZER, buzzState)
        tone.start(50)
        time.sleep(1)

# Light function
def lightTrigger():
    
    GPIO.setwarnings(False)

    Led2= 7 # pin number

    GPIO.setmode(GPIO.BOARD) # Numbering according to the physical location
    GPIO.setup(Led2, GPIO.OUT) # Set pin mode as output
    GPIO.output(Led2, GPIO.HIGH) # Output high level(+3.3V) to off the led
        
    while True:
        GPIO.output(Led2, GPIO.LOW) # led on
        time.sleep(0.5)
        GPIO.output(Led2, GPIO.HIGH) # led off
        time.sleep(0.5)


