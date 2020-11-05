#!/usr/bin/python3
import sys
from scapy.all import *
import urllib.request
import random 

import socket
import sys

HOST = 'localhost'	# Symbolic name meaning all available interfaces
PORT = 8888	# Arbitrary non-privileged port

def QoS_ping(host, count=3):
  packet = Ether()/IP(dst=host)/ICMP()
  t=0.0
  for x in range(count):
      ans,unans=srp(packet,iface="wlp82s0", filter='icmp', verbose=0)
      rx = ans[0][1]
      tx = ans[0][0]
      delta = rx.time-tx.sent_time
      print ("Ping:", delta)
      t+=delta
  return (t/count)*1000

def fetch_page(url):
  #replace this
  url = "http://"+url
  with urllib.request.urlopen(url) as response:
    html = response.read()
  return html



if __name__=="__main__":
    #pick the best one
    ip_addresses = ['google.com', "yahoo.com", 'google.com']
    total = QoS_ping(ip_addresses[1])
    print ("TOTAL", total)
    print("Average", total/3)

    #add loss

    #calculate the weight here, hardcoded in this example
    weight = (random.randint(0,2))
    print(weight)

    #pick the best weight
    origin = ip_addresses[weight]
    print(origin)
    fetched_data = fetch_page(origin)
#    print(data)
    
   
    # Datagram (udp) socket
    try :
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print('Socket created')
    except (socket.error, msg) :
            print('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()


    # Bind socket to local host and port
    try:
            s.bind((HOST, PORT))
    except socket.error:
            print('Bind failed')
            sys.exit()
            
    print('Socket bind complete')

    #now keep talking with the clients
    while True:
            # receive data from client (data, addr)
            d = s.recvfrom(1024)
            data = d[0]
            addr = d[1]
            
            if not data: 
               break
            
            reply = 'OK...' + str(fetched_data)
            s.sendto(reply.encode() , addr)
	



