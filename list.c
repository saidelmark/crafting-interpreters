#include<stdio.h>
#include<stdlib.h>
#include<stdbool.h>

// This is the main type I'll be working with,
// not with nodes themselves but with pointers to them
typedef struct Node* NodePtr;

struct Node {
	int value;
	NodePtr next;
	NodePtr prev;
};


// Global variables, pointers to both ends of the list
NodePtr first;
NodePtr last;

// Create a new node with given value.
// Later this node can be inserted into any place of the list
NodePtr newNode(int x) {
	NodePtr node = (NodePtr)malloc(sizeof(struct Node));
	node->value = x;
	node->next = NULL;
	node->prev = NULL;
	return node;
}

bool isEmpty() {
	return first == NULL;
}

void push(int x) {
	NodePtr node = newNode(x);
	if (isEmpty()){
		first = node;
		last = node;
	} else {
		node->next = first;
		first->prev = node;
		first = node;
	}
}

void append(int x) {
	NodePtr node = newNode(x);
	if (isEmpty()) {
		last = node;
		first = node;
	} else {
		node->prev = last;
		last->next = node;
		last = node;
	}
}

int* pop() {
	int* item = NULL;
	if (!isEmpty()) {
		item = &first->value;
		if (first->next != NULL) {
			first->next->prev = NULL;
		}
		NodePtr second = first->next;
		free(first);
		first = second;
	}
	return item;
}

int* trim() {
	int* item = NULL;
	if (!isEmpty()) {
		item = &last->value;
		if (last->prev != NULL) {
			last->prev->next = NULL;
		}
		NodePtr pre_last = last->prev;
		free(last);
		last = pre_last;
	}
	return item;
}

// Doesn't take any args as long as there's only one list,
// the one that `first` points to.
// Onece I abstract away from `first`, `length` should take a `Node* list` as an arg
int lentgh() {
	int result;
	NodePtr current = first;
	for (result = 0; current != NULL; current = current->next) {
		result++;
	}
	return result;
}

void printList() {
	printf("[ ");
	NodePtr current = first;
	for (; current != NULL; current = current->next) {
		printf("%d", current->value);
	}
	printf("]\n");
}

void printRevList() {
	printf("[ ");
	NodePtr current = last;
	for (; current != NULL; current = current->prev) {
		printf("%d", current->value);
	}
	printf("]\n");
}
