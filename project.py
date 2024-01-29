from tkinter import *
import RPi.GPIO as GPIO
import time
import sys
import os
import main
from multiprocessing import Process


class Application(Frame):
    def __init__ (self,master):
        super(Application, self).__init__(master)
        self.grid()
        self.create_widgets()
        
    # GUI elements
    def create_widgets(self):
        
        #Number Info Label
        self.numberInfo = Label (self, text='Number to contact Police/FD')
        self.numberInfo.grid(row=2, column=1, sticky=N)
    
        #Number Title Label
        self.contactNumber = Label (self, text='Contact Number:')
        self.contactNumber.grid(row=3, column=0, sticky=E)
        
        #Number TextBox
        self.contactNumberEntry = Entry (self, text='')
        self.contactNumberEntry.grid(row=3, column=1, sticky=W)
        
        #Timer Info Label
        self.timerInfo = Label (self, text='Timer until is number called')
        self.timerInfo.grid(row=4, column=1, sticky=N)
        
        #Timer Title Label
        self.countdownInfo = Label (self, text='Countdown (seconds):')
        self.countdownInfo.grid(row=5, column=0, sticky=E)
        
        #Timer TextBox
        self.timerEntry = Entry (self, text='')
        self.timerEntry.grid(row=5, column=1, sticky=W)
        
        #Heat Level Label
        self.heatInfo = Label (self, text='Alarm will trigger if past this')
        self.heatInfo.grid(row=6, column=1, sticky=N)
        
        #Heat Title Label
        self.levelInfo = Label (self, text='Set Heat Level Trigger:')
        self.levelInfo.grid(row=7, column=0, sticky=E)
        
        #Heat TextBox
        self.levelEntry = Entry (self, text='')
        self.levelEntry.grid(row=7, column=1, sticky=W)
        
        
        #Clear Button
        self.clear = Button (self, text='Clear', command=self.clear)
        self.clear.grid(row=8, column=1, sticky=W)
        
        #Close Button
        self.submit = Button (self, text='Close', command=self.close)
        self.submit.grid(row=9, column=1, sticky=W)
        
        #Enable Alarm Button
        self.submit = Button (self, text='Enable Alarm', command=self.script)
        self.submit.grid(row=8, column=1, sticky=E)
            
    def clear(self):
        #Clear TextBoxes
        self.contactNumberEntry.delete(0,END)
        self.timerEntry.delete(0,END)
        self.levelEntry.delete(0,END)
        
    def close(self):
        sys.exit()
    
    # Run alarm scripts if triggered
    def script(self):
        
        # Retrieve inputted values
        phoneNumber = self.contactNumberEntry.get()
        timer = int(self.timerEntry.get())
        heat = int(self.levelEntry.get())
        
        print("Your inputted contact number in case of emergency is:", phoneNumber)
        time.sleep(2)
        print("If alarm is triggered, the system will first count down the factory default")
        time.sleep(2)
        print("time of 15 seconds while the alarm plays, then will call the phone number after", timer, "seconds")
        time.sleep(8)
        print("--------------------------------------------------")
        print("--------------------------------------------------")
        
        
        GPIO.setmode (GPIO.BOARD)
        GPIO.setwarnings(True)

        pin1 = 24
        pin2 = 10

        enCount = 0

        GPIO.setup (pin1, GPIO.IN)
        GPIO.setup (pin2, GPIO.IN)

        # Values for rotary device to be read
        global rotationCount, startNum, allStates
        rotationCount = 0
        startNum = "00"
        allStates = {"0001":1,"0010":-1,"0100":-1,"0111":1,"1000":1,"1011":-1, "1101":-1, "1110":1}     
        
        # Rotary function
        def rotation(channel1):
            global enCount,rotationCount,startNum,allStates
            now = str(GPIO.input(24)) + str(GPIO.input(10))
            key = startNum + now
            if key in allStates:
                    direction = allStates[key]
                    startNum = now
                    rotationCount +=direction
            

        GPIO.add_event_detect (pin1, GPIO.BOTH, callback=rotation)  
        GPIO.add_event_detect (pin2, GPIO.BOTH, callback=rotation)
        
        alarmEnabled = False
                
        def alarm():
            # Process library used to execute multiple functions at once
            p1 = Process(target = main.buzzTrigger)
            p1.start()
            p2 = Process(target = main.lightTrigger)
            p2.start()
            p3 = Process(target = main.buttonTrigger)
            p3.start()
            # Alarm sounds for 15 seconds before countdown for phone number begins
            time.sleep(15)
            p1.terminate()
            p2.terminate()
            p3.terminate()
            p1.join()
            p2.join()
            p3.join()
            
        
    
        # Checking current heat level every half a second
        while(1):
            if (alarmEnabled == False):
                print ("Current Heat Level:", rotationCount)
                time.sleep(0.5)
        
            # If the heat level is higher than the user inputted value
            if (rotationCount > heat):
                
                print("----------------Alarm Triggered!!!----------------")
                print("User countdown will start after alarm sounds for 15 seconds (factory default)")
                print("Press the button on the module for more information")
                print("--------------------------------------------------")
                
                alarm()
                alarmEnabled = True
                
                # Countdown until number is called
                for i in reversed(range(1,timer + 1)):
                    print(i)
                    time.sleep(1)
                print("Dialing", phoneNumber, "...")
                time.sleep(5)
                print("...")
                time.sleep(2)
                print("...")
                time.sleep(2)
                print("...")
                time.sleep(2)
                print("Help is on its way!")
                break
            
                alarmEnabled = False
                
                    
            
        GPIO.cleanup()

        
root = Tk()
root.title('Smoke Alarm/Detector')
root.geometry('500x200')
app = Application(root)
app.mainloop()
