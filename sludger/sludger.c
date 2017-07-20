#include <stdio.h>
#include <string.h>
#include <unistd.h>

#include <arpa/inet.h>

#include "networking.h"
#include "structs.h"
#include "libscrypt.h"

/*

This is just a demo of the scrypt system that is used for drying sludge.
Note that the output is binary, so it should be piped to a hexdump-like
application.

*/

int main(void)
{
	int isludge = listen_incoming("4444");
	if(isludge < 0) {
		perror("Could not listen upstream");
		return -1;
	}

	int new_stream = 0;
	while((new_stream = accept_incoming(isludge))) {
		struct header head;

		ssize_t received_bytes = read(new_stream, &head, sizeof(head));
		if(received_bytes < 0) {
			perror("Could not read header");
			close(new_stream);
			continue;
		}
		if((size_t)received_bytes < sizeof(head)) {
			// TODO: Should log this and send a report packet
			fprintf(stderr, "Did not receive a full header (%zd/%zu)\n",
					received_bytes, sizeof(head));
			close(new_stream);
			continue;
		}

		// This is the only place where a ntoh_ call is needed
		size_t items = (ntohs(head.size) - sizeof(head))/8;
        size_t type = ntohs(head.type);
        printf("Type: %d\n", type);
        printf("Number of items: %zd\n", items);
		// Leave the last node as a nice all-0 node
		//struct node *payload = calloc(items+1, sizeof(payload));
		received_bytes = 0;

		// Read in the entire payload
        struct node *buf_node = calloc(1, sizeof(struct node));
        llnode * str_list = NULL;
		do {
			//ssize_t amt = read(new_stream, &((char *)payload)[8 + received_bytes], items*8 - received_bytes);

            ssize_t amt = read(new_stream, buf_node, sizeof(buf_node));
			if(amt < 0) {
				// TODO: Should log this and send a report packet
				fprintf(stderr, "Did not receive a entire packet\n");
				goto done;
			}
			received_bytes += amt;

            char * string = malloc(64); //Fix magic number
            string[0] = '\0';
            snprintf(string, sizeof(string), "%u", ntohl(buf_node->data));
            str_list = add_to_list(str_list, (void *)string);

		} while((size_t)received_bytes < items*8);

    //Create all the hashes and put them in a linked list
    llnode * hash_list = NULL;
    for(size_t i = 0; i < items; i++) {
        void * buf;

        char * input = NULL;
     
        buf = deconstruct_list_step(&str_list);

        input = (unsigned char *)buf;

        printf("''%s''\n", input);
        struct hash * new_hash = calloc(1, sizeof(struct hash));
        int ret = libscrypt_scrypt(input, strlen(input), salt, strlen(salt),
            2048, 4, 4,
            new_hash->code, sizeof(new_hash->code));

        free(input);
        hash_list = add_to_list(hash_list, (void *)new_hash);
    }

    //Write function to double check str_list free

    //Pull out the hashes and send them one by one (Eventually switch to a single
    // header)
    for(size_t i = 0; i < items; i++) {
        void * buf;
        buf = deconstruct_list_step(&hash_list);
        buf = (struct hash *)buf;

        struct header head;
        uint16_t two = 2;
        head.type = htons(two);
        head.size = htons(sizeof(head) + sizeof(struct hash));

        int osludge = connect_outgoing("downstream", "4444");
        if(osludge < 0) {
            perror("Could not connect downstream");
            goto done;
        }

        write(osludge, &head, sizeof(head));
        write(osludge, buf, sizeof(struct hash));
        close(osludge);

        free(buf);       
    }

done:
        //Deconstruct strlist
        free(buf_node);
        close(new_stream);
    }


}
