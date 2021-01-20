import argparse
import logging
import socket

#set the logging details
formatter = logging.Formatter("[%(levelname)s] ['Function:' %(funcName)s() 'Line:' %(lineno)s] %(message)s", "%Y-%m-%d %H:%M:%S")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
log = logging.getLogger(__name__)
log.addHandler(handler)
log.setLevel(logging.DEBUG)


def parse_cmd():
    '''Parse command line arguments, read hostname and port'''
    basic_parser = argparse.ArgumentParser(prog='server_skeleton',  description='read the server hostname and port')
    basic_parser.add_argument('-s', '--hostname', type=str, help='hostname where this server will be running', default='127.0.0.1')
    basic_parser.add_argument('-p', '--port', help='port number', required=True)
    args = basic_parser.parse_args()
    log.debug('Hostname {}, port {}\n'.format(args.hostname, args.port))
    return {'hostname':args.hostname, 'port':args.port}

if __name__=='__main__':
    #read the parameters from command line
    parser = parse_cmd()
    hostname = parser['hostname']
    port = parser['port']


    #create a socket object


    #bind to the host and port we read from CMD


    #listen for incoming connections


    #if a client initiates a connection, accept it


    #receive data


    #send some data


    #if you receive a closing request, close that socket


    #continue listening 
