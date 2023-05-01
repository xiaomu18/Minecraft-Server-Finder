import ipaddress
import struct
import socket
import json
from reptile_tools import threads

# For the rest of requests see wiki.vg/Protocol
def ping(ip: str, port: int):
    def read_var_int():
        i = 0
        j = 0
        while True:
            k = sock.recv(1)
            if not k:
                return 0
            k = k[0]
            i |= (k & 0x7f) << (j * 7)
            j += 1
            if j > 5:
                raise ValueError('var_int too big')
            if not (k & 0x80):
                return i
    #初始化套接字
    sock = socket.socket()
    sock.settimeout(1)
    try:
        sock.connect((ip, port))
    except Exception as e:
        return [False, e]
    

    try:
        host = ip.encode('utf-8')
        #数据包制作
        data = b''  # wiki.vg/Server_List_Ping
        data += b'\x00'  # packet ID
        data += b'\x04'  # protocol variant
        data += struct.pack('>b', len(host)) + host
        data += struct.pack('>H', port)
        data += b'\x01'  # next state
        data = struct.pack('>b', len(data)) + data
        #发送数据
        sock.sendall(data + b'\x01\x00')  # handshake + status ping

        length = read_var_int()  # full packet length
        if length < 10:
            if length < 0:
                raise ValueError('negative length read')
            else:
                raise ValueError('invalid response %s' % sock.read(length))

        sock.recv(1)  # packet type, 0 for pings
        length = read_var_int()  # string length
        data = b''

        while len(data) != length:
            chunk = sock.recv(length - len(data))
            if not chunk:
                raise ValueError('connection abborted')

            data += chunk
        return [True, json.loads(data)]
    except Exception as e:
        return [False, e]
    finally:
        sock.close()

def do_it(f, i, il):
    ip_range = ipaddress.ip_network(str(i) + '.' + str(il) + '.0.0/16')

    for ip in ip_range:
        result = ping(str(ip), 25565)
        if result[0]:
            print("[ INFO ] find one: ", str(ip) + ":25565")
            f.write(str(ip) + ":25565\n")
            f.flush()
    
    return

if __name__ == "__main__":
    f = open("server.txt", "w")

    args = []
    for i in range(128, 256):
        for il in range(0, 256):
            args.append((f, i, il, ))
    
    threads(do_it, args=args, wait=True)
    print("ok.")
    input()