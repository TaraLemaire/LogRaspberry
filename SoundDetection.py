
from github import Github, GithubException
import os
from pprint import pprint
from datetime import datetime
import serial, time

token="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"

if __name__ == '__main__':
    print('Running. Press CTRL-C to exit.')
    #Connection au depot Github
    try:
        g = Github(token)
        repoRasp = g.get_repo("TaraLemaire/LogRaspberry")
        print("Connected to repository :")
        print(repoRasp)
        file = repoRasp.get_contents("events.log")
        oldContent = file.decoded_content.decode()
        with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as arduino:
            time.sleep(0.1) #wait for serial to open
            if arduino.isOpen():
                print("{} connected!".format(arduino.port))
                try:
                    print("Waiting signal from Arduino : ")
                    while True:
                        if arduino.inWaiting()>0:
                            answer=arduino.read()
                            if answer == 'S':
                                date=datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
                                newContent = oldContent + date + "/SoundDetected\n"
                                repoRasp.update_file("events.log","Commit from RaspberryPI",newContent,file.sha,branch="main")
                                file = repoRasp.get_contents("events.log")
                                oldContent = file.decoded_content.decode() # nouveau code file.sha commit
                                arduino.flushInput() # vide le buffer
                                print(date + "/SoundDetected")
                                print("Waiting signal from Arduino : ")
                                time.sleep(0.1)
                except KeyboardInterrupt:
                    print("KeyboardInterrupt has been caught.")
    except GithubException as err:
        print("Connection github lost")
