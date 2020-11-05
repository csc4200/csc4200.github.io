---
title: "Create your own content delivery network"
sidebar: true # or false to display the sidebar
sidebarlogo: fresh-white-alt # From (static/images/logo/)
---
## Due Date - November 27, 2020, 10PM CST
___
**Objectives**
___

1. Learn to break down a very complex problem into smaller problems

2. Solve each smaller problem and bring them together to solve the larger problem

3. Learn how CDNs work and build your own CDN

___
**Overview**
___
<br>


![overview](/csc4200/img/cdn-load-balancer.png)

<br>

In this project, you are going to build on the first and the second project. You will build your own "CDN load-balancer". A cloud typically hosts multiple copies (replicas) of the same content. Depending on where the request is coming from, it routes the requests a suitable replica.  A primary component of any CDN is the entity called a load-balancer. The function of a load-balancer is route requests to the "most suitable" server. CDNs choose their own metric for defining which server is the most suitable. It can be the replica with the lowest latency, the replica with lowest loss, or a combination of multiple parameters.

<br>

In this exercise, you will create three replicas with the same content. You will also keep track of the delay and loss parameters to each replica. At the beginning, each replica will download some content from a website. When a request comes in, you will redirect the request to the most suitable replica (see the definition below), download the content, and close the connection. When the next request comes in, you will redirect that request to the most suitable replica at that time. The network conditions will change throughout the experiment.

<br>

The client and server communications may use TCP or UDP.
<br>

<br>
___
**Replica Server Specifications**
___
The server takes two arguments:

```
$ replicaserver -p <PORT> -s <LOG FILE LOCATION> -p <web page to download>
```

1.```PORT``` - The port server listens on.

2.```Log file location``` - Where you will keep a record of actions.

3.```p``` - Which webpage to download and serve.

For example:

```
$ replicaserver -p 30000 -l /tmp/logfile -p www.nytimes.com
```
___
Functional requirements
___
   1. The server must open a TCP/UDP socket on the specified port number
   2. The server should gracefully process incorrect port number and exit with a non-zero error code
   4. The server should download the file specified by -p and save it to the memory



___
***Load Balancer Specifications***
___
<br>

```
$ loadbalancer -s <SERVER-IP> -p <PORT> -l LOGFILE
```

The load balancer takes three arguments:

1.```Server IPs``` - A list of replica servers' IP addresses

2.```PORT``` - The port the servers listen on. They will all listen to the same port

2.```Log file location``` - Where you will keep a record of packets you received.


```
For example:
$ loadbalancer -s replica_servers.txt -p 6543 -l LOGFILE
```
<br>
___
Protocol Specifications:
___

1. Design your own protocol headers for most efficient communication between the load-balancer and the replicas
2. The client should connect to the replica server that has the highest preference.
3. We define the preference as lowest combined value of weighed delay and loss. Lower value wins.
4. Preference = 0.75*loss percentage + 0.25*delay in milliseconds
5. The load-balancer should probe the replica servers periodically and keep a list of preferences. You should be able to use a ping like program for this part.
5. The load-balancer should be able to accept and process multiple connection from clients at the same time

___
***Client Specifications***
___
<br>

```
$ anonclient -s <load-balancer-IP> -p <PORT> -l LOGFILE
```

The client takes three arguments:

1.```load-balancer IP``` - The IP address of the load-balancer.

2.```PORT``` - The port the server listens on.

2.```Log file location``` - Where you will keep a record of packets you received.


```
For example:
$ anonclient -s 192.168.2.1 -p 6543 -l LOGFILE
```

___
**Client Requirements**
___
1. The client will simply open a connection to the load-balancer and request a content
2. Design your own protocol headers for most efficient communication between the client and the load-balancer
1. The client should be able to receive the content and write to a file
2. The client should gracefully process incorrect port number and exit with a non-zero error code (you can assume that the folder is always correct). In addition to exit, the client must print out on standard error (std::cerr) an error message that starts with ERROR: string.

___
**Additional requirements:**
___
1. Code must compile/run on Google Cloud Ubuntu VM (18.04) - we will test your code only on the VM.
2. For each packet received, log interaction at the load-balancer in the following format:
```
Request from <CLIENT IP> for  <URL>. Redirecting to <Replica IP>, Preference <Preference>, Next Preference was <Next lowest preference> to <Replica IP>
Response from <Replica IP>, sending request to <Client IP>

```

3. If error occurs: log the following:
```
"Error: Unable to handle request between <Client IP>, <Replica IP>, <Preference>, <Error details>
```

4. Set the loss and delay using these commands:
```
tc qdisc add dev <ethernet device, e.g, eth0> root netem delay 200ms
tc qdisc add dev <ethernet device, e.g, eth0> root netem loss 20%
tc qdisc del dev eth0
```
