from collections.abc import Iterable

def greatestCommonSubsequenceLength(list1: list, list2: list):
  global counter
  print(counter :=counter +1)
  if not isinstance(list1, Iterable) or not isinstance(list2, Iterable):
    raise TypeError("list1 and list2 must be iterable")
  if len(list1) == 0 or len(list2) == 0:
    return 0
  if list1[0] == list2[0]:
    return 1 + greatestCommonSubsequenceLength(list1[1:], list2[1:])
  else:
    return max(greatestCommonSubsequenceLength(list1[1:], list2),
               greatestCommonSubsequenceLength(list1, list2[1:]))

one = tuple("""6
4
9
5
9
11
""".split())
two = tuple("""1
4
5
6
9
10
11""".split())
print(one, two)
counter = 0
print(greatestCommonSubsequenceLength(one, two)) # type: ignore

def greatestCommonSubsequence(list1: tuple, list2: tuple, saved: dict = {}):
  global counter
  print(counter := counter + 1)
  if not isinstance(list1, tuple) or not isinstance(list2, tuple):
    raise TypeError("list1 and list2 must be a tuple")

  # if one if the sequence is empty, there is no common subsequence
  if len(list1) == 0 or len(list2) == 0:
    return ()

  # if the start of the sequence is idenical, add it to the common subsequence
  elif list1[0] == list2[0]:
    res = (list1[0],) + greatestCommonSubsequence(list1[1:], list2[1:], saved)

  # else try both heads of the sequences
  else:
    first = greatestCommonSubsequence(list1[1:], list2, saved)
    # if path is not traversed, traverse 
    if saved.get(tuple(sorted((list1, list2[1:]))), None) is None:
      second = greatestCommonSubsequence(list1, list2[1:], saved)
    # else draw from saved
    else:
      second = saved[tuple(sorted((list1, list2[1:])))]
    
    res = max(first,
              second ,key = len)
  saved[tuple(sorted((list1, list2)))] = res
  return res
counter = 0
print(one, two)
print(greatestCommonSubsequenceLength(one, two)) # type: ignore
counter = 0
print(greatestCommonSubsequence(one, two))


class Description:
  NoChange = 0
  
  def __init__(self, object, description: int):
    ...

def getChanges(before: tuple, after: tuple) -> tuple[tuple[Description], int]: # type: ignore
  if not isinstance(before, tuple) or not isinstance(after, tuple):
    raise TypeError("before and after must be a tuple")
  if len(before) == 0:
    ...
  if len(after) == 0:
    ...