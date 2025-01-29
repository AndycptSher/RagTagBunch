class Byte:
  def __init__(self, value:int):
    if not isinstance(value, int):
      raise TypeError("value must be an integer")
    if not (0 <= value < 256):
      raise ValueError("Value not within bounds")
    self._value = value

  def __lshift__(self, other):
    if not isinstance(other, int):
      raise TypeError("Shift amount must be an integer")
    if other < 0:
      raise ValueError("Shift amount must be non-negative")
    return Byte((self._value << other) & 255)

  def __rshift__(self, other):
    if not isinstance(other, int):
      raise TypeError("Shift amount must be an integer")
    if other < 0:
      raise ValueError("Shift amount must be non-negative")
    return Byte((self._value >> other) & 255)

  def __and__(self, other):
    if not isinstance(other, Byte):
      raise TypeError("Operand must be a Byte")
    return Byte(self._value & other._value)
  
  def __or__(self, other):
    if not isinstance(other, Byte):
      raise TypeError("Operand must be a Byte")
    return Byte(self._value | other._value)

  def __xor__(self, other):
    if not isinstance(other, Byte):
      raise TypeError("Operand must be a Byte")
    return Byte(self._value ^ other._value)

  def __invert__(self):
    """
    NOT operator
    """
    return Byte(~self._value)

  def to_bytes(self):
    return bytes([self._value])

  @staticmethod
  def pad(string, leng:int=8):
    return "0"*(leng-len(string))+string

  def __float__(self):
    mantissa = ((self._value%128//8)-32*(self._value//128))/8.0
    return mantissa * 2**(self._value%8-8*(self._value%16//8))

  def __int__(self):
    return self._value

  def __hex__(self):
    return Byte.pad(hex(self._value)[2:], leng=2)

  def __str__(self):
    return Byte.pad(bin(self._value)[2:])
  pass

Byte(5)


class Memory(bytearray):
  """
  sources?
  https://www.geeksforgeeks.org/python-bytearray-function/
  https://docs.python.org/3/library/stdtypes.html
  https://stackoverflow.com/questions/60653350/difficulty-with-assigning-values-to-bytearrays-in-python-without-using-integers
  """
  def __init__(self, size:int=256):
    super(Memory, self).__init__(size)
    self._size = size
    
  def __setitem__(self, addr, val: bytes|Byte):
    """
    sets value into address
    Memory[int] <- Byte
    Memory[int] <- bytes # len(bytes) == 1
    
    """
    if not (isinstance(val, bytes) or isinstance(val, Byte)):
      raise TypeError(f"val must be bytes, not {type(val).__name__}")
    if not isinstance(addr, int):
      raise TypeError(f"addr must be int, not {type(addr).__name__}")
    if not (0 <= addr < 256):
      raise ValueError(f"addr must be in range [0, 256), not {addr}")
    match(addr, val):
      # deals with Memory[int] <- Byte
      case(addr, Byte()):
        super(Memory, self).__setitem__(slice(addr, addr+1), val.to_bytes())
        pass
      # deals with Memory[int] <- bytes
      case(addr, bytes(val)) if len(val) == 1:
        super(Memory, self).__setitem__(slice(addr,addr+1), val)
      # throws appropriate error
      case(addr, bytes(val)) if len(val) > 1:
        raise ValueError("bytes being assigned is too big")
      # catches all extrainous cases  
      case _:
        raise TypeError("addressing method not found")
    return

  def __getitem__(self, addr:int):
    """
    gets value from Memory
    """
    if not isinstance(addr, int):
      raise TypeError(f"addr must be int, not {type(addr).__name__}")
    if not (0 <= addr < self._size):
      raise IndexError(f"addr must be in range[0, {self._size})")
    return Byte(super(Memory, self).__getitem__(addr))
    

  def __str__(self, row_len=32, rep=0) -> str:
    """
    hex representation
    """
    # hex(x)[2:] -> x in hex
    # {:>02} -> pad with 0 on the left till 2 chrs long
    # bin(x)[2:] -> x in binary
    # f"{x:>08}" -> pad with 0 on the left till 8 chrs long
    return " ".join([("\n" if i%row_len==0 else "")+(f"{bin(x)[2:]:>08}" if rep else f"{hex(x)[2:]:>02}") for i,x in enumerate(self)])



m = Memory()
m[100] = Byte(5)
m[101] = Byte(6)
m[102] = Byte(7)
m[0] = b'1'
m[28] = b'3'
print(m)
m[255] = b'4'

#m[3:10] = b'3456789'
print(m[100])
for i in range(256):
  m[i] = Byte(i)
  pass
print(m.__str__(4, 1))
print()


m = Memory()
for i, b in enumerate(b"HelloWorld, I want to test the functionality of the meory thingy!@#$%^&* EFBUIKJIFVNSvgrefew"):
  m[i] = Byte(b)

for i, b in enumerate(b"wudwiUFCAIKUfe", start=128):
  m[i] = Byte(b)
print(m)
for i in range(256):
  print(chr(int(m[i])), end=" ")

"""
run(
MOV R0, #0
MOV R1, #0
MOV R2, #0
top:
LDR r1, r0
/compare to see if is upperCase if yes, lower it
CMP R1, #65
BLT next
CMP R1, #90
BGT next
/ or you can use OR
ADD r1, r1, #32
next:
OUT r1, 7
ADD r0, r0, #1
CMP R0, #255
BLT top

Halt, m)"""


def run(code:str, mem:Memory=Memory(256)):
  """
  run mock asm code
  sources?
  https://forum.snap.berkeley.edu/t/why-doesnt-the-opcode-of-an-instruction-uniquely-identify-the-operation/13144
  https://www.cs.cornell.edu/courses/cs513/2005fa/paper.alpeh1.stacksmashing.html
  https://stackoverflow.com/questions/32943666/assembly-popping-an-empty-stack
  https://zhu45.org/posts/2017/Jul/30/understanding-how-function-call-works/
  https://people.cs.rutgers.edu/~pxk/419/notes/frames.html
  https://www.youtube.com/watch?v=4gwYkEK0gOk
  https://www.tutorialspoint.com/assembly_programming/assembly_system_calls.htm
  https://people.engr.tamu.edu/djimenez/taco/utsa-www/cs5513-fall07/lecture2.html
  opcode:
    # arithmetic/logic operations
    add
    sub
    mul
    and
    or
    xor
    # floating point operators
    add
    multiply
    # register operations
    mov
    ldr
    str
    # stack operations
    pop
    push
    # control transfer program counter manipulation
    jump
    conditional jump
    indirect jump # jump to address in pointer(register)
    call
    ret(urn)
    # 'kernal' operations/syscalls
    inp
    out
  """
  
