
import os
import sys
if sys.version_info[0] < 3:
    import Queue as queue
else:
    import queue

import threading
import signal
import time

import numpy
import pyaudio
from quiet.quiet import Decoder
import evdev
from pixel_ring import pixel_ring
import mraa


power = mraa.Gpio(12)
time.sleep(1)

power.dir(mraa.DIR_OUT)
power.write(0)



class Listener(object):
    def __init__(self):
        self.pyaudio_instance = None
        self.done = None
        self.thread = None

    def start(self):
        self.done = False
        if not (self.thread and self.thread.is_alive()):
            self.thread = threading.Thread(target=self.run)
            self.thread.start()

    def run(self):
        FORMAT = pyaudio.paFloat32
        CHANNELS = 1
        RATE = 44100
        CHUNK = int(RATE / 10)

        if not self.pyaudio_instance:
            self.pyaudio_instance = pyaudio.PyAudio()

        q = queue.Queue()

        def callback(in_data, frame_count, time_info, status):
            q.put(in_data)
            return (None, pyaudio.paContinue)

        stream = self.pyaudio_instance.open(format=FORMAT,
                                            channels=CHANNELS,
                                            rate=RATE,
                                            input=True,
                                            frames_per_buffer=CHUNK,
                                            stream_callback=callback)

        decoder = Decoder(profile_name='ultrasonic-experimental')

        while not self.done:
            audio = q.get()
            audio = numpy.fromstring(audio, dtype='float32')
            data = decoder.decode(audio)
            if data is not None:
                self.on_data(data)

        stream.stop_stream()

    def stop(self):
        self.done = True
        if self.thread and self.thread.is_alive():
            self.thread.join()

    def on_data(self, data):
        print(data)


class Button(object):
    def __init__(self):
        pass

    def run(self):
        key = evdev.InputDevice("/dev/input/event0")
        timestamp = 0.
        action = None
        for event in key.read_loop():
            if event.type == evdev.ecodes.EV_KEY and event.code == 194:
                key_event = evdev.categorize(event)
                if key_event.keystate == key_event.key_down:
                    timestamp = event.timestamp()
                    action = None
                    print('key down')
                elif key_event.keystate == key_event.key_hold:
                    dt = event.timestamp() - timestamp
                    if dt > 3 and action is None:
                        action = True
                        self.on_hold()
                        print('hold more than 3 seconds')
                else:
                    dt = event.timestamp() - timestamp
                    if dt < 2:
                        self.on_click()
                    elif dt > 3 and action is None:
                        self.on_hold

                    print('hold {} seconds'.format(dt))
                    print('key up')

    def on_click(self):
        print('on click')

    def on_hold(self):
        print('on hold')
        

class EventManager:
    pass


def main():
    button = Button()
    listener = Listener()

    listener.is_muted = False

    def on_click():
        if listener.is_muted:
            print('Unmute')
            pixel_ring.off()
        else:
            print('Mute')
            listener.stop()
            
        listener.is_muted = not listener.is_muted

    def on_hold():
        if not listener.is_muted:
            listener.start()
            pixel_ring.think()

    def on_data(data):
        ssid_length = data[0]
        ssid = data[1:ssid_length+1].tostring()
        password = data[ssid_length+1:].tostring()

        if os.system('which nmcli') == 0:
            if os.system('sudo nmcli device wifi connect {} {}'.format(ssid, password)) == 0:
                print('Wi-Fi is connected')
                listener.stop()
                pixel_ring.off()
            else:
                print('Failed')
        else:
            print('to do')

    def on_interrupt(*arg, **karg):
        listener.stop()

    # signal.signal(signal.SIGINT, on_interrupt)

    listener.on_data = on_data
    button.on_click = on_click
    button.on_hold = on_hold

    button.run()
    

if __name__ == '__main__':
    main()
