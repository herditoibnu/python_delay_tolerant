import socket
import struct
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

message=raw_input("Masukkan pesan:")
dest=raw_input("Masukkan nama tujuan:")

limit_sec = raw_input("Masukkan umur pesan (detik):")
limit_sec = int(limit_sec)

hop = raw_input("Masukkan maksimal hop:")
hop = int(hop)

latitude = raw_input("Masukkan latitude:") # 52
latitude = int(latitude)

longitude = raw_input("Masukkan longitude:") # 21
longitude = int(longitude)

dist = raw_input("Masukkan jarak:") #342
dist = int(dist)

start  = raw_input("Mulai? (y):")
if start == "y":
    t1 = datetime.now()

def init_msg():
    msg = []
    msg.append(message) # Pesan yang dikirim
    msg.append(dest)  # Tujuan pesan

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

while True:
    try:
        client.sendto(init_msg(), (MCAST_GRP, MCAST_PORT))
        if limit_sec_new == 0:
            print "Umur pesan habis"
            break
    except NameError:
        continue