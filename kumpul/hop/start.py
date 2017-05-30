import socket
import struct
import pickle
import time

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
client.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('', MCAST_PORT))

mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
server.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

hop = 3 # Jml hop

def init_msg():
    msg = []
    msg.append("Halo") # Pesan yang dikirim
    msg.append(hop)
    msg.append("Roni") # Tujuan pesan
    msg = pickle.dumps(msg)
    return msg

time.sleep(1)

while True:
    client.sendto(init_msg(), (MCAST_GRP, MCAST_PORT))