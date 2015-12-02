import sys
import datetime
import serial
import threading
import time

baudrate = 115200
quitflag = False

class Thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()
        
if(len(sys.argv) == 1):
    print "Usage: python cli_batt_charger.py /dev/tty[NAME]"
    print "       ========================================="
    sys.exit()

print "====================================="
print " CLI - battery charger frdm board   "
print "====================================="


portname = str(sys.argv[1])    
print("Connecting to port " + portname+" ...")
ser = serial.Serial(portname, baudrate, timeout=1)

if(ser.isOpen()):
    quit_flag = False
    cmd = 0
    print("Port opened - OK")
else:
    print("Error opening port")
    sys.exit()
###############################
OPTION1="1"
OPTION2="2"
OPTION3="3"
QUIT="q"

menu = {
OPTION1: "do 1",
OPTION2: "do 2",
OPTION3: "do 3",
QUIT: "quit",
}
###############################
def print_menu():
    for item in menu:
        print item,
        print ") ",
        print menu[item]

def read_keyboard():
    global quitflag
    while (quitflag == False):
        print_menu()
        user_input= raw_input('Select option :')
        if (user_input == ""):
            continue
        elif (user_input[0] == QUIT):
            quitflag = True
        else:
            continue
        
def read_serial():
    global quitflag
    print "read_serial"
    while (quitflag == False):
        line = ser.readline()
        if( line == ""):
            continue
        else:
            print line

def write_serial():
    global quitflag
    print "write_serial"
    while (quitflag == False):
        #ser.write("serial_data_sent\n")
        time.sleep(1)
        
    



thread = Thread(read_keyboard)
thread = Thread(read_serial)
thread = Thread(write_serial)
