from flask import Flask
from Pedokom import pedokom
from dbctl import apeksdbctl

try:
    Coms = pedokom.PedoKom('/dev/ttyUSB0', 9600, .1)
except:
    Coms = pedokom.PedoKom('/dev/ttyUSB1', 9600, .1)

def PingMe():
    #time.sleep(2)
    asu = Coms.SendCommand("yuhu", 1)
    if 'uth3re?' in asu["Response"]:
        Coms.SendCommand("metoo", 0)
    print(asu)

def main():
    apeksdbctl.DbInit()
    app_ = Flask(__name__)
    #Start Ping and Send Challenge Request to Arduino
    print('Sending Challenge Request...')
    PingMe()
    #a = Thread(target=miscale2.mainS, daemon=True)
    #a.start()
    print('[OK] Challenge Received')
    return app_
