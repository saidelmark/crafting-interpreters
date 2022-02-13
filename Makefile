RESULT ?= ./result.out

build:
	clang --std=c99 -Wall main.c -o $(RESULT)

run: build
	$(RESULT)

clean:
	rm -f *.out

check: build
	valgrind --tool=memcheck --leak-check=full $(RESULT)

