from __future__ import print_function
import threading, time, signal
from datetime import timedelta
from datetime import datetime
from io import open
import sys
import os
import json
sys.path.append("zk")
from zk import ZK, const
file_name = '/home/pi/MagicMirror/modules/MMM-Attend/new_attend.txt'    #previous latest attendance
file_exist = os.path.isfile(file_name)
conn = None
zk = ZK('192.168.1.201', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False) #connect with the zk terminal
cur_data = 0
wait_time = 10

class ProgramKilled(Exception):
    pass

def foo():
    def staff_name(staff_id):
        if staff_id == 1000:
            Sname = "Test1"
        elif staff_id == 1001:
            Sname = "Test2"
        else:
            Sname = "New staff, please register"
        return Sname

    try:
        #print ('Connecting to device...')
        conn = zk.connect()
        #print ('Disabling device...')
        attend = conn.get_attendance()
        data = len(attend) #get total number of attendance
        #print (data)
        
        if file_exist:  #check whether new_attend exist or not
            try:
                f = open(file_name, 'r',encoding = 'utf-8')     
                cur_data = int(f.read())    #read the number inside new_attend
                #print (cur_data)
                if cur_data < data:         #if exist check latest attendance with previous latest attendance
                    with open(file_name,'w', encoding = 'utf-8') as f:
                        f.write(str(data).decode('utf-8'))  #save latest attendance
                        f.close
                    #print('Data have been updated') #if latest attendance > previous attendance update the new_attend.txt
                    
                    attend_data = str(attend[data-1])
                    test, staff_id, test3, date_come, time_come, test6, test7=  attend_data.split() #take staff_id, date and time
                    #print('New attendance: ', staff_id, 'timestamp: ', date_come, time_come)
                    #print("Welcome! \n" + staff_name(int(staff_id)))
                    nameStaff = staff_name(int(staff_id))
                    conJson = nameStaff
                    sendJson = json.dumps(conJson)
                    print(sendJson)
                    sys.stdout.flush()
                else:
                    #print('No new entries')
                    stat = "No new Entries"
            except:
                print ('An excepetion occured')
                
        else:
            #if file not exist create a new one and save the latest attendance in new_attend.txt
            with open(file_name,'w', encoding = 'utf-8') as f:
                f.write(str(data).decode('utf-8'))
                f.close
            #print('File created')
            attend_data = str(attend[data-1])
            test, staff_id, test3, date_come, time_come, test6, test7=  attend_data.split() #take staff_id, date and time
            #print('New attendance: ', staff_id, 'timestamp: ', date_come, time_come)
            #print(staff_name(int(staff_id)))
            nameStaff = staff_name(int(staff_id))
            conJson = nameStaff
            sendJson = json.dumps(conJson)
            print(sendJson)
            sys.stdout.flush()
            
    except Exception as e:
        print ('Process terminate : {}'.format(e))
    finally:
        if conn:
            conn.disconnect()
    
def signal_handler(signum, frame):
    raise ProgramKilled

class Job(threading.Thread):
    def __init__(self, interval, execute, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = False
        self.stopped = threading.Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs

    def stop(self):
        self.stopped.set()
        self.join()
    
    def run(self):
        while not self.stopped.wait(self.interval.total_seconds()):
            self.execute(*self.args, **self.kwargs)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    job = Job(interval=timedelta(seconds=wait_time), execute=foo)
    job.start()
    
    while True:
          try:
              time.sleep(1)
          except ProgramKilled:
              #print ("Program killed: running cleanup code")
              job.stop()
              break        
    
