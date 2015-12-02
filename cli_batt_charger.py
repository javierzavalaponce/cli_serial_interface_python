import sys
import datetime
import serial
import threading
import time
import Queue 
import datetime
baudrate = 115200
quitflag = False

###############################
#  create a global queue to
#  process users requests
###############################
q = Queue.Queue()
###############################
#  options for user 
#  (add options here)
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
#  init
###############################
class Thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()

if(len(sys.argv) == 1):
    print "Usage: python cli_batt_charger.py /dev/tty[NAME]"
    print "       you might need to change permissions to access the port, hint: chmod "
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

def print_menu():
    print "====================================="
    for item in menu:
        print item,
        print ") ",
        print menu[item]
    print "Select option: "
    


###############################
#  thread to read user requests
#  program will loop here until
#  option QUIT is selected
###############################  
def read_keyboard():
    global quitflag
    while (quitflag == False):
        print_menu()
        user_input= raw_input()
        if (user_input == ""):
            continue
        #read only first character typed by user
        if user_input[0] in menu:
            print menu[user_input[0]]
            if (user_input[0] != QUIT):
                q.put(user_input[0])
            else:
                quitflag = True
        else:
            print "====================================="
            print("invalid input")
            continue

###############################
#  thread to read serial port
###############################        
def read_serial():
    global quitflag
    while (quitflag == False):
        data_read_from_serial_port = ser.readline()
        if( data_read_from_serial_port == ""):
            continue
        else:
            date = datetime.datetime.now()
            day=str(date.day).rjust(2,'0')
            month=str(date.month).rjust(2,'0')
            year=str(date.year)
            hour=str(date.hour).rjust(2,'0')
            minute=str(date.minute).rjust(2,'0')
            second=str(date.second).rjust(2,'0')
            log_time=month+day+year+"_"+hour+minute+second
            print "["+log_time+"]"+" : "+data_read_from_serial_port

###############################
#  thread to write to serial
###############################        
def write_serial():
    global quitflag
    while (quitflag == False):
        if q.empty() == False:
            data = q.get()
            ser.write(data+"\n")
        #time.sleep(1)
        
###############################
#  create threads
###############################        
thread = Thread(read_keyboard)
thread = Thread(read_serial)
thread = Thread(write_serial)
