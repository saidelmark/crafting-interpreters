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

struct List {
	NodePtr first;
	NodePtr last;
} List;

typedef struct List* ListPtr;

ListPtr newList() {
	ListPtr list = (ListPtr) malloc(sizeof(List));
	if (list != NULL) {
		list->first = NULL;
		list->last = NULL;
	}
	return list;
}

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
	if (node != NULL) {
		node->value = strdup(s);
		node->next = NULL;
		node->prev = NULL;
	}
	return node;
}

bool isEmpty(ListPtr list) {
	return list->first == NULL;
}

void push(ListPtr list, char*  x) {
	NodePtr node = newNode(x);
	if (isEmpty(list)) {
		list->first = node;
		list->last = node;
	} else {
		node->next = list->first;
		list->first->prev = node;
		list->first = node;
	}
}

void append(ListPtr list, char*  x) {
	NodePtr node = newNode(x);
	if (isEmpty(list)) {
		list->last = node;
		list->first = node;
	} else {
		node->prev = list->last;
		list->last->next = node;
		list->last = node;
	}
}

// WARNING: this function returns a heap-allocated string.
// It's you responsibility to deallocate the memory.
char* pop(ListPtr list) {
	char* nodeValue = NULL;
	if (!isEmpty(list)) {
		nodeValue = list->first->value;
		if (list->first->next != NULL) {
			list->first->next->prev = NULL;
		}
		NodePtr second = list->first->next;
		list->first->next = NULL;
		free(list->first);
		list->first = second;
		list->first->prev = NULL;
	}
	return nodeValue;
}

// WARNING: this function returns a heap-allocated string.
// It's you responsibility to deallocate the memory.
char* trim(ListPtr list) {
	char* nodeValue = NULL;
	if (!isEmpty(list)) {
		nodeValue = list->last->value;
		if (list->last->prev != NULL) {
			list->last->prev->next = NULL;
		}
		NodePtr pre_last = list->last->prev;
		list->last->prev = NULL;
		free(list->last);
		list->last = pre_last;
		list->last->next = NULL;
	}
	return nodeValue;
}

void destroy(ListPtr list) {
	for (NodePtr current = list->first; !isEmpty(list); current = list->first) {
		list->first = list->first->next;
		current->next = NULL;
		current->prev = NULL;
		free(current->value);
		free(current);
	}
	free(list);
}

void deleteNode(ListPtr list, NodePtr node) {
	if (node == NULL) {
		return;
	}
	NodePtr prev = node->prev;
	NodePtr next = node->next;
	if (node == list->first) {
		list->first = next;
	} else {
		prev->next = next;
	}
	if (node == list->last) {
		list->last = prev;
	} else {
		next->prev = prev;
	}
	free(node->value);
	free(node);
}

NodePtr findNode(ListPtr list, char* query) {
	NodePtr result = NULL;
	for (NodePtr node = list->first; node != NULL; node = node->next) {
		if (!strcmp(query, node->value)) {
			result = node;
		}
	}
	return result;
}

void deleteByValue(ListPtr list, char* query) {
	deleteNode(list, findNode(list, query));
}

int lentgh(ListPtr list) {
	int result;
	NodePtr current = list->first;
	for (result = 0; current != NULL; current = current->next) {
		result++;
	}
	return result;
}

void printList(ListPtr list) {
	printf("[ ");
	NodePtr current = list->first;
	for (; current != NULL; current = current->next) {
		printf("\"%s\", ", current->value);
	}
	printf("]\n");
}

void printRevList(ListPtr list) {
	printf("[ ");
	NodePtr current = list->last;
	for (; current != NULL; current = current->prev) {
		printf("\"%s\", ", current->value);
	}
	printf("]\n");
}
