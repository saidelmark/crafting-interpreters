#include<stdio.h>
#include<stdlib.h>
#include<stdbool.h>
#include<string.h>

// This is the main type I'll be working with,
// not with nodes themselves but with pointers to them
typedef struct Node* NodePtr;

struct Node {
	char* value;
	NodePtr next;
	NodePtr prev;
};


// Global variables, pointers to both ends of the list
NodePtr first, last;

// Duplicate a string
char* strdup(char* str) {
	char* str_d = (char*) malloc(strlen(str)+1);
	if  (str_d != NULL) {
		strcpy(str_d, str);
	}
	return str_d;
}

// Create a new node with given value.
// Later this node can be inserted into any place of the list
NodePtr newNode(char* s) {
	NodePtr node = (NodePtr)malloc(sizeof(struct Node));
	node->value = strdup(s);
	node->next = NULL;
	node->prev = NULL;
	return node;
}

bool isEmpty() {
	return first == NULL;
}

void push(char*  x) {
	NodePtr node = newNode(x);
	if (isEmpty()) {
		first = node;
		last = node;
	} else {
		node->next = first;
		first->prev = node;
		first = node;
	}
}

void append(char*  x) {
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

// WARNING: this function returns a heap-allocated string.
// It's you responsibility to deallocate the memory.
char* pop() {
	char* nodeValue = NULL;
	if (!isEmpty()) {
		nodeValue = first->value;
		if (first->next != NULL) {
			first->next->prev = NULL;
		}
		NodePtr second = first->next;
		first->next = NULL;
		free(first);
		first = second;
		first->prev = NULL;
	}
	return nodeValue;
}

// WARNING: this function returns a heap-allocated string.
// It's you responsibility to deallocate the memory.
char* trim() {
	char* nodeValue = NULL;
	if (!isEmpty()) {
		nodeValue = last->value;
		if (last->prev != NULL) {
			last->prev->next = NULL;
		}
		NodePtr pre_last = last->prev;
		last->prev = NULL;
		free(last);
		last = pre_last;
		last->next = NULL;
	}
	return nodeValue;
}

void destroy() {
	for (NodePtr current = first; !isEmpty(); current = first) {
		first = first->next;
		current->next = NULL;
		current->prev = NULL;
		free(current->value);
		free(current);
	}
}

void deleteNode(NodePtr node) {
	if (node == NULL) {
		return;
	}
	NodePtr prev = node->prev;
	NodePtr next = node->next;
	if (prev != NULL) {
		prev->next = next;
	} else {
		first = next;
	}
	if (next != NULL) {
		next->prev = prev;
	} else {
		last = prev;
	}
	free(node->value);
	free(node);
}

NodePtr findNode(char* query) {
	NodePtr result = NULL;
	for (NodePtr node = first; node != NULL; node = node->next) {
		if (!strcmp(query, node->value)) {
			result = node;
		}
	}
	return result;
}

void deleteByValue(char* query) {
	deleteNode(findNode(query));
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
		printf("\"%s\", ", current->value);
	}
	printf("]\n");
}

void printRevList() {
	printf("[ ");
	NodePtr current = last;
	for (; current != NULL; current = current->prev) {
		printf("\"%s\", ", current->value);
	}
	printf("]\n");
}
