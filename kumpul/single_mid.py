import socket
import struct
import threading
import pickle
from datetime import datetime
from math import sin, cos, sqrt, atan2, radians, floor

ask_dest = raw_input("Masukkan nama:")

ask_latitude = raw_input("Masukkan latitude:")
ask_latitude = int(ask_latitude)

ask_longitude = raw_input("Masukkan longitude:")
ask_longitude = int(ask_longitude)

start  = raw_input("Mulai? (y):")
if start == "y":
    t1 = datetime.now()

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
client.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('', MCAST_PORT))

mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
server.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

def sendfeedback():
    while True:
        msg = server.recv(10240)
        msg_recv = pickle.loads(msg)

        global message
        message = msg_recv[0]

        global dest
        dest = msg_recv[1]

        global limit_sec
        limit_sec = msg_recv[2]

        global hop
        hop = msg_recv[3] - 1

        global latitude
        latitude = msg_recv[4]

        global longitude
        longitude = msg_recv[5]

        global dist
        dist = msg_recv[6]

        break

threads = []
t_sendfeedback = threading.Thread(target=sendfeedback)
threads.append(t_sendfeedback)
t_sendfeedback.start()

def init_msg():
    msg = []
    msg.append(message)
    msg.append(dest)

    t2 = datetime.now()
    diff_sec = t2 - t1
    global limit_sec_new
    limit_sec_new = limit_sec - diff_sec.seconds
    msg.append(limit_sec_new)

    msg.append(hop)
    msg.append(latitude)
    msg.append(longitude)
    msg.append(dist)

    msg = pickle.dumps(msg)
    return msg

def getDist():
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(ask_latitude)
    lon1 = radians(ask_longitude)
    lat2 = radians(latitude)
    lon2 = radians(longitude)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = floor(R * c)
    return distance

while True:
    try:
        if dest == ask_dest:  # Tujuan pesan
            print message
            break
        if dist == getDist():  # Jarak tujuan pesan
            print message
            break
        client.sendto(init_msg(), (MCAST_GRP, MCAST_PORT))
        if limit_sec_new == 0:
            print "Umur pesan habis"
            break
        if hop == 0:
            print message
            print "Max hop terpenuhi"
            break
    except NameError:
        continue