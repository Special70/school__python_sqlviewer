import time, sys

def exiting (num):
    if num == 1:
        print("Thank you for using the program. Exiting...")
        time.sleep(2.5)
        sys.exit()
    else:
        print("Returning to Previous Menu...")
        time.sleep(2.5)