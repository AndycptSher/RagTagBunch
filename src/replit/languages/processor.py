class ALU:
  def __init__(self, size):
    """
    :param size: size of the registers
    """
    if type(size) != int:
      raise TypeError(f"size must be an integer, not {type(size)}")
    self.__size = size
    self.__acc = 0
    self.__overflow = False
    self.__carryOut = False
    self.__zeroFlag = False

  def setState(self, inp1, inp2, carryIn: bool, sub: bool):
    """
    :param inp1: input 1
    :param inp2: input 2
    :param carryIn: carry in
    :param sub: subtract
    """
    self.__acc = inp1 + (-1 if sub else 1) * inp2 + int(carryIn)
    self.__carryOut = self.__acc > self.__size - 1
    self.__overflow = not (0 <= self.__acc < self.__size)
    if self.__overflow:
      self.__acc %= self.__size
    self.__zeroFlag = self.__acc == 0

  def getAccumulator(self):
    return self.__acc
    
  def getCarryOut(self):
    return self.__carryOut
    
  def getOverflow(self):
    return self.__overflow
    
  def getZeroFlag(self):
    return self.__zeroFlag

# class 