class matrix:
  def __init__(self, array):
    """
    array: matrix as an array
    [[1,2],[3,4]]: 2x2
    1 2
    3 4
    [[1,2,3],[4,5,6]]: 2x3
    """
    # if len of all arrays are not the same, raise
    if not all(map(lambda a:len(array[0])==len(a), array)):
      raise Exception("not valid input")
    self.__dimension = (len(array), len(array[0]))
    self.__mat = array

  def isSquare(self):
    return self.__dimension[0] == self.__dimension[1]

  def getSize(self):
    return self.__dimension

  def __getArray(self):
    return self.__mat

  def getMinor(self, xIndex, yIndex):
    """
    starting with 1
    """
    # check if indexes are within bounds
    if not(0< yIndex <=self.__dimension[0] and 0< xIndex <=self.__dimension[1]):
      raise Exception("invalid index")

    final = []
    for y in range(self.__dimension[0]):
      if y == yIndex-1:
        continue
      final1 = []
      for x in range(self.__dimension[1]):
        if x == xIndex-1:
          continue
        final1.append(self.__mat[y][x])
      final.append(final1)
    return matrix(final)

  def getDeterminant(self):
    try:
      return self.__det
    except AttributeError as e:
      pass
    if not self.isSquare():
      raise Exception("Not Square matrix")
    if self.__dimension == (1,1):
      return self.__mat[0][0]
    coefficient = 1
    total = 0
    for index, item in enumerate(self.__mat[0]):
      total += coefficient * item * self.getMinor(index+1,1).getDeterminant()
      coefficient *= -1
    return total
        
  def getMatrixOfMinors(self):
    final = []
    for y in range(self.__dimension[0]):
      final1 = []
      for x in range(self.__dimension[1]):
        final1.append(self.getMinor(x+1, y+1).getDeterminant())
      final.append(final1)
    return matrix(final)
    
  def applyMatrixOfCofactors(self):
    final = []
    for i, row in enumerate(self.__mat):
      final1 = []
      for j, item in enumerate(row):
        final1.append((-1)**(i+j)*item)
      final.append(final1)
    return matrix(final)

  def getTranspose(self):
    return matrix(list(zip(*self.__mat)))
    
  def getInverse(self):
    # if not square matrix
    if not self.isSquare():
      raise Exception("Not Square matrix")
    det = self.getDeterminant()
    # if determinant is 0
    if not det:
      raise Exception("inverse does not exist")

    return self.getMatrixOfMinors().applyMatrixOfCofactors().getTranspose()*(1/det)
    
  def __mul__(self, other):
    if type(other) not in (matrix, int, float):
      raise TypeError("other is not a matrix or number")
    # if other is a number
    if type(other) != matrix:
      final = []
      for row in self.__mat:
        final.append(list(map(lambda a: a*other, row)))
      return matrix(final)
    elif type(other) == matrix:
      other = other.getTranspose()
      if other.__dimension[1] != self.__dimension[1]:
        raise Exception("Invalid matrix dimensions")
      final = []
      for y in range(self.__dimension[0]):
        final1 = []
        for x in range(other.__dimension[0]):
          final1.append(sum(map(lambda a: a[0]*a[1], zip(self.__mat[y],other.__mat[x]))))
        final.append(final1)
      return matrix(final)

  def __eq__(self, other):
    if type(other) != matrix:
      return False
    if other.getSize() != self.__dimension:
      return False
    return self.__mat == other.__getArray()
      
  def __str__(self):
    final = ""
    for row in self.__mat:
      final += "("+" ".join(map(str,row)) + ")\n"
    final = final[:-1]
    return final

def tests():
  test = lambda a, b:[print(a+str(b)),b][1]
  result = True
  a = matrix([[1,4],[6,2]])
  result &= test("2x2 print check: ",str(a)=="(1 4)\n(6 2)")
  result &= test("2x2 minor check: ", a.getMinor(1,2) == matrix([[4]]))
  result &= test("2x2 determinant check: ", a.getDeterminant() == -22)
  result &= test("2x2 inverse check: ", a.getInverse() == matrix([[-1/11, 2/11],[3/11, -1/22]]))
  b = matrix([[5,0,2],[-1,8,1],[6,7,3]])
  result &= test("3x3 print check: ", str(b) == "(5 0 2)\n(-1 8 1)\n(6 7 3)")
  result &= test("3x3 determinant check: ", b.getDeterminant() == -25)
  result &= test("3x3 transpose check: ", b.getTranspose().__str__() == matrix([[5,-1,6],[0,8,7],[2,1,3]]).__str__())
  c = matrix([[3,0,2],[2,0,-2],[0,1,1]])
  # print(c)
  result &= test("3x3 inverse check: ", c.getInverse() == matrix([[2/10,2/10,0.0],[-2/10,0.1+0.2,1.0],[2/10,-0.2-0.1,0.0]]))
  d = matrix([[2,2,0],[-2,3,10],[2,-3,0]])
  # print(d)
  d *= 0.1
  # print(d)
  # print(c*d)
  # print(d*c)

  a = matrix([[2,1],[3,-1]]).getInverse()
  b = matrix([[5],[5]])
  result &= test("2x2*2x1 matrix multiplication test: ", a*b == matrix([[2.0],[(0.1+0.2)*10-2]]))
  
  z = b.getSize
  b.getSize = lambda :(print("sillly"),z())[1]
  print(b.getSize())
  print(a.getSize())
  return result

def main():
  assert(tests())
  p = matrix([[1,0,3],[2,1,-4],[0,2,-19]])
  q = matrix([[0.5,0,0],[0,0,1/3],[0,1/4,0]])
  print(p.getInverse())
  print(q.getInverse())
  print(pq:=p*q)
  print(pq.getDeterminant())
  print(pq.getInverse())

  m = matrix([[1,1,1],[0,-1,1],[1.22, 0.9, 1.28]])
  print("M\n", m.getInverse()*0.26)
  print(m.getInverse()*matrix([[200, 0, 0], [20, 0, 0], [240, 0, 0]])*0.26)

if __name__ == "__main__":
  main()

