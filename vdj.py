import requests
import time
import serial
import sys
import threading
import pygame
import pygame_gui

def Average(lst):
    return sum(lst) / len(lst)

def update_ui():
    window_width = 200
    window_height = 800

    global mode
    global stop_threads

    pygame.init()

    pygame.display.set_caption('Light Controller')
    window_surface = pygame.display.set_mode((window_width, window_height))

    background = pygame.Surface((window_width, window_height))
    background.fill(pygame.Color('#000000'))

    manager = pygame_gui.UIManager((window_width, window_height))

    hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10), (100, 50)),
                                                text='FLASH!',
                                                manager=manager)

    clp_scroll = pygame_gui.elements.UIVerticalScrollBar(relative_rect=pygame.Rect((10, 100), (30, 160)),
                                            visible_percentage=0.2,
                                            manager=manager)

    clp_scroll_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 70), (30, 30)),
                                text='CLP',
                                manager=manager)

    spd_scroll = pygame_gui.elements.UIVerticalScrollBar(relative_rect=pygame.Rect((50, 100), (30, 160)),
                                            visible_percentage=0.2,
                                            manager=manager)

    spd_scroll_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 70), (30, 30)),
                                text='SPD',
                                manager=manager)

    frq_scroll = pygame_gui.elements.UIVerticalScrollBar(relative_rect=pygame.Rect((90, 100), (30, 160)),
                                            visible_percentage=0.2,
                                            manager=manager)

    frq_scroll_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((90, 70), (30, 30)),
                                text='FRQ',
                                manager=manager)

    mode_dropdown = pygame_gui.elements.UIDropDownMenu(options_list=['Beat', 'BeatGrid'],
                                    starting_option='Beat',
                                    relative_rect=pygame.Rect((10, 300), (125, 50)),
                                    manager=manager)
    mode_dropdown_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((20, 270), (30, 30)),
                                text='MODE',
                                manager=manager)
                                

    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == hello_button:
                    mode = 3

            manager.process_events(event)

        manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)

        pygame.display.update()
    stop_threads = True


# send paclkets to arduino over serial
# Packet: brightness;palette;max_brightness;mode;speed
def write_to_serial():
    ser = serial.Serial('COM4', 115200, timeout=0.050)
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
    global palette
    global mode
    global error_count
    last_beats = [] 

    avg_beats = 0.2


    while True:
        try:
            if stop_threads:
                break

            if mode == 1:
                x = requests.get('http://127.0.0.1/query?script=get_beat2', verify=False, timeout=1)
                palette = 1
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

            elif mode == 2:
                # x = requests.get('http://127.0.0.1/query?script=get_bpm', verify=False, timeout=1)
                # time_between_grid = 60/float(x.text)
                x = requests.get('http://127.0.0.1/query?script=get_beatgrid', verify=False, timeout=1)
                palette = 1
                if float(x.text) > 0.90 or float(x.text) < 0.00:
                    brightness = x.text
                    print("Beatgrid: " + str(x.text))
                else:
                    brightness = '0.0'

            elif mode == 3 :
                # x = requests.get('http://127.0.0.1/query?script=get_bpm', verify=False, timeout=1)
                # time_between_grid = 60/float(x.text)
                brightness = "1"
                palette = 0
                time.sleep(0.15)    
                brightness = '0.0'
                mode = 0
                

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

    ui_thread = threading.Thread(target=update_ui, args=())
    ui_thread.start()
    print("Started ui thread")
    write_thread = threading.Thread(target=write_to_serial, args=())
    write_thread.start()
    print("Started write thread")

    write_thread = threading.Thread(target=get_light, args=())
    write_thread.start()
    print("Started light thread")


