import socket
import os
import json
import time

from flask import Flask
from flask import Flask, redirect, request, jsonify, make_response, render_template, url_for, send_file
from miscale2 import miscale2
from PedoScore import ZScore
from Pedokom import pedokom
from threading import Thread, Event
from queue import Queue
from multiprocessing import Process, Queue

import run

app = run.main()

busyo = 0
q = None
worker = None


try:
    Coms = pedokom.PedoKom('/dev/ttyUSB0', 9600, .1)
except:
    Coms = pedokom.PedoKom('/dev/ttyUSB1', 9600, .1)

def ThreadD(q):
    global busyo
    #if busyo == 1:
    #    time.sleep(3)
    
    tb = []
    #PingMe()
    busyo =1
    #Coms = pedokom.PedoKom('/dev/ttyUSB0', 9600, .1)
    #jangan lupa IMT
    
    data = q.get()
    print(data)
    print("MULAI JALAN")
    #Coms.SendCommand("pesan1;Ukur Berat Badan", 0)
    Coms.SendCommand("pesan2;Measuring...", 0)

    #HOST = '127.0.0.1'  # The server's hostname or IP address
    #PORT = 65433        # The port used by the server

    #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #    s.connect((HOST, PORT))
    #    s.sendall(b'miscale2.noimpedance')
    #    data = s.recv(1024)

    data_ = miscale2.mainV()
    print("BERAT: ", data_)

    Berat = float(data_["Berat"])

    #time.sleep(3)
    #Coms.SendCommand("pesan1;Mengukur Tinggi")
    #Coms.SendCommand("pesan2;Tegakkan Badan")

    tinggi = Coms.SendCommand("tinggi",2)["Response"].split(",")
    temp = tinggi[0:len(tinggi)-1]
    temp2 = []
    for i in temp:
        temp2.append(float(i))

    Tinggi = max(temp2)
    #Tinggi = max(tb) #float(Coms.SendCommand("tinggi")["Response"])
    print("TINGGI: ", Tinggi)

    #time.sleep(3)

    print("JSON: ", data)
    
    try:
        usia = int(data.get("usia",0))
    except:
        usia = 0
    
    try:
        jk = str(data.get('kelamin', "no")).lower()
    except:
        jk = "no"

    Gender = ""
    if jk == "boy":
        Gender = "M"
    else:
        Gender = "F"

    zee = ""
    if usia == 0 and jk == "no":
        zimt = ZScore.IMT(Berat, Tinggi/100)
        zee = "BMI (Body Mass Index)"
    else:
        zimt = ZScore.ZScore(usia, Berat, Gender)
        zee = "Z-Score"

    resp = {"zimt": zimt, "tinggi": str(Tinggi)+" CM", "berat": str(Berat), "Pesan": zee}
    
    Coms.SendCommand("pesanx;Tinggi: " + str(Tinggi) + "CM?" + "Berat: " + str(Berat) + "KG", 0)
    q.put_nowait(resp)
    #q.task_done()

    #Coms.SendCommand("pesanx;Go WebWifi?=>apeks.net<=")

@app.route('/', methods=["GET"])
def index():
    #return render_template('index.html')
    return render_template('index.html')

def PingMe():
    #time.sleep(2)
    asu = Coms.SendCommand("yuhu", 1)
    if 'uth3re?' in asu["Response"]:
        Coms.SendCommand("metoo", 0)
    print(asu)

@app.route('/sane', methods=["GET", "POST"])
def Sane():
    global busyo
    print("BUSY STATE = ", busyo)
    if busyo == 1:
        return "ok"
    else:
        return "ok"

@app.route('/clear', methods=["GET", "POST"])
def bersih():
    global busyo
    Coms.SendCommand("pesan1;Go WebWifi")
    Coms.SendCommand("pesan2;=>apeks.net<=")

    time.sleep(3)
    Coms.SendCommand("pesan1;    Welcome")
    Coms.SendCommand("pesan2;Waiting Input...")
    busyo = 0
    return "ok"

@app.route('/measure', methods=["GET", "POST"])
def measure():
    global q, worker, busyo
    
    if busyo == 1:
        print("[DEBUG] Busy State Terminate...")
        worker.terminate()

    busyo = 1
    q = Queue(maxsize=0)
    data = request.get_json(force=True)
    
    worker = Process(target=ThreadD, args=(q,))
    worker.daemon = True
    worker.start()
    
    q.put(data)
    
    worker.join()
    
    resp = q.get()
    busyo = 0
    return make_response(jsonify(resp), 200)

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5050, debug=True)
