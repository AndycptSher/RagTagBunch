from abc import ABC, abstractmethod
from utilities import raiseNotImplementedBy


"""
reminders:
  everything in this operation/file will be in bytes
    no ints being passed, except for the asm code, but once assembled, will become byte
    only bytes

citations(possible)
https://www.cs.jhu.edu/~phi/csf/slides/lecture-scram1.pdf
s
"""

class BytesInterface():
  """
  an interface that all byte interacting classes/methods in this file should use
  """
  
  @abstractmethod
  def __init__(self, value:bytearray) -> None:
    """
    :param value: the bytearray to wrap
    """
    raiseNotImplementedBy("Constructor", self)

  @staticmethod
  @abstractmethod
  def cast(item: 'int|BytesInterface') -> 'BytesInterface':
    """
    Casts the item to a BytesInterface
    "param item: the item to cast
    """
    raiseNotImplementedBy("cast", object())

  @abstractmethod
  def __len__(self) -> int:
    """
    returns the length of bytes being stored
    """
    raiseNotImplementedBy("len", self)

  @abstractmethod
  def __and__(self, other: 'BytesInterface') -> 'BytesInterface':
    """
    Performs a bitwise and on the two BytesInterfaces
    :param other: the other BytesInterface to perform the and on
    """
    raiseNotImplementedBy("and", self)

  @abstractmethod
  def __or__(self, other: 'BytesInterface') -> 'BytesInterface':
    """
    Performs a bitwise or on the two BytesInterfaces
    :param other: the other BytesInterface to perform the or on
    """
    raiseNotImplementedBy("or", self)

  @abstractmethod
  def __xor__(self, other: 'BytesInterface') -> 'BytesInterface':
    """
    Performs a bitwise xor on the two BytesInterfaces
    :param other: the other BytesInterface to perform the xor on
    """
    raiseNotImplementedBy("xor", self)
    
  @abstractmethod
  def __lshift__(self, other: 'BytesInterface') -> 'BytesInterface':
    """
    Performs a bitwise left shift on the BytesInterface
    :param other: the amount to shift by
    """
    raiseNotImplementedBy("lshift", self)
    
  @abstractmethod
  def __rshift__(self, other: 'BytesInterface') -> 'BytesInterface':
    """
    Performs a bitwise right shift on the BytesInterface
    :param other: the amount to shift by
    """
    raiseNotImplementedBy("rshift", self)
    
  @abstractmethod
  def __invert__(self) -> 'BytesInterface':
    """
    Performs a bitwise invert on the BytesInterface
    """
    raiseNotImplementedBy("invert", self)
    
  @abstractmethod
  def __eq__(self, other: 'BytesInterface') -> bool:
    """
    Performs a bitwise eq on the BytesInterface
    :param other: the other BytesInterface to perform the eq on
    """
    raiseNotImplementedBy("eq", self)

  @abstractmethod
  def __int__(self):
    """
    returns the BytesInterface as an int
    """
    raiseNotImplementedBy("int", self)
  
  @abstractmethod
  def __repr__(self) -> str:
    """
    :return: the string representation of the BytesInterface
    """
    raiseNotImplementedBy("repr", self)

class MemoryInterface:
  """
  an interface that all memory interacting classes/methods in this file should use
  """
  
  @abstractmethod
  def __init__(self, size:int, busSize) -> None:
    """
    :param size: the size of the memory
    :param busSize: the size of the memory bus
    """
    raiseNotImplementedBy("Constructor", self)
    
  @abstractmethod
  def __getitem__(self, index:BytesInterface) -> BytesInterface:
    """
    gets the value at the index
    :param index: the index to get the value at
    """
    raiseNotImplementedBy("getitem", self)
    
  @abstractmethod
  def __setitem__(self, index:BytesInterface, value:BytesInterface) -> None:
    """
    Sets the value at the index
    :param index: the index to set the value at
    :param value: the value to set
    """
    raiseNotImplementedBy("setitem", self)
    
  @abstractmethod
  def __len__(self) -> int:
    """
    returns the length of the memory
    """
    raiseNotImplementedBy("len", self)
    
  @abstractmethod
  def __repr__(self):
    """
    returns the string representation of the memory
    """
    raiseNotImplementedBy("repr", self)



class Bytes(BytesInterface):
  """
  a class that represents bytes
  """
  
  def __init__(self, value:bytearray) -> None:
    """
    :param value: the value of the bytes
    """
    if not isinstance(value, bytearray):
      raise TypeError("value must be a bytearray")
    self._value = value

  @staticmethod
  def cast(item: 'int|BytesInterface') -> 'BytesInterface':
    if isinstance(item, int):
      return Bytes(bytearray([item]))
    elif isinstance(item, Bytes):
      return Bytes(item._value)
    else:
      raise TypeError(f"item must be an int or Bytes, not {type(item)}")

  def __len__(self):
    return len(self._value)
    
  def __and__ (self, other: 'Bytes') -> 'Bytes':
    if not isinstance(other, Bytes):
      raise TypeError("other must be a Bytes")
    if len(self) != len(other):
      raise ValueError("other must be the same length as self")
    return Bytes(bytearray([self._value[i] & other._value[i] for i in range(len(self))]))

  def __or__ (self, other: 'Bytes') -> 'Bytes':
    if not isinstance(other, Bytes):
      raise TypeError("other must be a Bytes")
    if len(self) != len(other):
      raise ValueError("other must be the same length as self")
    return Bytes(bytearray([self._value[i] | other._value[i] for i in range(len(self))]))
    
  def __xor__ (self, other: 'Bytes') -> 'Bytes':
    if not isinstance(other, Bytes):
      raise TypeError("other must be a Bytes")
    if len(self) != len(other):
      raise ValueError("other must be the same length as self")
    return Bytes(bytearray([self._value[i] ^ other._value[i] for i in range(len(self))]))
    
  def __lshift__(self, other: 'Bytes') -> 'Bytes':
    self._value[0] << int(other)
    
  def __invert__ (self) -> 'Bytes':
    return Bytes(bytearray([(~self._value[i])%256 for i in range(len(self))]))

  def __int__(self):
    return int.from_bytes(self._value, byteorder='big')

  def __repr__(self) -> str:
    return "\n"+bin(int(self))[2:]+"\n"+str(self._value)[12:-2]


if __name__ == "__main__":
  pass
  print("running asmSim2")
  b=Bytes.cast(17)
  print(type(b))
  print(repr(b))
  print(int(b))
  print(~b)
  a = Bytes(bytearray([128,17,0,128]))
  print(repr(a))
  mask = Bytes(bytearray([0,0,255,255]))
  print(a&mask)
  print(a|mask)
  print(a^mask)
  print("finnished running asmSim2")