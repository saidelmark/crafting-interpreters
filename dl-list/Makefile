RESULT ?= ./result.out
BUILD_ARGS ?= ""

build: main.c list.c
	clang --std=c99 -Wall main.c -o $(RESULT) $(BUILD_ARGS)

build_sanitize:
	BUILD_ARGS="-fsanitize=leak -fno-omit-frame-pointer" $(MAKE) build

run: build
	$(RESULT)

run_sanitize: build_sanitize
	$(RESULT)

clean:
	rm -f *.out

valgrind: build
	valgrind --tool=memcheck --leak-check=full $(RESULT)

