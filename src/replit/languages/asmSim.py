"""
instructions
LDR reg, mem ref
STR reg, mem ref
ADD reg, reg, reg/operand
SUB reg, reg, reg/operand
MOV reg, reg/operand
CMP reg, reg/operand
B label
B condition, label
AND reg, reg, reg/operand
OR reg, reg, reg/operand
XOR reg, reg, reg/operand
NOT reg, reg
LSL reg, reg, reg/operand
LSR reg, reg, reg/operand
"""



from collections.abc import Iterable
from typing import Any


class arrayMonad(list):
  def __init__(self, array: list, ty):
    super(arrayMonad, self).__init__(array)
    self._type: Any = ty

  def flatmap(self, f):
    assert type(f(self._type())) == list
    return arrayMonad(sum(map(f, super(arrayMonad, self).__iter__()), []), self._type)
    
  def returnContents(self):
    return super(arrayMonad, self).copy()


class outputBuffer:
  def __init__(self):
    self._buffer = []
    self._persist = []

  def add(self, it: Iterable|Any) -> None:
    if type(it) != Iterable:
      if len(self._buffer) >= 20:
        self.flush()
        self._buffer = []
      self._buffer.append(it)
      return
    for i in it:
      if len(self._buffer) >= 20:
        self.flush()
        self._buffer = []
      self._buffer.append(i)
  def flush(self):
    print("\noutputting:", *self._buffer)
    self._persist += self._buffer
    self._buffer = []

  def showHistory(self):
    print(*self._persist)

    
class Memory:
  """
  representation of memory hardware
  each index stores a byte in the form of an int
  """
  def __init__(self, size:int=50):
    self._memory = [0 for _ in range(size)]
    self._maxIndex = size

  def isValidAddress(self, index: int) -> bool:
    return (0 <= index < self._maxIndex)

  def __setitem__(self, index: int, item: int) -> bool:
    if not self.isValidAddress(index):
      raise IndexError("Index must be within bounds")
    if not (0 <= item <= 255):
      raise ValueError("item integer must be representable with a byte")
    self._memory[index] = item
    return True

  def __getitem__(self, index:int) -> int:
    if not self.isValidAddress(index):
      raise IndexError("Index must be within bounds")
    return self._memory[index]

  def __str__(self, lineLen=4):
    return " ".join(
      [("\n" if not i%4 else "")+
       f"{x:0>3}" 
       for i,x in enumerate(self._memory)
      ])


print(arrayMonad([1, 2, 3, 4, 5], int)
      .flatmap(lambda x: [x, x])
      .flatmap(lambda a: [] if (a%2==0) else [a])
      .returnContents())


