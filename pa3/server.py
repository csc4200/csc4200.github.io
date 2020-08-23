import binascii
import socket
import struct
import sys

def create_packet(**kwargs):
    print(kwargs)
    m_v = kwargs['message_version']
    m_t = kwargs['message_type']
    m_s = kwargs['message_string']
    data = struct.pack('!I', m_v) #pack the version
    data += struct.pack('!I', m_t) #pack the version
    data += struct.pack("!I", len(m_s)) #pack the length of string
    data += m_s.encode() #pack the data
    return data


def run_command(command):
    return 0

if __name__=='__main__':
    version =17
    hello_message = "Hello"
    hello_packet = create_packet(message_version=version, message_type = 1,message_string=hello_message)


    #create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('localhost', 30001))
    #sock.listen(5) #backlog
    recv_buf = []
    FIN_SET = 0
    with open('recv_file', 'wb') as w:
        while True:
            data, address = sock.recvfrom(512)
            print("Received connection from (IP, PORT): ", address)
            try:
                w.write(data)
                print('Writing data')
            except socket.timeout:
                sock.close()
                print("File downloaded")
            if FIN_SET:
                break


