import time

def executeRelay(shutdownSprinkler):
    error = None
    try:
        Relay_Ch1 = 26
        import RPi.GPIO as GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        try:
            GPIO.setup(Relay_Ch1,GPIO.OUT)
            print("Setup The Relay Module is [success]")
            if shutdownSprinkler:
                GPIO.output(Relay_Ch1,GPIO.LOW)
                print("Channel 1: Sending LOW signal to contact to OPEN the circuit...should override the sprinkler\n")
            else:
                GPIO.output(Relay_Ch1, GPIO.HIGH)
                print("Channel 1: Sending HIGH signal to contact to CLOSE the circuit...should allow sprinkler to function as normal!\n")
            result = True #only return true if executed.
        except:
            error = "exception setting relay"
            GPIO.cleanup()
    except:
        error = 'Could not load RPi.GPIO'
    return True if error is None else False, error

if __name__ == "__main__":
    print("Executing tests:")
    results, error = executeRelay(True)
    print("Turning off sprinkler: " + str(results) + ("." if results == True else " (" + error + ")"))
    print("Sleeping...")
    time.sleep(2.0)
    results, error = executeRelay(False)
    print("Turning on sprinkler: " + str(results) + ("." if results == True else " (" + error + ")"))