def run(inp: str, mem:Memory=Memory(10), display_steps:bool=False):
  # sanitizing input
  instructions: list[str] = (arrayMonad(inp.split("\n"), str)
                             # filtering out comments
                             .flatmap(lambda a: a.split("/",1)[:1])
                             # splitting up labels into their own lines
                             .flatmap(lambda a: 
                                      (lambda b, *c: [b+(":" if c else ""), *c])
                                      (*a.split(":", 1)))
                             # filtering out blanks
                             .flatmap(lambda a: [] if not a else [a])
                             # removing whitespace at the ends
                             .flatmap(lambda a: [a.strip()])
                             .returnContents())
  if display_steps:
    print(*instructions, sep="\n")
  # don't try to solve the halting problem
  # indexing labels
  labels = {}
  for line_num, line in enumerate(instructions):
    if line.endswith(":"):
      labels[line[:-1]] = line_num


  program_counter = 0
  class Registers(list):
    def __init__(self, numOfReg:int):
      if numOfReg <= 0:
        raise ValueError("there should be a positive number of registers")
      super(Registers, self).__init__([0 for _ in range(numOfReg)])
    def __setitem__(self, index: int, item: int) -> None:
      if not (0 <= item < 256):
        raise ValueError("item must be representable by a byte")
      super(Registers, self).__setitem__(index, item)

  registers = Registers(8)
  output_buffer = outputBuffer()
  if display_steps: print("Labels", labels)

  
  class ValueStore:
    def getValue(self) -> int:
      """
      Virtual method to be overridded by subclasses
      """
      raise NotImplementedError("not implemented")
      pass
  
  class Register(ValueStore):
    def __init__(self, num:int):
      if not (0 <= num < 8):
        raise IndexError("Index must be within bounds")
      self._index = num

    def getValue(self) -> int:
      return registers[self._index]

    def __str__(self) -> str:
      return f"R{self._index}"

  class Literal(ValueStore):
    def __init__(self, num: int) -> None:
      if not (0 <= num < 256):
        raise ValueError(str(num)+"num must be representable by a byte")
      self._value = num

    def getValue(self) -> int:
      return self._value

  # flags
  flags = [
    # less than
    False,
    # greater than
    False,
    # equal to
    False,
  ]
  LESS_THAN = 0
  GREATER_THAN = 1
  EQUAL_TO = 2
  
  while instructions[program_counter].lower() != "halt":
    # lexer
    line = instructions[program_counter].split(" ", 1)
    # splits up operands
    if len(line) > 1:
      line = [line[0].lower(), *(line[1].replace(" ", "").lower().split(","))]

    ops: list[str|int|Register|Literal] = []
    for term in line:
      if term[0] == "r":
        ops.append(Register(int(term[1:])))
      elif term[0] == "#":
        ops.append(Literal(int(term[1:])))
      elif term.isdecimal():
        # implied only mem address is int
        if not mem.isValidAddress(int(term)):
          raise ValueError("memory address must be within bounds")
        ops.append(int(term))
      else:
        ops.append(term)
        
    
    # print(ops)
    # parser (ik it's very lazy, it was to test the match case functionality)
    match ops:
      case [str(label)] if label[-1] == ":":
        if display_steps: print("label encountered")
        pass
      case ["ldr", Register(_index = id), (int()|Register()) as op1]:
        match op1:
          case int(op1):
            if display_steps: print(f"loading from memory address {op1} into register {id}")
            registers[id] = mem[op1]
          case Register(_index = id1):
            if display_steps: print(f"loading from memory address in register {id1} into register {id}")
            registers[id] = int(mem[registers[id1]])
        pass
      case ["str", Register(_index = id), int(address)]:
        if display_steps: print(f"storing register {id} into memory address {address}")
        mem[address] = registers[id]
        pass
      case ["add", Register(_index = id1), Register(_index = id2),\
            (Register(_index = id3)|Literal(_value=id3)) as third]:
        if display_steps: print(f"adding from register {id2} and {type(third).__name__} {id3} to register {id1}")
        registers[id1] = registers[id2] + third.getValue()
        pass
      case ["sub", Register(_index = id1), Register(_index = id2),\
          (Register(_index = id3)|Literal(_value=id3)) as third]:
        if display_steps: print(f"subtracting {type(third).__name__} {id3} from register {id2} to register {id1}")
        registers[id1] = registers[id2] - third.getValue()
        pass
      case ["mov", Register(_index = id1),\
          (Register(_index = id2)|Literal(_value=id2)) as second]:
        if display_steps: print(f"moving {type(second).__name__} {id2} to register {id1}")
        registers[id1] = second.getValue()
        pass
      case ["cmp", Register(_index = id1),\
            (Register(_index = id2)|Literal(_value=id2)) as second]:
        if display_steps: print(f"comparing register {id1} and {type(second).__name__} {id2}")
        v1 = registers[id1]
        v2 = second.getValue()
        if v1 < v2:
          flags = [True, False, False]
        elif v1 > v2:
          flags = [False, True, False]
        else:
          flags = [False, False, True]
        pass
      case ["b", str(label)]:
        if display_steps: print(f"jumping to label \"{label}\"")
        program_counter = labels[label]
        pass
      case ["beq"|"bne"|"blt"|"bgt"|"bge"|"ble" as condition, str(label)]:
        if display_steps: print(f"jumping to label \"{label}\" if {condition[1:]}")
        do_jump = False
        match condition[1:]:
          case "eq":
            do_jump = flags[EQUAL_TO]
          case "ne":
            do_jump = not flags[EQUAL_TO]
          case "lt":
            do_jump = flags[LESS_THAN]
          case "gt":
            do_jump = flags[GREATER_THAN]
          case "ge":
            do_jump = flags[GREATER_THAN] or flags[EQUAL_TO]
          case "le":
            do_jump = flags[LESS_THAN] or flags[EQUAL_TO]
        if do_jump:
          program_counter = labels[label]
        pass
      case ["and", Register(_index = id1), Register(_index = id2), (Register(_index = id3)|Literal(_value = id3)) as val]:
        if display_steps: print(f"performing bitwise and on register {id2} and {type(val).__name__} {id3} to register {id1}")
        registers[id1] = registers[id2] & val.getValue()
        pass
      case ["or", Register(_index = id1), Register(_index = id2), (Register(_index = id3)|Literal(_value = id3)) as third]:
        if display_steps: print(f"performing bitwise or on register {id2} and {type(third).__name__} {id3} to register {id1}")
        registers[id1] = registers[id2] | third.getValue()
        pass
      case ["xor", Register(_index = id1), Register(_index = id2), (Register(_index = id3)|Literal(_value = id3)) as third]:
        if display_steps: print(f"performing bitwise xor on register {id2} and {type(third).__name__} {id3} to register {id1}")
        registers[id1] = registers[id2] ^ third.getValue()
        pass
      case ["not", Register(_index = id1), (Register(_index = id2)|Literal(_value = id2)) as second]:
        if display_steps: print(f"performing bitwise not on register {id2} to register {id1}")
        registers[id1] = ~second.getValue()
        pass
      case ["lsl", Register(_index = id1), Register(_index = id2), (Register(_index = id3)|Literal(_value = id3)) as third]:
        if display_steps: print(f"performing bitwise left shift on register {id2} by the value of  {type(third).__name__} {id3} to register {id1}")
        registers[id1] = registers[id2] << third.getValue()
        pass
      case ["lsr", Register(_index = id1), Register(_index = id2), (Register(_index = id3)|Literal(_value = id3)) as third]:
        if display_steps: print(f"performing bitwise right shift on register {id2} by the value of  {type(third).__name__} {id3} to register {id1}")
        registers[id1] = registers[id2] >> third.getValue()
        pass
      case ["out", Register(_index = id), int(magic_num)]:
        if display_steps: print(f"putting contents of register {id} to outputBuffer")
        NUMBER = 4
        SIGNED_NUMBER = 5
        HEX = 6
        ALPHABET = 7
        
        if magic_num == NUMBER:
          output_buffer.add(registers[id])
        elif magic_num == SIGNED_NUMBER:
          num = registers[id]
          output_buffer.add((num//128)*-128 + num%128)
        elif magic_num == HEX:
          output_buffer.add(hex(registers[id])[2:])
        elif magic_num == ALPHABET:
          output_buffer.add(chr(registers[id]))
        else:
          output_buffer.add(registers[id])
        pass
      case ["stall"]:
        import time
        time.sleep(1)
      case [*instructions]:
        raise Exception(f"{instructions} is not a valid instruction")
        
      case _:
        if display_steps: print("gotta catch em all!")
    
    if display_steps: print(registers)
    program_counter += 1
    
  # flush out the buffer at end of program
  output_buffer.flush()
  return output_buffer

memory = Memory(10)
memory[4] = 132
run(
"""LDR R1, 4
MOV r0, #3 //abhek /a 
AND r3, r0, r1
// this will be gone, poof, disappear
loop:CMP r0,r1  / this is an inline comment
BLT out 
SUB r0,r0,#1
B loop
out:
OUT r0,4
HALT
""", memory)
print(memory)

run("""
HALT
// loops through all the numbers from 0 to 255 testing the OUT opcode
mov r0, #0
MOV r1, #0
loop: CMP r0, #255
BEQ stop
ADD r0, r0, #1
OUT r0, 4
OUT r0, 5
OUT r0, 6
OUT r0, 7
B loop
stop:


HALT

""", memory).showHistory()

run("""
loop:
MOV r0, #7 //bell character
OUT r0, 7
stall
OUT r0, 4
halt
B loop
HALT""")


