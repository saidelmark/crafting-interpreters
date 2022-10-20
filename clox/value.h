#ifndef CLOX_VALUE_H
#define CLOX_VALUE_H

#include "common.h"
typedef double Value;

typedef struct {
  int capacity; // allocated space
  int count; // used space
  Value* values;
} ValueArray;

void initValueArray(ValueArray* array);
void writeValueArray(ValueArray* array, Value value);
void freeValueArray(ValueArray* array);
void printValue(Value value);

#endif
