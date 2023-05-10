#include <stdio.h>
#include "debug.h"
#include "value.h"

static char* instructionToStr(OpCode code) {
	switch (code) {
		case OP_CONSTANT: return "OP_CONSTANT";
		case OP_NOT: return "OP_NOT";
		case OP_NEGATE: return "OP_NEGATE";
		case OP_NIL: return "OP_NIL";
		case OP_TRUE: return "OP_TRUE";
		case OP_FALSE: return "OP_FALSE";
		case OP_POP: return "OP_POP";
		case OP_GET_LOCAL: return "OP_GET_LOCAL";
		case OP_SET_LOCAL: return "OP_SET_LOCAL";
		case OP_GET_GLOBAL: return "OP_GET_GLOBAL";
		case OP_DEFINE_GLOBAL: return "OP_DEFINE_GLOBAL";
		case OP_SET_GLOBAL: return "OP_SET_GLOBAL";
		case OP_EQUAL: return "OP_EQUAL";
		case OP_GREATER: return "OP_GREATER";
		case OP_LESS: return "OP_LESS";
		case OP_ADD: return "OP_ADD";
		case OP_SUBTRACT: return "OP_SUBTRACT";
		case OP_MULTIPLY: return "OP_MULTIPLY";
		case OP_DIVIDE: return "OP_DIVIDE";
		case OP_PRINT: return "OP_PRINT";
		case OP_JUMP: return "OP_JUMP";
		case OP_JUMP_IF_FALSE: return "OP_JUMP_IF_FALSE";
		case OP_LOOP: return "OP_LOOP";
		case OP_RETURN: return "OP_RETURN";
	}
}

void disassembleChunk(Chunk* chunk, const char* name) {
	printf("== %s ==\n", name);
	for (int offset = 0; offset < chunk->count;) {
		offset = disassembleInstruction(chunk, offset);
	}
}

static int simpleInstruction(OpCode code, int offset) {
	char* name = instructionToStr(code);
	printf("%s\n", name);
	return offset + 1;
}

static int byteInstruction(OpCode code, Chunk* chunk, int offset) {
	char* name = instructionToStr(code);
	uint8_t slot = chunk->code[offset + 1];
	printf("%-16s %4d\n", name, slot);
	return offset + 2;
}

static int jumpInstruction(OpCode code, int sign, Chunk* chunk, int offset) {
	char* name = instructionToStr(code);
	uint16_t jump = (uint16_t)(chunk->code[offset + 1] << 8);
	jump |= chunk->code[offset + 2];
	printf("%-16s %4d -> %d\n", name, offset,
		offset + 3 + sign * jump);
	return offset + 3;
}

static int constantInstruction(OpCode code, Chunk* chunk, int offset) {
	char* name = instructionToStr(code);
	uint8_t constant = chunk->code[offset+1];
	printf("%-16s %4d '", name, constant);
	printValue(chunk->constants.values[constant]);
	printf("'\n");
	return offset + 2;
}

int disassembleInstruction(Chunk* chunk, int offset) {
	printf("%04d ", offset);
	if (offset > 0 &&
		chunk->lines[offset] == chunk->lines[offset-1]) {
		printf("   | ");
	} else {
		printf("%4d ", chunk->lines[offset]);
	}
	uint8_t instruction = chunk->code[offset];
	switch (instruction) {
		case OP_CONSTANT:
			return constantInstruction(instruction, chunk, offset);
		case OP_NIL:
			return simpleInstruction(instruction, offset);
		case OP_TRUE:
			return simpleInstruction(instruction, offset);
		case OP_FALSE:
			return simpleInstruction(instruction, offset);
		case OP_POP:
			return simpleInstruction(instruction, offset);
		case OP_GET_LOCAL:
			return byteInstruction(instruction, chunk, offset);
		case OP_SET_LOCAL:
			return byteInstruction(instruction, chunk, offset);
		case OP_GET_GLOBAL:
			return constantInstruction(instruction, chunk, offset);
		case OP_DEFINE_GLOBAL:
			return constantInstruction(instruction, chunk, offset);
		case OP_SET_GLOBAL:
			return constantInstruction(instruction, chunk, offset);
		case OP_EQUAL:
			return simpleInstruction(instruction, offset);
		case OP_GREATER:
			return simpleInstruction(instruction, offset);
		case OP_LESS:
			return simpleInstruction(instruction, offset);
		case OP_ADD:
			return simpleInstruction(instruction, offset);
		case OP_SUBTRACT:
			return simpleInstruction(instruction, offset);
		case OP_MULTIPLY:
			return simpleInstruction(instruction, offset);
		case OP_DIVIDE:
			return simpleInstruction(instruction, offset);
		case OP_NOT:
			return simpleInstruction(instruction, offset);
		case OP_NEGATE:
			return simpleInstruction(instruction, offset);
		case OP_PRINT:
			return simpleInstruction(instruction, offset);
		case OP_JUMP:
			return jumpInstruction(instruction, 1, chunk, offset);
		case OP_JUMP_IF_FALSE:
			return jumpInstruction(instruction, 1, chunk, offset);
		case OP_LOOP:
			return jumpInstruction(instruction, -1, chunk, offset);
		case OP_RETURN:
			return simpleInstruction(instruction, offset);
		default:
			printf("Unknown opcode %d\n", instruction);
			return offset + 1;
	}
}
