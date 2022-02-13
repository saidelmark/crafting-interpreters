#include <stdlib.h>
#include "list.c"

int main(int count, char *argv[]) {
	ListPtr list = newList();
	push(list, "some first item");
	push(list, "another item");
	push(list, "one more item");
	append(list, "the last item");
	printList(list);
	printRevList(list);
	deleteByValue(list, "the last item");
	char* popped = pop(list);
	printf("popped \"%s\"\n", popped);
	free(popped);
	char* trimmed = trim(list);
	printf("trimmed \"%s\"\n", trimmed);
	free(trimmed);
	deleteByValue(list, "another item");
	printList(list);
	destroy(list);
	return 0;
}
