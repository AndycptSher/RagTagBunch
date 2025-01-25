# About
This is the earliest work relating to interacting with the program text instead of the data and instructions a program conveys.

[Whitespace](https://en.wikipedia.org/wiki/Whitespace_(programming_language)) is a mainly stack based (imperative) programming langugage 
where the instructions closely resemble machine opcodes, 
in that they are restricted to only using 3 characters to represent all values and instructions.

This "project" feels like the precursor to/inspired [asmSim.py](https://github.com/AndycptSher/RagTagBunch/tree/main/src/replit/languages/asmSim.py)
, a program that executes a simple assembly instruction set
# How
The rules of the language is first embedded into a trie structure

> [Trie](https://en.wikipedia.org/wiki/Trie) is like a tree, but specifically used to describe search trees where the element to be searched is partioned into noded parts that can be shared with other elements in the seach space

When constructing the trie, the operation that 'opcode' represents is also passed in so when the instruction can be directly mapped to when retrived

> Implementation Note: an optional function can also be passed in, to parse remaining variable parts of an instruction
> namely, numbers and labels

Once the trie is constructed, the program is incrementally passed into the trie into an instruction and the un"parsed" part of the program.
The remianing program undergoes the same process until there is no more program text to parse.

This leaves us with a list of instructions(lambdas) to be executed.

> lambdas were used becuase of their lazy property, in that they will not execute unless called
