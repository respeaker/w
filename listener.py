
import os
import sys
if sys.version_info[0] < 3:
    import Queue as queue
else:
    import queue

import threading
import signal

import numpy
import pyaudio
from quiet.quiet import Decoder


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


def main():
    listener = Listener()

    def on_data(data):
        ssid_length = data[0]
        ssid = data[1:ssid_length+1].tostring()
        password = data[ssid_length+1:].tostring()

        if os.system('which nmcli') == 0:
            if os.system('sudo nmcli device wifi con {} {}'.format(ssid, password)) == 0:
                print('Wi-Fi is connected')
                listener.stop()
            else:
                print('Failed')
        else:
            print('to do')


    def int_handler(sig, frame):
        listener.stop()

    signal.signal(signal.SIGINT, int_handler)

    listener.on_data = on_data
    listener.run()


if __name__ == '__main__':
    main()
