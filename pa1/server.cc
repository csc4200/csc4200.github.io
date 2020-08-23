
// Server side C/C++ program to demonstrate Socket programming
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define PORT 9999

#pragma pack (1)
struct packet
{
	int version;
  int message_type;
  int message_length;
  char message[8];
};
#pragma pack (0)


int main(int argc, char const *argv[])
{
    int server_fd, new_socket, valread;
    struct sockaddr_in server_address, client_address;
    int opt = 1;
    int addrlen = sizeof(server_address);
    char buffer_pkt[12] = {0};
    char buf_msg[8] = {0};
    char *hello = "HELLO";

    // Creating socket file descriptor
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0)
    {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT,
                                                  &opt, sizeof(opt)))
    {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }
    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = INADDR_ANY;
    server_address.sin_port = htons( PORT );

    // Forcefully attaching socket to the port 8080
    if (bind(server_fd, (struct sockaddr *)&server_address,
                                 sizeof(server_address))<0)
    {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }
    if (listen(server_fd, 3) < 0)
    {
        perror("listen");
        exit(EXIT_FAILURE);
    }
    if ((new_socket = accept(server_fd, (struct sockaddr *)&client_address,
                       (socklen_t*)&addrlen))<0)
    {

        perror("accept");
        exit(EXIT_FAILURE);
    }
    printf("Received connection from %s port %d\n",
          inet_ntoa(client_address.sin_addr), ntohs(client_address.sin_port));


     //send hello


     //receive hello

     //receive command - do things

     //send SUCCESS

    packet pkt;
    valread = recv(new_socket , &pkt, 12,0); //read packet
    printf("Version:%d, Message type:%d, Message Length:%d\n", ntohs(pkt.version), pkt.message_type, pkt.message_length);
    valread = recv(new_socket , buf_msg, pkt.message_length,0); //read packet
    printf("Version:%d, Message type:%d, Message Length:%d msg:%s\n", pkt.version, pkt.message_type, pkt.message_length, buf_msg);
//    valread = recv(new_socket , buf_msg, 8,0);//read message
//    printf("Message: %s", buf_msg);

    strcpy(pkt.message, buf_msg);
    send(new_socket, &pkt, 20, 0); //send hello packet
 //   send(new_socket, buf_msg, 8, 0); //send hello message

    return 0;
}

