import binascii
import socket
import struct
import sys
import urllib.request


# Create a TCP/IP socket
def create_packet(**kwargs):
    print(kwargs)
    s_n = kwargs['sequence_number']
    a_n = kwargs['ack_number']
    padding = [x]*29
    ack = kwargs['ack']
    syn = kwargs['syn']
    fin = kwargs['fin']
    data = kwargs['data']
    data = struct.pack('!I', s_n) #pack the version
    data += struct.pack('!I', a_n) #pack the version
    data += struct.pack('!{0}s'.format(len(padding), padding)) #pack the version
    data += struct.pack("!c", ack) #pack the length of string
    data += struct.pack("!c", syn) #pack the length of string
    data += struct.pack("!c", fin) #pack the length of string
    data += struct.pack("{0}s".format(len(data),data))
    data += m_s.encode() #pack the data
    return data

def get_webpage(**kwargs):
    page = kwargs['webpage']
    with urllib.request.urlopen(page) as response, open("test", 'w') as w:
       html = response.read()
       w.write(html.decode())
    return html

if __name__=='__main__':
    webpage = get_webpage(webpage="www.python.org")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 30001)
    buf = 512
    r =  open('test', 'rb')
    total_read = 0
    data_size = len(webpage)
    data = r.read(buf)
    total_read += 512
    send_data = create_packet(sequence_number=100, ack_numeber=0, ack = 'Y', SYN = 'N', FIN = 'N', data)
    sock.sendto(data,server_address)
    while (total_read < data_size):
        if (sock.sendto(data, server_address)):
            send_data = create_packet(sequence_number=101, ack_numeber=0, ack = 'Y', SYN = 'N', FIN = 'N', data)
            data = r.read(buf)
            total_read += len(send_data)-12

    sock.close()
    r.close()


