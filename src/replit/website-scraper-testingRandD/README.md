# About
This project is a collection of larger and more complete(it is usable with an output) code modules

# Files
## main
### makeDoc
CLI function to create a docstring

## web_scraping
A short script using the requests library to "scrape" the selected websites

## functional_programs
File where all variables are first order function objects/higher order functions 

Where I attempted to replicate all list functions as well as function composition functions

although the functions work for intended cases*, when unintended objects are passed in, who knows what will happen
> *(but sometimes only the complex cases, note foldl)

Testing grounds for makeDoc in `main.py`
## monad
a library class that defines a moad-ified version of list and maybe

> implementation of mMaybe prevents the existance of a Just(None)

Precursor of monad library in my [NEA](https://github.com/AndycptOrg/NEA-Calculator/blob/main/code/monad.py)

## GrowingPlant
Experiement of OOP Patterns:
- visitor
- observer
- delegation

Done through a self growing "plant"

plant being able to "grow" by creating recursive structure

And alter their position in the structure by calling an update function defiend by the observer

Instructions can be given via a visitor where it "visits" all elements of the plant structure

These instructions/visitor action is delegated to nested objects/structures

> There is a single monster lambda used as to pretty print the plant
> 
> That was crazy, which was then replicated in my [NEA](https://github.com/AndycptOrg/NEA-Calculator/blob/main/code/utilities.py#L62) with minor adjustments

There is an acompanying CLI watering loop which grows the plant infinitely



## GreatestCommonSubSequence
modified Levenshtein Distance algorithm

Naive recursive implementation

## DataStructures
Includes:
- Heaps(Min, max, or any comparison)
> Implemented with an "array" (as close as a list is an array) as opposed to a noded/recursive/pointer based structure

- Doubley Linked Lists

- Binary Tree
> Implemented using a noded structure as the tree is not (intended to have) self balancing
>
> Where all items in the sub-nodes to the left are less than or equal to the item in the node, 
>
> and all items in the right sub-nodes are greater than or equal to the item in the node

- Simple B-Tree
> A binary tree, but each node can store n items and dynamically restructures itself as items are inserted and removed
>
> There is a recursive implementation of getting a slice of the items within
>
> For this specific implmentation, not all items are stored in the leaf nodes, the seperators in the branches are actually only stored in the non-leaf nodes
>
> Most of the logic executed by the datastructure is delegated to the Node class within the BTree class  

- DataBaseTree
> This was inteneded to be a linked B-Tree where all sequential leaf nodes have a reference to the previous and next leaf node, 
>
> theoretically speeding up `get_slice` in the Simple B-Tree

- BTreeFactory
> There was an attempt at creating a BTree factory object that can specify when the internal nodes resize,
>
> but this was later succeeded by the constructor with the size as a parameter in BTree to reduce implementation concerns
