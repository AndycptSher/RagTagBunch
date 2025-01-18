from typing import Generic, TypeVar

class Functor:
  def __init__(self, wrap):
    self._v = wrap
  def map(self, func):
    return Functor(func(self._v))

class Monad(Functor):
  """
  unit :: a -> ma
  unit(x) >>= f <-> f(x)
  ma >>= unit <-> ma
  """
  def bind(self, f): # aka flatmap/chain
    raise NotImplementedError(f"bind function not yet implemented by {type(self).__name__}")

  def __rshift__(self, other):
    return self.bind(other)


class mList(Monad):
  def __init__(self, lst):
    self._lst = lst[::1]

  def breakUp(self):
    return (mMaybe(None) if len(self._lst) == 0 else mMaybe(self._lst[0])), mList(self._lst[1:])

  def reversed(self):
    return mList(self._lst[::-1])

  @classmethod
  def just(cls, *x):
    """
    returns mList wrapped around x
    """
    if len(x) == 0:
      return mList([])
    elif len(x) == 1 and isinstance(x[0], (list, set, tuple)):
      return mList(list(x[0]))
    elif len(x) == 1:
      return mList([x[0]])

  def map(self, func):
    return mList(list(map(func, self._lst)))

  def bind(self, f):
    """
    bind operator
    applies func to each element of self
    concatinates it back together
    """
    return mList(sum(map(lambda e: f(e)._lst, self._lst), []))

  def flatmap(self, other):
    return self >> other

  def toList(self):
    return self._lst[::1]

  def __pow__(self, other):
    """
    list concatination
    """
    if isinstance(other, mList):
      return mList(self._lst + other._lst)
    elif isinstance(other, (list, set, tuple)):
      return mList(self._lst + list(other))
    else:
      return mList(self._lst + [other])

  def __len__(self):
    return len(self._lst)

  def __str__(self):
    return "mList:"+str(self._lst)

def mListTest():
  lst = mList([1, 2, 3])
  print(lst.bind(lambda x: mList([x, x])))  # duplicate every element
  print(lst.bind(
    lambda x: mList([x, x]) 
    >> (lambda x: mList([x, x]))
  ))  # duplicate every element 4x

  class mDistinctList(mList):
    def bind(self, f):
      def nub(lis:list):
        if not isinstance(lis, list):
          raise TypeError("lis must be a list, not a {}".format(type(lis).__name__))
        if len(lis) <= 1:
          return lis
        else:
          return [lis[0]] + nub(list(filter(lambda a:(a != lis[0]),lis[1:])))
      return mDistinctList(nub(super(mDistinctList, self).bind(f)._lst))
      

  revCollatz = lambda x: mDistinctList([6*x,(x-1)]) >> (lambda z: mDistinctList([z//3]) if z%3==0 else mDistinctList([]))
  revCollatz.__doc__ = "reverse collatz conjecture" 
  print(mDistinctList([2,4,3]).bind(lambda x: mDistinctList([x])))
  s = mDistinctList([1])
  inp = input()
  while not inp:
    s >>= revCollatz
    print(s)
    inp = input()

class mMaybe(Monad):
  def __init__(self, x):
    self._x = x

  def map(self, func):
    return mMaybe(func(self._x)) if self._x is not None else self

  def bind(self, f):
    return f(self._x) if self._x is not None else self

  def unwrap(self):
    return self._x

  def __eq__ (self, other):
    if not isinstance(other, mMaybe):
      return False
    return self._x == other._x

  def __str__(self):
    return f"M({str(self._x)})"

def mMaybeTest():
  message = mMaybe("heyo")
  print(message)
  print(message\
        >> (lambda x: mMaybe(print("side effect", x)))\
        >> (lambda x: mMaybe(print("side effect2", x)))
       )


# def modifyTest():
#   testData = mList([
#     "|"
#     "L",
#     "|",
#     "L",
#     "|",
#     "|"
#     ])
#   modifyH = (lambda hInp: 
#              "" if hInp.breakUp()[0] else ""
#             )
#   modify = (lambda inp: modifyH(inp)(mList.just()))
if __name__ == "__main__":
  mListTest()
  mMaybeTest()