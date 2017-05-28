import socket
import struct
import threading
import pickle
import time
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

def recvfeedback(t1, limit_sec):
    global limit_sec_new
    while True:
        t2 = datetime.now()
        diff_sec = t2 - t1
        limit_sec_new = limit_sec - diff_sec.seconds
        if diff_sec.seconds == limit_sec:
            print "Masa berlaku pesan habis"
            break

        flag = server.recv(10240)
        if flag == "pesan diteruskan" or flag == "pesan diterima":
            print flag
            break

t1 = datetime.now()
limit_sec = 100 # Umur pesan (detik)

threads = []
t_recvfeedback = threading.Thread(target=recvfeedback, args=(t1, limit_sec,))
threads.append(t_recvfeedback)
t_recvfeedback.start()

def init_msg():
    msg = []
    msg.append("Halo") # Pesan yang dikirim
    msg.append(limit_sec_new)
    msg = pickle.dumps(msg)
    return msg

time.sleep(1)

while True:
    if not t_recvfeedback.is_alive():
        break
    client.sendto(init_msg(), (MCAST_GRP, MCAST_PORT))