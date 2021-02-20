from __future__ import annotations

class Node:
  """
  #### Node object to be used in Walker's algorithm.

  Properties:
  - `parent`: type `Node | None`, parent of the node
  - `leftSibling`: type `Node | None`, left sibling of the node
  - `rightSibling`: type `Node | None`, right sibling of the node
  - `children`: type `list[Node]`, children of the node
  - `id`: type `int`, ID of the node
  - `x`, `y`: type `int`, coordinates of the node
  - `preX`: type `int`, preliminary x coordinates of the node
  - `modifier`: type `int`, modifier value of the node
  - `leftNeighbor`: type `Node`, nearest neighbor of the node to the left at the same level

  Methods:
  - `__init__(parent = None, lSib = None, rSib = None, children = [], id = 0)`: constructor, returns `None`
  - `isLeaf()`: check whether the node is a leaf, returns `bool`
  - `isLeftMost()`: check whether the node is the leftmost child of its parent, returns `bool`
  - `isRightMost()`: check whether the node is the rightmost child of its parent, returns `bool`
  - `getLeftMostChild()`: get the leftmost child of the node, returns `None` if the node is a leaf, otherwise `Node`
  - `getRightMostChild()`: get the rightmost child of the node, returns `None` if the node is a leaf, otherwise `Node`
  - `getLeftMost(currLevel, searchDepth)`: get the leftmost descendant of the node at a given depth, returns `None` if the node is a leaf, otherwise `Node`

  """
  def __init__(self, parent: Node or None = None, lSib: Node or None = None, rSib: Node or None = None, children: list[Node] = [], id: int or str = 0) -> None:
    """
    constructor

    Parameters:
    - `parent`: type `Node | None`, optional, parent of the new node if exists, defaults to `None`
    - `lSib`: type `Node | None`, optional, left sibling of the new node if exists, defaults to `None`
    - `rSib`: type `Node | None`, optional, right sibling of the new node if exists, defaults to `None`
    - `children`: type `list[Node]`, optional, list of children of the new node if exists, defaults to `[]`
    - `id`: type `int | str`, ID of the new node, defaults to `0`

    Returns: `None`
    """
    self.parent = parent
    self.leftSibling = lSib
    self.rightSibling = rSib
    self.children = children
    self.id = id
    self.x = 0
    self.y = 0
    self.preX = 0
    self.modifier = 0
    self.prev: Node or None = None
  
  def isLeaf(self) -> bool:
    """
    check whether the node is a leaf

    Parameters: None

    Returns: `bool`
    """
    return len(self.children) == 0

  def isLeftMost(self) -> bool:
    """
    check whether the node is the leftmost child of its parent

    Parameters: None

    Returns: `bool`
    """
    if self.parent is None: return True
    return self.parent.children[0] is self

  def isRightMost(self) -> bool:
    """
    check whether the node is the rightmost child of its parent

    Parameters: None

    Returns: `bool`
    """
    if self.parent is None: return True
    return self.parent.children[-1] is self

  def getLeftMostChild(self) -> Node or None:
    """
    get the leftmost child of the node

    Parameters: None

    Returns: `None` if the node is a leaf, otherwise `Node`
    """
    if len(self.children) == 0: return None
    return self.children[0]

  def getRightMostChild(self) -> Node or None:
    """
    get the rightmost child of the node

    Parameters: None

    Returns: `None` if the node is a leaf, otherwise `Node`
    """
    if len(self.children) == 0: return None
    return self.children[-1]

  def getLeftMost(self, currLevel: int, searchDepth: int) -> Node or None:
    """
    get the leftmost descendant of the node at a given depth

    Parameters: 
    - `currLevel`: type `int`, required, current level of search
    - `searchDepth`: type `int`, required, the target level of search

    Returns: `None` if the node is a leaf, otherwise `Node`
    """
    if currLevel >= searchDepth: return self
    elif self.isLeaf(): return None
    else:
      currRightMost = self.getLeftMostChild()
      currLeftMost = currRightMost.getLeftMost(currLevel + 1, searchDepth)

      while currLeftMost is None and currRightMost.rightSibling is not None:
        currRightMost = currRightMost.rightSibling
        currLeftMost = currRightMost.getLeftMost(currLevel + 1, searchDepth)
      
      return currLeftMost
