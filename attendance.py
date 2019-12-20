from __future__ import print_function
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

def staff_name(staff_id):
    
    if staff_id == 0001:
		Sname = "Test"
    elif staff_id == 2:
        Sname = "ADMIN"
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
                print("Welcome! \n" + staff_name(int(staff_id)))
                nameStaff = staff_name(int(staff_id))
                conJson = {"Staff ID" : staff_id,
                "Staff Name" : nameStaff,
                "Time" : time_come}
                sendJson = json.dumps(conJson)
                #print(sendJson)
            else:
                #print('No new entries')
                stat = "No new Entries"
                attend_data = str(attend[data-1]) #nanti delete balik
                test, staff_id, test3, date_come, time_come, test6, test7=  attend_data.split() #take staff_id, date and time
                #print('New attendance: ', staff_id, 'timestamp: ', date_come, time_come)
                print ("No new staff")
                
        except:
            print ('An excepetion occured')
            
    else:
        #print('File not exist')  #if file not exist create a new one and save the latest attendance in new_attend.txt
        with open(file_name,'w', encoding = 'utf-8') as f:
            f.write(str(data).decode('utf-8'))
            f.close
        #print('File created')
        attend_data = str(attend[data-1])
        test, staff_id, test3, date_come, time_come, test6, test7=  attend_data.split() #take staff_id, date and time
        #print('New attendance: ', staff_id, 'timestamp: ', date_come, time_come)
        print(staff_name(int(staff_id)))
        nameStaff = staff_name(int(staff_id))
        conJson = {"Staff ID" : staff_id,
        "Staff Name" : nameStaff,
        "Time" : time_come}
        sendJson = json.dumps(conJson)
        #print(sendJson)
        
except Exception as e:
    print ('Process terminate : {}'.format(e))
finally:
    if conn:
        conn.disconnect()
