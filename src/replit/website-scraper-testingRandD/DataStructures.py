from collections.abc import ItemsView, Iterable
from typing import Type
import math
# from typing import Type

def assert_print(test, objective, msg="assertion failed"):
  print(test)
  assert test == objective, msg


class Heap:
  """
  abstract base class for all heaps
  """
  @staticmethod
  def comparison_function(a, b) -> bool:
    """
    returns True if a should exit before b
    """
    raise NotImplementedError(f"comparison method not implemented")

  def __bubble_up(self, index: int) -> None:
    """
    also known as sift up,
    bubbles the value at index up the heap until it is in the correct position
    """
    # while index of node is not root node/parent is not out of bounds
    while (parent_index := (index+1) // 2 - 1) >= 0:
      # if the value at the child index should exit before the parent node, swap
      if self.comparison_function(self.__array[index], self.__array[parent_index]):
        # swap at indexes
        self.__array[parent_index], self.__array[index] = self.__array[index], self.__array[parent_index]
        # recurse upwards
        index = parent_index
      # if already in correct order, operation finished
      else:
        break

  def __bubble_down(self, index: int) -> None:
    """
    also known as sift down,
    bubbles the value at index down the heap until it is in the correct position
    """
    while index < len(self.__array):
      new_index = 2*(index+1)-1
      if new_index >= len(self.__array):
          break
      elif new_index+1 >= len(self.__array):
          pass
      elif self.__array[new_index] < self.__array[new_index+1]:
          new_index += 1
      if self.__array[index]>self.__array[new_index]:
          break
      # swap
      temp = self.__array[new_index]
      self.__array[new_index] = self.__array[index]
      self.__array[index] = temp
      # traverse to next layer
      index = new_index
  
  @classmethod
  def from_list(cls, lis: list):
    assert isinstance(lis, Iterable)
    new_array = []
    for item in lis:
      new_array.append(item)
      
      # index = len(new_array)-1
      # # while index of node is not root node/parent is not out of bounds
      # while (parent_index := (index+1) // 2 - 1) >= 0:
      #   # if the value at the child index should exit before the parent node, swap
      #   if cls.comparison_function(new_array[index], new_array[parent_index]):
      #     # swap at indexes
      #     new_array[parent_index], new_array[index] = new_array[index], new_array[parent_index]
      #     # recurse upwards
      #     index = parent_index
      #   # if already in correct order, continue to next
      #   else:
      #     break
    
    new_heap = cls()
    new_heap.__array = new_array
    for i in range(len(new_array)):
      new_heap.__bubble_up(i)
    return new_heap
    
  def __init__(self) -> None:
    self.__array = []

  def add_node(self, node) -> None:
    self.__array.append(node)
    self.__bubble_up(len(self.__array)-1)

  def remove_node(self):
    if len(self.__array) == 0:
      raise IndexError("cannot remove from empty heap")
    # swap root with last node
    self.__array[0], self.__array[-1] = self.__array[-1], self.__array[0]
    # remove last node
    result = self.__array.pop()
    # bubble down
    self.__bubble_down(0)
    return result

  def is_empty(self) -> bool:
    return not bool(self.__array)
  
  def to_list(self) -> list:
    return self.__array[:]


def heap_tests():
  """
  tests for heap class
  """
  print("heap tests")
  class MinHeap(Heap):
    @staticmethod
    def comparison_function(a, b) -> bool:
      return a < b
  
  h = MinHeap()
  h.add_node(1)
  h.add_node(2)
  h.add_node(3)
  h.add_node(-4)
  h.add_node(-1)
  assert h.to_list() == [-4, -1, 3, 2, 1]

  class MaxHeap(Heap):
    @staticmethod
    def comparison_function(a, b) -> bool:
      return a > b

  h = MaxHeap.from_list([3,3,4,1,3,4,3,4,6,6,9,3,6,2,8,5])
  print(h.to_list())
  while not h.is_empty():
    print(h.remove_node())
    print(h.to_list())

if __name__ == "__main__":
  heap_tests()


class DoubleyLinkedList:
  class Node:
    @classmethod
    def create_first_node(cls, item):
      node = cls.__new__(cls)
      node.previous_node = None
      node.next_node = None
      node.__item = item
      return node
      
    def __init__(self, previous_node: 'DoubleyLinkedList.Node', item, next_node: 'DoubleyLinkedList.Node | None' = None) -> None:
      self.__item = item
      if not isinstance(previous_node, DoubleyLinkedList.Node):
        raise TypeError(f"previous_node must be a DoubleyLinkedList.Node, not {type(previous_node)}")
      if not isinstance(next_node, DoubleyLinkedList.Node) and next_node is not None:
        raise TypeError(f"next_node must be a DoubleyLinkedList.Node, not {type(next_node)}")
      # pointer/ reference to previous node
      self.previous_node = previous_node
      # pointer/reference to next node
      self.next_node = next_node

    def get_item(self):
      return self.__item

  def __init__(self):
    self.__head = None
    self.__tail = None
    self.__length = 0

  def append(self, item):
    self.__length += 1
    # if the list is empty
    if self.__tail is None:
      self.__head = self.Node.create_first_node(item)
      self.__tail = self.__head
      return
    self.__tail.next_node = self.Node(self.__tail, item)
    self.__tail = self.__tail.next_node

  def insert(self, index: int, item):
    if not isinstance(index, int):
      raise TypeError(f"index must be an int, not {type(index)}")
    if index < 0 or index > self.__length:
      raise IndexError(f"index {index} out of bounds")
    
    if index == 0:
      previouse_head = self.__head
      self.__head = self.Node.create_first_node(item)
      self.__head.next_node = previouse_head
      self.__length += 1
    elif index == self.__length or self.__tail is None:
      self.append(item)
    elif index >= self.__length//2:
      # traverse from tail
      current_node = self.__tail
      while index < self.__length:
        current_node = current_node.previous_node
        index += 1
      current_node.next_node = self.Node(current_node, item, current_node.next_node)
    elif index < self.__length//2:
      # traverse from head
      current_node = self.__head
      while index > 1:
        current_node = current_node.next_node
        index -= 1
      current_node.next_node = self.Node(current_node, item, current_node.next_node)

  def remove(self, index: int):
    if not isinstance(index, int):
      raise TypeError(f"index must be an int, not {type(index)}")
    if not (0<=index<self.__length):
      raise ValueError(f"index {index} out of bounds")
      
    value = None
    if index == 0:
      value = self.__head.get_item()
      self.__head = self.__head.next_node
      self.__head.previous_node = None
      self.__length -= 1
    elif index == self.__length-1:
      value = self.__tail.get_item()
      self.__tail = self.__tail.previous_node
      self.__tail.next_node = None

  def pop(self, index: int = -1):
    if not isinstance(index, int):
      raise TypeError(f"index must be an int, not {type(index)}")
    if index == -1:
      index = self.__length-1
    saved = self.get(index)
    self.remove(index)
    return saved

  def get(self, index: int):
    if not isinstance(index, int):
      raise TypeError(f"index must be an int, not {type(index)}")
    if not (0<=index<self.__length):
      raise ValueError(f"index {index} out of bounds")
    
    pointer = self.__head
    for i in range(index):
      pointer = pointer.next_node
    return pointer.get_item()
  
  def __len__(self) -> int:
    return self.__length

  def to_list(self) -> list:
    result = []
    current_node = self.__head
    while current_node is not None:
      result.append(current_node.get_item())
      current_node = current_node.next_node
    return result
  ...



def linked_list_tests():
  """
  tests for linked list class
  """
  print("linked list tests")
  l = DoubleyLinkedList()
  l.append(1)
  l.append(2)
  l.append(3)
  l.append(4)
  l.append(5)
  
  assert l.to_list() == [1,2,3,4,5]
  l.insert(0, 0)
  l.insert(6, 6)
  l.insert(3, 3.5)
  
  assert l.to_list() == [0,1,2,3.5,3,4,5,6]
  ...

if __name__ == "__main__":
  linked_list_tests()

class BinaryTree:
  class Node:
    def __init__(self, item, left: 'BinaryTree.Node | None' = None, right: 'BinaryTree.Node | None' = None) -> None:
      self.__item = item
      self.left = left
      self.right = right

    def get_item(self):
      return self.__item

    def get_left(self):
      return self.left

    def get_right(self):
      return self.right

  def __init__(self) -> None:
    self.__root: None | BinaryTree.Node = None

  def contains(self, item):
    current_node = self.__root
    while current_node is not None:
      if item == current_node.get_item():
        return True
      elif item < current_node.get_item():
        current_node = current_node.get_left()
      else:
        current_node = current_node.get_right()
    return False
    
  def add_node(self, item):
    if self.__root is None:
      self.__root = self.Node(item)
      return
    
    current_node = self.__root
    while current_node is not None:
      if item < current_node.get_item():
        if current_node.get_left() is None:
          current_node.left = self.Node(item)
          return
        else:
          current_node = current_node.get_left()
      elif item > current_node.get_item():
        if current_node.get_right() is None:
          current_node.right = self.Node(item)
          return
        else:
          current_node = current_node.get_right()
      else:
        # implementation dependant on how duplicates are handled/intended behaviour
        ...
    ...

  def remove_node(self, item):
    if self.__root is None:
      raise ValueError(f"cannot remove from empty tree")
    current_node = self.__root
    parent_node = None
    # search for node
    while current_node is not None:
      if item == current_node.get_item():
        break
      elif item < current_node.get_item():
        parent_node = current_node
        current_node = current_node.get_left()
      else:
        parent_node = current_node
        current_node = current_node.get_right()

    # if node not found
    if current_node is None:
      raise ValueError(f"item {item} not found in tree")

    # if node has no children
    if current_node.get_left() is None and current_node.get_right() is None:
      if parent_node is None:
        self.__root = None
      elif parent_node.get_left() == current_node:
        parent_node.left = None
      else:
        parent_node.right = None
    # if node has one child
    elif current_node.get_left() is None or current_node.get_right() is None:
      replacement_node = current_node.get_left() if current_node.get_left() is not None else current_node.get_right()
      if parent_node is None:
        self.__root = replacement_node
      elif parent_node.get_left() == current_node:
        parent_node.left = replacement_node
      else:
        parent_node.right = replacement_node
    # if node has two children
    else:
      replacement_node = current_node.get_right()
      replacement_parent = current_node
      # find leftmost child of right subtree
      while replacement_node.get_left() is not None:
        replacement_parent = replacement_node
        replacement_node = replacement_node.get_left()
      # replace node with leftmost child of right subtree
      replacement_parent.left = replacement_node.get_right()
      replacement_node.left = current_node.get_left()
      replacement_node.right = current_node.get_right()
      # ^ has tendency to create left heavy tree
      
      if parent_node is None:
        self.__root = replacement_node
      elif parent_node.get_left() == current_node:
        parent_node.left = replacement_node
      else:
        parent_node.right = replacement_node
    return current_node.get_item()
  ...



class BTree:
  # https://en.wikipedia.org/wiki/B-tree
  def __init__(self, num: int):
    assert isinstance(num, int)
    assert num > 0
    self.__min_num = num
    self.__max_num = 2*num
    class Node:
      __min_num = num
      __max_num = num*2
      def __init__(self, parent: 'BTree.Node | None', keys: list, children: 'list[Node]', is_leaf: bool):
        self.__parent = parent # also is_root flag when None
        self.__children = children
        self.__keys = keys
        self.__is_leaf = is_leaf

      def set_parent(self, parent):
        if self.__parent is not None:
          raise ValueError("node already has a parent")
        self.__parent = parent

      def get_keys(self):
        return [*self.__keys] # lockdown reference

      def get_children(self):
        return [*self.__children] # lockdown reference

      def _split(self):
        # split node into two
        # return the new nodes and the key that was split
        if len(self.__keys) <= self.__max_num:
          raise ValueError("can only split overflowing nodes")

        midpoint = len(self.__keys)//2

        # for refactors into different languages, self.__children may be []/empty and cause out of bounds error
        left =  Node(self.__parent, self.__keys[:midpoint],     self.__children[:midpoint + 1], self.__is_leaf)
        right = Node(self.__parent, self.__keys[midpoint + 1:], self.__children[midpoint + 1:], self.__is_leaf)
        return left, self.__keys[midpoint], right

      def contains(self, item):
        if len(self.__keys) == 0:
          return False
        # assumes tree structure is valid
        upper_bound = len(self.__keys)
        lower_bound = -1
        while abs(upper_bound - lower_bound) > 1:
          middle = (upper_bound + lower_bound)//2
          if item == self.__keys[middle]:
            return True
          elif item < self.__keys[middle]:
            upper_bound = middle
          else:
            lower_bound = middle
        return not self.__is_leaf and self.__children[upper_bound].contains(item)

      def add_item(self, item):
        # warning, throws error if node becomes full
        # binary search down to leaf node, insert, check size, raise warning if full, recurse check upward 
        if self.__is_leaf:
          self.__keys.append(item)
          self.__keys.sort() # unoptimized for large min_sizes conceptually
        
        else:
          # find index of child node to insert into
          upper_bound = len(self.__keys)
          lower_bound = -1
          while upper_bound - lower_bound > 1:
            middle = (upper_bound + lower_bound)//2
            if item == self.__keys[middle]:
              upper_bound = middle
              break
            elif item < self.__keys[middle]:
              upper_bound = middle
            else:
              lower_bound = middle

          # insert into child node
          target_node = self.__children[upper_bound]
          try:
            # if there is no problem adding the node
            target_node.add_item(item)
            return # if no error(no new keys), return
            
          except ValueError as e:
            # if the target node is full
            left, key, right = target_node._split() # cannot error since prior complementary error was raised
            self.__keys.insert(upper_bound, key)
            self.__children[upper_bound] = left
            self.__children.insert(upper_bound+1, right)
        
        # account for overflow when splitting
        if len(self.__keys) > self.__max_num:
          if self.__parent is not None:
            raise ValueError("node is full")
          else:
            left, key, right = self._split()
            # root = Node(None, [key], [left, right], False)
            # left.set_parent(root)
            # right.set_parent(root)
            # return root
            self.__keys = [key]
            self.__children = [left, right]
            left.set_parent(self)
            right.set_parent(self)
            self.__is_leaf = False
            return
        return

      def _retrieve_rightmost_item(self) -> 'tuple[item, Exception]':
        # helper method for remove_item
        # recursive method to retrieve the rightmost item in a node branch
        # warning, assuming node is not root
        assert self.__parent is not None, "helper function \"_retrieve_rightmost_item\" called on root node"
        
        if self.__is_leaf:
          temp = self.__keys.pop() # remove from keys first before checking num of remaining keys
          # report to parent node if node is full
          return temp, len(self.__keys) < self.__min_num
          
        else:
          temp, request = self.__children[-1]._retrieve_rightmost_item()

          # only relay when no action required
          if not request:
            return temp, False
            
          # handle merge request
          seperator = self.__keys.pop()
          child2 = self.__children.pop()
          child1 = self.__children.pop()
          newChild = Node(self, [*child1.get_keys(), seperator, *child2.get_keys()], [*child1.get_children(), *child2.get_children()], child1.get_children() == [])
          
          try:
            # see if the merged node is full
            child1, seperator, child2 = newChild._split()
            # if _split does not raise error, split successfull
            self.__keys.append(seperator)
            self.__children.extend([child1, child2])
            # as number of keys unchanged, no merge action required by parent
            return temp, False
            
          except ValueError:
            # if new_child cannot be split, check if self underflows
            self.__children.append(newChild)
            return temp, len(self.__keys) < self.__min_num
 
      def remove_item(self, item, contains_check: bool=False) -> 'tuple[item, bool]':
        # warning, throws error or option if item not found
        # return stored item(retrieve using item skeleton object) and flag if handling required
        # binary search find target
        # if leaf node, remove item, and bubble concern to be handled by parent
        # if not leaf node, replace item with item from rightmost item in left branch
        # if node retrieved from becomes deficent, bubble concern to be handled by parent
        # handling -> merge, then attempt to split if possible, if cannot split, check if deficit for parent to handle, if can split, return retrieved item up
        
        if not contains_check and self.__parent is None and not self.contains(item):
          raise ValueError(f"item {item} not found in tree")

        # binary search for target
        upper_bound = len(self.__keys)
        lower_bound = -1
        while upper_bound - lower_bound > 1:
          middle = (upper_bound + lower_bound)//2
          if item == self.__keys[middle]:
            # if the node is a leaf, remove the item and return, as leaf nodes need not replace the retrieved node
            if self.__is_leaf:
              temp = self.__keys.pop(middle)

              # succinct/branchless code/version
              return temp, self.__parent is not None and len(self.__keys) < self.__min_num

              # readable code/version
              if self.__parent is None: # if the node is a root, no action required
                return temp, False
              else:
                return temp, len(self.__keys) < self.__min_num

              # whacky code/version
              if self.__parent is None:
                return temp, False
              else:
                if len(self.__keys) < self.__min_num:
                  return temp, True
                else:
                  return temp, False
              
            replacement, action_requested = self.__children[middle]._retrieve_rightmost_item()

            # replace item with rightmost item in child node + setup for checks
            temp = self.__keys.pop(middle)
            seperator_key = replacement
            seperator_index = middle
            
            break
            
          elif item < self.__keys[middle]:
            upper_bound = middle
          else:
            lower_bound = middle
        else:
          temp, action_requested = self.__children[upper_bound].remove_item(item, True)
          
          # handle merge request
          # find/calculate/get valid other node's side
          seperator_index = min(upper_bound, len(self.__keys)-1)
          seperator_key = self.__keys.pop(seperator_index)

        
        # propagate unchanged state
        if not action_requested:
          return temp, False

        # merge and try to split if action required
        child1 = self.__children.pop(seperator_index)
        child2 = self.__children.pop(seperator_index)
        newChild = Node(self, [*child1.get_keys(), seperator_key, *child2.get_keys()], [*child1.get_children(), *child2.get_children()], child1.get_children() == [])

        try:
          # see if the merged node is full
          child1, seperator_key, child2 = newChild._split()

          # if _split does not raise error, split successfull
          self.__keys.insert(seperator_index, seperator_key)
          self.__children.insert(seperator_index, child2)
          self.__children.insert(seperator_index, child1)
          # as number of keys unchanged, no merge action required by parent
          return temp, False
        
        except ValueError:
          # if new_child cannot be split, check if self underflows
          self.__children.insert(seperator_index, newChild)
      
          # if the removed item is in root node, check if root node underflows below 0
          if self.__parent is None:
            if len(self.__keys) == 0:
              # the newChild will be the new root node
              self.__keys = newChild.get_keys()
              self.__children = newChild.get_children()
              self.__is_leaf = newChild.get_children() == []
              return temp, False
              
            # no action required for roots with one or more keys remaining
            return temp, False

          # else if current node is an intermeidate node, check if underflows
          return temp, len(self.__keys) < self.__min_num

      def get_slice(self, start, end, found_start = False) -> list:
        # return a slice of the tree
        # start inclusive and end exclusive
        # returns a list of items
        # if start and end are not in the tree, returns an empty list
        # if start and end are in the tree, returns a list of items
        
        # empty root case
        if len(self.__keys) == 0:
          return []
          
        if not found_start:
          bottom_upper_bound = len(self.__keys) # inclusive upper bound for start
          bottom_lower_bound = -1 # exclusive lower bound for start
          while bottom_upper_bound - bottom_lower_bound > 1:
            bottom_middle = (bottom_upper_bound + bottom_lower_bound)//2
            if start <= self.__keys[bottom_middle]:
              bottom_upper_bound = bottom_middle
            else:
              bottom_lower_bound = bottom_middle
          
          start_index = bottom_upper_bound
        else:  
          start_index = 0
        
        result = []
        # if the node is a leaf, scrape the keys until the end is reached (item or index, whichever comes first)
        if self.__is_leaf:
          while start_index < len(self.__keys) and self.__keys[start_index] < end:
            result.append(self.__keys[start_index])
            start_index += 1
          return result
        # if the node is not a leaf, find the start index in the node to the left
        else:
          while start_index < len(self.__keys):
            result.extend(self.__children[start_index].get_slice(start, end, found_start))
            found_start |= result == []
            if end <= self.__keys[start_index]:
              break
            result.append(self.__keys[start_index])
            start_index += 1

          # when index reaches the end of keys, check if the end is in the rightmost child
          else:
            result.extend(self.__children[start_index].get_slice(start, end, found_start))
          return result
      
      def _repr(self):
        # helper function for __repr__
        if self.__is_leaf:
          return map(str, self.__keys)

        child_lines = map(
          lambda x: map(
            lambda y: "\t" + y, x._repr()
          ), self.__children
        )
        return sum([[str(x), *y] for (x, y) in zip(["", *self.__keys], child_lines)], [])[1:]

      def __repr__(self):
        return "\n".join(self._repr())
        
    self.__root = Node(None, [], [], True)

  def contains(self, item):
    return self.__root.contains(item)

  def get_slice(self, start, end):
    return self.__root.get_slice(start, end)

  def add_item(self, item):
    self.__root.add_item(item)

  def remove_item(self, item):
    temp, request =  self.__root.remove_item(item)
    assert not request, "remove_item should have been handled by node class"
    return temp

  def __repr__(self):
    return "-----\n"+\
    "\n".join(map(lambda line: "|\t"+line, repr(self.__root).split("\n")))+\
    "\n-----"




def BTree_tests():
  def test_n_size(tree):
    print(tree.contains(3))
    tree.add_item(3)
    print(repr(tree))
    print(tree.contains(3))
    tree.add_item(4)
    print(repr(tree))
    for i in range(3):
      tree.add_item(i)
      print(repr(tree))
    for i in range(5):
      print(i, tree.contains(i))
  
    for i in range(5, 13):
      tree.add_item(i)
      print(repr(tree))
  
    for i in range(0, 14):
      print(i, tree.contains(i))
  
    tree.add_item(3)
    print(repr(tree))
    tree.add_item(3)
    tree.add_item(5)
    print(repr(tree))
    tree.add_item(12)
    print(repr(tree))

    

    tree.remove_item(12)
    print(repr(tree))
    tree.add_item(13)
    print(repr(tree))
    tree.remove_item(5)
    print(repr(tree))
    tree.add_item(5)
    print(repr(tree))
    tree.remove_item(11)
    print(repr(tree))
    assert_print(tree.get_slice(2, 4), [2, 3, 3, 3], "slice does not match")
    assert_print(tree.get_slice(3, 4), [3, 3, 3], "slice does not match")
    assert_print(tree.get_slice(1, 9), [1, 2, 3, 3, 3, 4, 5, 5, 6, 7, 8], "slice does not match")
    assert_print(tree.get_slice(7, 10), [7, 8, 9], "slice does not match")
    assert_print(tree.get_slice(-2, 3), [0, 1, 2], "slice does not match")
    assert_print(tree.get_slice(0, 0), [], "slice does not match")
    assert_print(tree.get_slice(8, 20), [8, 9, 10, 12, 13], "slice does not match")
    assert_print(tree.get_slice(11, 11), [], "slice does not match")
    assert_print(tree.get_slice(20, 20), [], "slice does not match")

  
  import random
  # tree = BTree(2)
  # while not (inp := input(f"{(rand := random.randint(0, 17))}(type anything to stop)")):
  #   tree.add_item(rand)
  #   print(repr(tree))

  
  test_n_size(BTree(2))
  # test_n_size(BTree(3))
  # test_n_size(BTree(4))
  ...


if __name__ == "__main__":
  BTree_tests()


class DataBaseBTree:
  ...

# class BTreeFactory:
#   @staticmethod
#   def create_tree(minimum: int, maximum: int):
#     assert (minimum > 0 & maximum > 2*minimum & maximum != math.inf)
#     class BTree:
#       mini = minimum
#       maxi = maximum
#       class Node:
#         class OverFlowException(Exception):
#           ...
#         def __init__(self, is_root: bool):
#           self.max_items = maximum
#           self.min_items = minimum
#           self.is_root = is_root
#           self.is_leaf = True
#           self.items = []
#           self.seperators = [] # if the node is a leaf, seperators will be empty
#           self.parent_item = None

#         def add_item(self, item) -> 'Node':
#           if len(self.items) == self.max_items:
#             if self.is_root:
#               # TODO:implement splitting of current node into two nodes
#               ...
#               return
#             raise self.OverFlowException()
            
#           if self.is_leaf:
#             # binary search to insert into sorted position
#             for i, x in enumerate(self.items):
#               if item < x:
#                 self.items.insert(i, item)
#                 return
#           else:
#             # TODO: binary search to find the correct node to insert into
#             return
      
#       def __init__(self):
#         self.root = None
      
#       def add_item(self, item):
#         if self.root is None:
#           self.root = self.Node(True)
#           self.root.add_item(item)
#           return
#         # TODO: finish method
#         ...
#     return BTree

