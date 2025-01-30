# About
Experiementation of Assembly interpreter, following the [whitespace interpreter](https://github.com/AndycptSher/RagTagBunch/tree/main/src/whitespace_interpreter)

split into 3 attempts, where the latter 2 were never finished,

## 1. [`asmSim.py`](https://github.com/AndycptSher/RagTagBunch/blob/main/src/replit/languages/asmSim.py)

The goal of this was to create a interpreter that takes in an "assembly" program and execute the program sequentially adn interface with a memory object.

This was matovated by the desire to seperate the "magic" that was presented along with the basic concept of assembly

> Magic being, a dedicated memory and console line that is associated with the machine
>
> So in the program, the typical printed output is seperated out to a seperate object which the interpreter only interacts via 1 method, and any further logic can be independantly modified once in that method
## 2. [`asmSim1.py`](https://github.com/AndycptSher/RagTagBunch/blob/main/src/replit/languages/asmSim1.py)

The goal of this attempt was to also represent the processer down to the register level, so the instructions jump, branch, and instruction fetching can be realized as bits moving as opposed to higher level control flow and heap retrieval

Or it could be said that the goal was to create a processor that performs the fetch decode execute cycle

There were many questions that popped up during the process of writing the code, and this can be noted with the various sources and links scattered throughout the code comments

There was a tedious search for an elegant solution for implementing the calling and returning instructions,
In the end, the ideal solution (call stack) was delayed as I had moved on to my [NEA](https://github.com/AndycptOrg/NEA-Calculator)

The main problem(remaining)(when I returned) was relating to communicating with any expernal attatchments (kernal, pcie ports, usb, etc)
## 3. [`asmSim2.py`](https://github.com/AndycptSher/RagTagBunch/blob/main/src/replit/languages/asmSim2.py)

This was a brief attempt at creating a unified interface that could allow different implementations of memory and other lower level objects that can be interchangable when being executed

