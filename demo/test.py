import vlc
import os
p = vlc.MediaPlayer("/home/YFENG/Desktop/Raspi-car/录音.mp3")
p.play()


os.system('arecord -D "plughw:1,0" -f dat -c 1 -r 16000 -d 5 /home/YFENG/Desktop/Raspi-car/录音.mp3')
