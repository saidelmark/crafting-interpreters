RESULT ?= ./result.out

build:
	clang --std=c99 -Wall main.c -o $(RESULT)

run:
	$(RESULT)

clean:
	rm -f *.out

check:
	valgrind --tool=memcheck --leak-check=full $(RESULT)

