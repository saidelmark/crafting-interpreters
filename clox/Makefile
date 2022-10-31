CC = clang
BUILD_DIR := build
NAME=clox
debug:
	@ $(MAKE) -f c.make NAME=cloxd MODE=debug SOURCE_DIR=. CC=$(CC)

clox:
	@ $(MAKE) -f c.make NAME=$(NAME) MODE=release SOURCE_DIR=. CC=$(CC)
	@ cp build/$(NAME) $(NAME) # For convenience, copy the interpreter to the top level.

run: clox
	./$(NAME)

clean:
	@ rm -rf $(BUILD_DIR)
	@ rm -rf clox

.PHONY: clox clean debug
