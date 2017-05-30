import socket
import struct
import threading
import pickle
from datetime import datetime

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
        global limit_sec
        limit_sec = msg_recv[1]
        global dest
        dest = msg_recv[2]
        print limit_sec
        break

t1 = datetime.now()

threads = []
t_sendfeedback = threading.Thread(target=sendfeedback)
threads.append(t_sendfeedback)
t_sendfeedback.start()

def init_msg():
    msg = []
    msg.append(message)
    t2 = datetime.now()
    diff_sec = t2 - t1
    global limit_sec_new
    limit_sec_new = limit_sec - diff_sec.seconds
    msg.append(limit_sec_new)
    msg.append(dest)
    msg = pickle.dumps(msg)
    return msg

while True:
    try:
        if dest == "Roni":  # Tujuan pesan
            print message
            break
        client.sendto(init_msg(), (MCAST_GRP, MCAST_PORT))
        if limit_sec_new == 0:
            print "Umur pesan habis"
            break
    except NameError:
        continue