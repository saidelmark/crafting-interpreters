#include "chunk.h"
#include "common.h"
#include "debug.h"

int main(int argc, const char* argv[]) {
	Chunk chunk;
	initChunk(&chunk);

	int constant1 = addConstant(&chunk, 1.2);
	writeChunk(&chunk, OP_CONSTANT, 123);
	writeChunk(&chunk, constant1, 123);

	int constant2 = addConstant(&chunk, 1.3);
	writeChunk(&chunk, OP_CONSTANT, 124);
	writeChunk(&chunk, constant2, 124);

	writeChunk(&chunk, OP_RETURN, 124);
	disassembleChunk(&chunk, "test chunk");
	freeChunk(&chunk);
	return 0;
}
