
// Server side C/C++ program to demonstrate Socket programming
#include <unistd.h>
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#define PORT 9999

struct header
{
	int version;
  int message_type;
  int message_length;
};


int main(int argc, char const *argv[])
{
    int server_fd, new_socket, valread;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    char buffer_hdr[12] = {0};
    char buf_msg[8] = {0};
    char *hello = "HELLO";

    // Creating socket file descriptor
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0)
    {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    // Forcefully attaching socket to the port 8080
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT,
                                                  &opt, sizeof(opt)))
    {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons( PORT );

    // Forcefully attaching socket to the port 8080
    if (bind(server_fd, (struct sockaddr *)&address,
                                 sizeof(address))<0)
    {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }
    if (listen(server_fd, 3) < 0)
    {
        perror("listen");
        exit(EXIT_FAILURE);
    }
    if ((new_socket = accept(server_fd, (struct sockaddr *)&address,
                       (socklen_t*)&addrlen))<0)
    {
        perror("accept");
        exit(EXIT_FAILURE);
    }

    header hdr;
    valread = recv(new_socket , &hdr, 12,0);
    printf("Version:%d, Message type:%d, Message Length:%d\n", hdr.version, hdr.message_type, hdr.message_length);
    valread = recv(new_socket , buf_msg, 8,0);
    printf("Message: %s", buf_msg);

//    memcpy(hdr.version, buffer_hdr, 4);
//    memcpy(hdr.message_type, buffer_hdr+4, 4);
//    memcpy(hdr.message_length, buffer_hdr+8, 4);

//    valread = read(new_socket , buffer_msg, 12);
//    printf("%s\n",buffer_msg);
//    send(new_socket , hello , strlen(hello) , 0 );
//    printf("Hello message sent\n");
    return 0;
}

