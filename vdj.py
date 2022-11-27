import requests
import time
import serial
import sys
import threading


def Average(lst):
    return sum(lst) / len(lst)

# send paclkets to arduino over serial
# Packet: brightness;palette;max_brightness;mode;speed
def write_to_serial():
    ser = serial.Serial('COM5', 115200, timeout=0.050)
    # global brightness
    global error_count
    # brightness = '0.971'
    while True:

        try:
            value_brgt= int(float(brightness)*100)
            to_send = str(value_brgt) + ';'+ str(palette) +';255;1;100&'
            ser.write(to_send.encode())
            # print("Sending: " + to_send)
            time.sleep(frequency)
            if stop_threads:
                break
        except Exception as e:
            print("error" + str(e))
            error_count += 1 

def get_light():
    global brightness
    global mode
    global error_count
    last_beats = [] 

    avg_beats = 0.2


    while True:
        try:
            if stop_threads:
                break

            if mode == '1':
                x = requests.get('http://127.0.0.1/query?script=get_beat2', verify=False, timeout=1)

                if float(x.text) < avg_beats - 0.1 or float(x.text) < clip:
                    brightness = '0.0'
                else: 
                    brightness = x.text
                # print(float(x.text))
                last_beats.append(float(x.text))
                if len(last_beats) > sample_time/frequency:
                    avg_beats = Average(last_beats)
                    last_beats = []

                to_print = 'Current: ' + str(x.text) + (4-len(str(x.text)))*' ' + ' Sent: ' + str(brightness) + (4-len(brightness))*' ' + ' Average: ' + str(avg_beats) 
                
                print(to_print)
                time.sleep(frequency)    

            elif mode == '2':
                # x = requests.get('http://127.0.0.1/query?script=get_bpm', verify=False, timeout=1)
                # time_between_grid = 60/float(x.text)
                x = requests.get('http://127.0.0.1/query?script=get_beatgrid', verify=False, timeout=1)
                if float(x.text) > 0.90 or float(x.text) < 0.00:
                    brightness = x.text
                    print("Beatgrid: " + str(x.text))
                else:
                    brightness = '0.0'


        except Exception as e:
            print("error" + str(e))
            error_count += 1







#CONFIG
frequency = 0.01
clip = 0.31
sample_time = 0.5 #seconds


error_count = 0
to_send = "0.0"
stop_threads = False
mode = 1
brightness = '0.0'
palette = 1



if __name__ == "__main__":

    mode = input('Select mode: 1 - beat, 2 - grid: ')
    write_thread = threading.Thread(target=write_to_serial, args=())
    write_thread.start()
    print("Started write thread")

    write_thread = threading.Thread(target=get_light, args=())
    write_thread.start()
    print("Started light thread")
    try:
        while True:
            palette = input('Select mode: 1 - beat, 2 - grid: ')
    except KeyboardInterrupt:
        print ('Interrupted, encoutered ' + str(error_count) + ' errors')
        stop_threads = True

        sys.exit(0)


