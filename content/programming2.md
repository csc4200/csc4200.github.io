---
title: "To the Cloud and Back"
sidebar: true # or false to display the sidebar
sidebarlogo: fresh-white-alt # From (static/images/logo/)
---
## Due Date - April 04, 2021, 10PM CST
___
**Objectives**
___

In this project, you are going to build on the first project. You will have a server in the cloud that downloads and saves a web page in memory. You will then have clients connect to the server and retrives this content. This is the overly simplified idea behind a **WEB PROXY**. The client and server communications MUST use UDP (SOCK_DGRAM) and NOT TCP.

The objectives are:

-- Learn to create robust network protocols

-- Learn about reliable communication

-- How a premitive proxy might work. You can use this to get around sensorship or firewalls.

___
**Server Specifications**
___
The server (we name it anonserver) takes two arguments:

```
$ anonserver -p <PORT> -s <LOG FILE LOCATION> -w <web page to download>
```

1.```PORT``` - The port server listens on.

2.```Log file location``` - Where you will keep a record of actions.

3.```Web page to download``` - Which webpage to download and serve.

For example:

```
$ anonserver -p 30000 -l /tmp/logfile -w www.nytimes.com
```


You can use python URLLIB2 to download the files. Here is a helpful tutorial: https://docs.python.org/3/howto/urllib2.html
___
**Server's Functional requirements**
___
   1. The server must open a UDP socket on the specified port number
   2. The server should gracefully process incorrect port number and exit with a non-zero error code
   3. The server should send a FIN after done sending the packet
   4. The server should download the file specified by -p and serve it from the memory (you don't need to write the retrieved page to a file, just save it to a variable/string)
   5. The server runs indefinitely - it does not exit.
   6. The server accepts connections from multiple clients.

___
***Client Specifications***
___

The client (we name it anonclient) takes four arguments:
<br>

```
$ anonclient -s <SERVER-IP> -p <PORT> -l LOGFILE -f <file_to_write_to>
```

The client takes three arguments:

1.```Server IP``` - The IP address of the anonserver.

2.```PORT``` - The port the server listens on.

2.```Log file location``` - Where you will keep a record of packets you received.

2.```File to write to``` - Where you will write the retrieved content.


```
For example:
$ anonclient -s 192.168.2.1 -p 6543 -l LOGFILE -f test.txt
```
<br>

___
**Packet Specification**
___
The payload of each UDP packet sent by server and client MUST start with the following 12-byte header. All fields are in network order (most significant bit first):

```
   0                   1                   2                   3
   0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  |                        Sequence Number                        |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  |                     Acknowledgment Number                     |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  |                  Not Used                               |A|S|F|
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```
Where:

1. Sequence Number (32 bits): The sequence number of the first data octet in this packet (except when SYN is present). If SYN is present the sequence number is the initial sequence number (randomly choosen).

3. Acknowledgement Number (32 bits): **If the ACK control bit is set, this field contains the value of the next sequence number the sender of the segment is expecting to receive. Once a connection is established this is always sent.**

4. The acknowledgement number is given in the unit of bytes (how many bytes you have sent)

6. Not Used (29 bits): Must be zero.

7. A (ACK, 1 bit): Indicates that there the value of Acknowledgment Number field is valid

8. S (SYN, 1 bit): Synchronize sequence numbers

9. F (FIN, 1 bit): Finish, No more data from sender


___
**This is the protocol you will implement**
___

1. The client opens a UDP socket and initiate 3-way handshake to the specified hostname/ip and port. For an explanation of how a three way handshake works, see the next three steps. Essentially, the client and server will exchange three packets with the following flags sets: (1) SYN (2) SYN|ACK (3)ACK. At the end of the handshake, they will have learned each other's sequence number.

3. Handshake Step 1: *Anonclient* sends a UDP packet with the following parameters: 
  - **src-ip=anonclient_IP, src-port=anonclient_port, dst-ip=anonserver_ip, dst-port=anonserver_port, Sequence Number set to 12345 (or chosen randomly), SYN flag set to 1, ACK flag set to 0, FIN flag set to 0**.
 
4. Handshake Step 2:  *Anonserver* sends a UDP packet with the following parameters: 
  - **src-ip=anonserver_IP, src-port=anonserver_port, dst-ip=anonclient_ip, dst-port=anonclient_port. Sequence Number set to 100 (or chosen randomly), ACK number set to 12346 (Clients seq number + 1) SYN flag set to 1, ACK flag set to 1, FIN flag set to 0**.

5. Handshake Step 3:  Anonclient sends a UDP packet with the following parameters: 
  - **src-ip=anonclient_IP, src-port=anonclient_port, dst-ip=anonserver_ip, dst-port=anonserver_port, Sequence Number set to 12346 (ACK from server), ACK number set to 101 (Server seq number + 1), SYN flag set to 0, ACK flag set to 1, FIN flag set to 0**.

6. Now both anonclient and anonserver knows each others' sequence numbers and communication can begin. You only perform this handshake once.
3. Server sends 512 bytes of data in an UDP packet as a payload. It also increases the sequence number  **(seq_to_send = client_seq_received + 1)**, and sets the ACK flag.
4. The Client acknowledges the number of bytes it received by setting the ACK flag, and adding the number of bytes received to the previous client sequence number **(seq_to_send = server_seq_received + number of bytes received)**.
4. Upon receiving this ACK, the server creates another packet, sets the ACK flag, updates the sequence number, and sends another 512 bytes.
5. This interaction continues until all data is sent to the client.
6. The last packet from the server has the FIN bit set.
7. The client will send a packet with both FIN and ACK bit set. This completes the data transfer.
7. Once the interaction is complete, write the retrieved content to a file (on the client side).

Here is what a sample interaction looks like:

```
      Server                                     Client
      |                                            |
      |     seq=12345, ack=0, SYN                  |
      | <------------------------------------------|
      | seq=100,  ack=12346, SYN, ACK              |
      | ----------------------------------------- >|
      |   seq=12346,  ack=101, ACK           	   |
      | <----------------------------------------- |####handshake complete, start getting data
      |seq=101, ack=12347, ACK,512Byte payload 	   |	
      | -----------------------------------------> |
      |   seq=12347, ack=614, ACK            	   |
      | <----------------------------------------- |
      |seq=614,ack=12348,ACK,512Byte payload 	   |
      | ----------------------------------------- >|
      |   seq=12348, ack=1126, ACK           	   |
      | <----------------------------------------- |
      |seq=1126, ack=12349,ACK,512Byte payload	   |
      | ----------------------------------------- >|
      |   seq=12349, ack=1638, ACK           	   |
      | <----------------------------------------- |
      |seq=1638, ack=12350, FIN, payload=5bytes    |
      | -----------------------------------------> |
      |seq=12350, ack=1643, FIN, ACK               |
      | <----------------------------------------- |
```


___
**Additional requirements:**
___
1. Code must compile/run on Google Cloud Ubuntu VM (18.04) - we will test your code only on the VM.
2. For each packet received, log both at server and receiver in the following format:
```
"RECV" <Sequence Number> <Acknowledgement Number> ["ACK"] ["SYN"] ["FIN"]
"SEND" <Sequence Number> <Acknowledgement Number> ["ACK"] ["SYN"] ["FIN"]
```
---
**Hints**
---

`  def create_packet(**kwargs):`

    data = struct.pack('!I', s_n) #pack the version
    ....
    data += struct.pack("!c", ack) #pack the ACK
    data += struct.pack("!c", syn) #pack the SYN
    data += struct.pack("!c", fin) #pack the FIN
    ....
    return data    
    
`send_data = create_packet(sequence_number=100, ack_number=0, ack = 'Y', syn = 'N', fin = 'N', payload=data)    `

	
