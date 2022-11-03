CC = clang
BUILD_DIR := build
NAME=clox
DNAME=cloxd
debug:
	@ $(MAKE) -f c.make NAME=$(DNAME) MODE=debug SOURCE_DIR=. CC=$(CC)
clox:
	@ $(MAKE) -f c.make NAME=$(NAME) MODE=release SOURCE_DIR=. CC=$(CC)
	@ cp build/$(NAME) $(NAME) # For convenience, copy the interpreter to the top level.

run: clox
	./$(NAME)

rund: debug
	./build/$(DNAME)

clean:
	@ rm -rf $(BUILD_DIR)
	@ rm -rf $(NAME)

.PHONY: clox clean debug
