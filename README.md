# w

Send Wi-Fi settings through sound wave.

The application is based on [libquiet](https://github.com/quiet) which is a library to transmit data with sound.

## for ReSpeaker V2 or Raspberry Pi
1. Install quiet python library

   `sudo pip install ./quiet-*.whl`

2. Run a receiver

   `python listener.py`


3. Go to [respeaker.io/w](http://respeaker.io/w) to transmit any data

![](qr.png)


![](send.png)


## for PC
1. Install [quiet](https://github.com/quiet/quiet).
Second

2. Get the configuration

        wget http://respeaker.io/w/js/quiet-profiles.json
        sudo cp quiet-profiles.json /usr/local/share/quiet/quiet-profiles.json

3. Run a receiver

        quiet_decode_soundcard ultrasonic-experimental

4. Go to [respeaker.io/w](http://respeaker.io/w) to transmit any data
