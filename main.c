#include <stdlib.h>
#include "list.c"

int main(int count, char *argv[]) {
	push("some first item");
	push("another item");
	push("one more item");
	append("the last item");
	printList();
	printRevList();
	char* popped = pop();
	printf("popped \"%s\"\n", popped);
	free(popped);
	char* trimmed = trim();
	printf("trimmed \"%s\"\n", trimmed);
	free(trimmed);
	deleteByValue("another item");
	printList();
	destroy();
	printList();
	return 0;
}
