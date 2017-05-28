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

def countRecv(val):
    global countCek
    countCek = val

def recvfeedback(t1, val):
    global limit_sec_new
    global messageExpired
    messageExpired = 0
    while True:
        t2 = datetime.now()
        diff_sec = t2 - t1
        limit_sec_new = limit_sec - diff_sec.seconds
        if diff_sec.seconds == limit_sec:
            print "Masa berlaku pesan habis"
            messageExpired = 1
            break

        flag = server.recv(10240)
        if flag == "pesan diteruskan" or flag == "pesan diterima":
            print flag
            countRecv(val)
            break

def sendfeedback():
    while True:
        global msg
        msg = server.recv(10240)
        msg_recv = pickle.loads(msg)
        global limit_sec
        limit_sec = msg_recv[1]
        print limit_sec
        client.sendto("pesan diteruskan", (MCAST_GRP, MCAST_PORT))
        break

t1 = datetime.now()

threads = []
t_sendfeedback = threading.Thread(target=sendfeedback)
threads.append(t_sendfeedback)
t_sendfeedback.start()

flag_thread_send = 1
flag_thread_recv = 0
flag_thread_sec = 1

while True:
    if not t_sendfeedback.is_alive() and flag_thread_send:
        flag_thread_send = 0
        flag_thread_recv = 1
        t_recvfeedback = threading.Thread(target=recvfeedback, args=(t1,1,))
        threads.append(t_recvfeedback)
        t_recvfeedback.start()

    if flag_thread_recv and flag_thread_sec:
        flag_thread_recv = 0
        flag_thread_sec = 0
        time.sleep(1)
        t_recvfeedback = threading.Thread(target=recvfeedback, args=(t1,2,))
        threads.append(t_recvfeedback)
        t_recvfeedback.start()

    try:
        client.sendto(msg, (MCAST_GRP, MCAST_PORT))
        if messageExpired:
            break
        if countCek == 2:
            break
    except NameError:
        continue