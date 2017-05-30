import socket
import struct
import threading
import pickle
from datetime import datetime
from math import sin, cos, sqrt, atan2, radians, floor

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
        global latitude
        latitude = msg_recv[1]
        print latitude
        global longitude
        longitude = msg_recv[2]
        print longitude
        break

t1 = datetime.now()

threads = []
t_sendfeedback = threading.Thread(target=sendfeedback)
threads.append(t_sendfeedback)
t_sendfeedback.start()

def init_msg():
    msg = []
    msg.append(message)
    msg.append(latitude)
    msg.append(longitude)
    msg = pickle.dumps(msg)
    return msg

def getDist():
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(52.406374)
    lon1 = radians(16.925168)
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
        if getDist() == 100 or getDist() == 500: # Jarak tujuan pesan
            print message
            break
        client.sendto(init_msg(), (MCAST_GRP, MCAST_PORT))
    except NameError:
        continue