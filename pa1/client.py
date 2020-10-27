import binascii
import socket
import struct
import sys

def create_packet(**kwargs):
    print(kwargs)
    m_v = socket.htons(kwargs['message_version'])
    m_t = socket.htons(kwargs['message_type'])
    m_s = kwargs['message_string']
    data = struct.pack('!I', m_v) #pack the version
    data += struct.pack('!I', m_t) #pack the version
    data += struct.pack("!I", len(m_s)) #pack the length of string
    data += m_s.encode() #pack the data
    return data


# Create a TCP/IP socket

if __name__=='__main__':
    version =17
    hello_message = "Hello"
    hello_packet = create_packet(message_version=version, message_type = 1, message_string=hello_message)

    command_message = "LIGHTON"
    command_packet_on = create_packet(message_version=version, message_type = 2, message_string=command_message)

    command_message = "LIGHTOFF"
    command_packet_off = create_packet(message_version=version, message_type = 2, message_string=command_message)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 30001)
    sock.connect(server_address)

    sock.sendall(hello_packet)

    try:
        while True:
        # Send data
#        print( 'sending "%s"' % binascii.hexlify(packed_data), values)


            data = sock.recv(struct.calcsize('!III'))
            version_raw, message_type_raw, length_raw = struct.unpack('!III',data)
            version = socket.ntohs(version_raw)
            message_type = socket.ntohs(message_type_raw)
            length = socket.ntohs(length_raw)
            print ('version: {0:d} type: {1:d} length: {2:d}'.format(version, message_type, length))
            if version == 17:
                print("VERSION ACCEPTED")
            else:
                print("VERSION MISMATCH")
            message = sock.recv(length).decode()
            print("Message", message)

            if message_type == 1:
                print("Sending command")
                sock.sendall(command_packet_on) #or send off
            elif message_type == 2 and message == "SUCCESS":
                print("Command Successful")
                print('Closing socket')
                break

    finally:
        sock.close()
