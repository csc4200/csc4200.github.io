#include <stdio.h>

#include <stdlib.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>
#define PORT 9999

#pragma pack (1)
struct packet_with_message
{
	int version;
  int message_type;
  int message_length;
  char message[8]={0};
};
#pragma pack (0)



void create_packet(int version, int message_type, char *message, struct packet_with_message **packet);

void create_packet(int version, int message_type, char *message, struct packet_with_message **packet) {

    struct packet_with_message *new_pkt;
    new_pkt = (packet_with_message*) malloc(sizeof(struct packet_with_message));
    new_pkt->version = htons(version);
    new_pkt->message_type = message_type;
    new_pkt->message_length = strlen(message);
    strcpy(new_pkt->message, message);
    *packet = new_pkt;
}


int main(int argc, char const *argv[])
{
    int sock = 0, valread;
    struct sockaddr_in serv_addr;
    char buffer_pkt[12] = {0};
    char buf_msg[8] = {0};
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        printf("\n Socket creation error \n");
        return -1;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    if(inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr)<=0)
    {
        printf("\nInvalid address/ Address not supported \n");
        return -1;
    }

    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        printf("\nConnection Failed \n");
        return -1;
    }

    //send_hello()
    struct packet_with_message *hello_pkt = NULL;
    create_packet(17, 1, "hello", &hello_pkt);
    printf("Sending Version:%d, Message type:%d, Message Length:%d, msg=%s\n", ntohs(hello_pkt->version), hello_pkt->message_type, hello_pkt->message_length, hello_pkt->message);
    send(sock , hello_pkt , 20 , 0 ); //send packet_with_message

//    create_hello_packet();

    //receive hello(), check version 17

    //send command

    //shutdown

//
//    packet_with_message pkt;
//    pkt.version = 17;
//    pkt.message_type = 0;
//    pkt.message_length = 6;
//    strcpy(pkt.message,"HELLO");
//
//    send(sock , &pkt , 20 , 0 ); //send packet_with_message
////    send(sock , hello , 5 , 0 ); //send message
//    printf("Hello message sent\n");
//
//    packet_with_message recv_pkt;
//    valread = recv(sock , &recv_pkt, 12,0);
//    printf("Version:%d, Message type:%d, Message Length:%d\n", pkt.version, pkt.message_type, pkt.message_length);
//    valread = recv(sock , buf_msg, pkt.message_length,0); //read packet
//    printf("Version:%d, Message type:%d, Message Length:%d msg:%s\n", pkt.version, pkt.message_type, pkt.message_length, buf_msg);
//
////    valread = read( sock , buffer, 1024);
//    printf("%s\n",buffer );
    return 0;
}
