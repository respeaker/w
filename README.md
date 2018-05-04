# w

Send Wi-Fi settings through sound wave.

The application is based on [libquiet](https://github.com/quiet) which is a library to transmit data with sound. 

## To Do
1. Install [quiet](https://github.com/quiet/quiet).
Second

2. Get the configuration

        wget http://respeaker.io/w/js/quiet-profiles.json
        sudo cp quiet-profiles.json /usr/local/share/quiet/quiet-profiles.json

3. Run a receiver

        quiet_decode_soundcard ultrasonic-experimental

4. Go to [respeaker.io/w](http://respeaker.io/w) to transmit any data


![](send.png)


