from flask import Flask, request, jsonify
from multiprocessing import Value
from flask_cors import CORS
import os
import logging

counter = Value('i', 0)
app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

@app.route("/info", methods=["POST"])
def info():
    data = request.get_json()
    print(data)
    return jsonify({"did": 0})

@app.route("/api", methods=["POST"])
def api():
    with counter.get_lock():
        counter.value = (counter.value+1)%100
    
        data = request.get_json()
        #print(data)
        f = open("input"+str(counter.value)+".txt", "w")
        f.write("%d %d %d\n" % (data["left"],data["state"],data["maxf"]))
        for i in range(34):
            f.write("%d " % data["hai"][i])
        f.write("\n")
        for i in range(34):
            f.write("%d " % data["rest"][i])
        f.write("\n")
        for i in range(len(data["dora"])):
            f.write("%d " % data["dora"][i])
        f.write("\n")
        for i in range(len(data["yi"])):
            f.write("%d " % data["yi"][i])
        f.write("\n")
        for i in range(4):
            for j in range(34):
                f.write("%d " % data["safecards"][i][j])
            f.write("\n")
        for i in range(4):
            f.write("%d " % data["playerliqi"][i])
        f.write("\n")
        f.close()


        did = os.system("maj_cpk.exe input"+str(counter.value)+".txt")
        f=open("output.txt","r")
        did,xt,xtd,val = f.read().split()
        did = int(did)
        xt = int(xt)
        xtd = int(xtd)
        val = float(val)
        f.close()
        #print("ans", ({"discard_id": did, "xt":xt, "val":val}))
        return jsonify({"discard_id": did, "xt":xt, "val":val})
    

@app.route("/cpk", methods=["POST"])
def cpk():
    with counter.get_lock():
        counter.value = (counter.value+1)%20
        data = request.get_json()
        f = open("input"+str(counter.value)+".txt", "w")
        f.write("%d %d %d\n" % (data["left"],data["state"],data["maxf"]))
        for i in range(34):
            f.write("%d " % data["hai"][i])
        f.write("\n")
        for i in range(34):
            f.write("%d " % data["rest"][i])
        f.write("\n")
        for i in range(len(data["dora"])):
            f.write("%d " % data["dora"][i])
        f.write("\n")
        for i in range(len(data["yi"])):
            f.write("%d " % data["yi"][i])
        f.write("\n")
        for i in range(4):
            for j in range(34):
                f.write("%d " % data["safecards"][i][j])
            f.write("\n")
        for i in range(4):
            f.write("%d " % data["playerliqi"][i])
        f.write("\n")
        f.close()


        did = os.system("maj_cpk.exe input"+str(counter.value)+".txt")
        f=open("output.txt","r")
        sread = f.read()
        did,xt,xtd,val = sread.split()
        did = int(did)
        xt = int(xt)
        xtd = int(xtd)
        val = float(val)
        chiflag = False
        f.close()

        bestval = val
        bestdid = did
        bestk = -1
        bestk2 = -1

        temp = {}
        hai = data["hai"]
        if(xt <= 1 or xt >= 4 or (xt > 2 and sum(data["playerliqi"]) > 0)):
            #print("ans", ({"discard_id": -1, "k1":-1,"k2":-1}))
            return jsonify({"discard_id": -1, "k1":-1,"k2":-1})

        for k in data["choices"]:
            if(k[0] in temp and temp[k[0]]==k[1]):continue
            counter.value = (counter.value+1)%20
            hai[k[0]] -= 1
            hai[k[1]] -= 1
            temp[k[0]]=k[1]

            f = open("input"+str(counter.value)+".txt", "w")
            f.write("%d %d %d\n" % (data["left"],(1 if data["state"]==0 else data["state"]),data["maxf"]-1))
            for i in range(34):
                f.write("%d " % data["hai"][i])
            f.write("\n")
            for i in range(34):
                f.write("%d " % data["rest"][i])
            f.write("\n")
            for i in range(len(data["dora"])):
                f.write("%d " % data["dora"][i])
            f.write("\n")
            for i in range(len(data["yi"])):
                f.write("%d " % data["yi"][i])
            f.write("\n")
            for i in range(4):
                for j in range(34):
                    f.write("%d " % data["safecards"][i][j])
                f.write("\n")
            for i in range(4):
                f.write("%d " % data["playerliqi"][i])
            f.write("\n")
            f.close()


            hai[k[0]] += 1
            hai[k[1]] += 1

            did = os.system("maj_cpk.exe input"+str(counter.value)+".txt")
            f=open("output.txt","r")
            sread = f.read()
            did2,xt2,xtd2,val2 = sread.split()
            f.close()
            did2 = int(did2)
            xt2 = int(xt2)
            xtd2 = int(xtd2)
            val2 = float(val2)
            if(xtd2>=xt or xtd2 == 0):
                continue
            if(data['state'] == 0):
                if(chiflag == False):# and val2 > val * 2 * 1.2):
                    chiflag = True
                if(chiflag):
                    bestk = k[0]
                    bestk2 = k[1]
                    bestval = val2
                    bestdid = did2
            else:
                chiflag = True
                bestk = k[0]
                bestk2 = k[1]
                bestval = val2
                bestdid = did2


        if(chiflag):
            #print("ans", {"discard_id": bestdid, "k1":bestk, "k2":bestk2})
            return jsonify({"discard_id": bestdid, "k1":bestk, "k2":bestk2})
        else:
            #print("ans", ({"discard_id": -1, "k1":-1,"k2":-1}))
            return jsonify({"discard_id": -1, "k1":-1,"k2":-1})
            

if __name__ == "__main__":
    CORS(app, supports_credentials=True)
    app.run(host="127.0.0.1", port=2356)
