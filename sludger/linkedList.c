#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct llnode
{
    void * data;
    struct llnode * next;
} llnode;

void print_list(llnode * root)
{
    printf("%d\n", root->data);
    if (root->next)
    {
        print_list(root->next);
    }
}

bool find_val(llnode * root, int data)
{
    llnode * cursor = root;
    while(cursor)
    {
        if(cursor->data == data)
        {
            return true;
        }
        else
        {
            cursor = cursor->next;
        }
    }
    return false;
}

llnode * remove_head(llnode * root)
{
    llnode * tmp = root;
    if(root->next)
    {
        root = root->next;
    }
    else
    {
        printf("List only has one element, returning NULL\n");
        return NULL;
    }
    free(tmp);

    return root;
}

llnode * add_to_list(llnode * root, int data)
{
    llnode * newllnode = malloc(sizeof(llnode));
    newllnode->data = data;
    newllnode->next = NULL;

    if (root == NULL)
    {
        root = newllnode;                
    }
    else
    {
        llnode * cursor = root;
        while (cursor->next != NULL)
        {
            cursor = cursor->next;
        }
        cursor->next = newllnode;
    }

    return root;
}

void deconstruct_list(llnode * root)
{
    llnode * cursor;

    while(root != NULL)
    {
        cursor = root;
        root = root->next;
        free(cursor);
    }
}
