#include <stdlib.h>
#include "list.c"

int main(int count, char *argv[]) {
	push(1);
	push(2);
	push(3);
	append(5);
	printList();
	printRevList();
	pop();
	trim();
	printList();
	destroy();
	printList();
	return 0;
}
