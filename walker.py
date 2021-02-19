from __future__ import annotations

from node import Node

class Walker:
  """
  #### Tree layout using Walker's Algorithm

  Properties:
  - `config`: configuration of spacing, maximum depth, etc.
  - `nodes`: all nodes in the tree

  Methods:
  - `addNode(node)`: add node to the tree, returns `None`
  - `positionTree()`: do the layout, returns `None`
  """
  def __init__(self, rootX: int = 50, rootY: int = 50, debug: bool = False) -> None: 
    """
    constructor
    """
    self.config = {
      'LEVEL_SEPARATION': 160,
      'NODE_SEPARATION': 7,
      'TREE_SEPARATION': 20,
      'NODE_SIZE': 25,
      'MAX_WIDTH': 25,
      'MAX_DEPTH': 25,
      'X_MAX': 10000,
      'Y_MAX': 10000,
      'X_TOP': rootX,
      'Y_TOP': rootY
    }
    self.nodes: list[Node] = []
    self._prevAtLevel: list[Node or None] = [None] * self.config['MAX_DEPTH']
    self.debug = debug

  def addNode(self, node: Node) -> None:
    """
    add node to the tree

    Parameters:
    - `node`: type `Node`, required

    Returns: None
    """
    self.nodes.append(node)

  def addNodes(self, nodes: list[Node]) -> None:
    for node in nodes: self.addNode(node)

  def positionTree(self) -> None:
    """
    do the layout

    Parameters: None

    Returns: None
    """
    self._firstwalk(self.nodes[0], 0)
    if self.debug: print('[positionTree] _firstwalk completed')
    self._secondwalk(self.nodes[0], 0, 0)

  def _firstwalk(self, currNode: Node, level: int) -> None:
    """
    post-order traversal and assigns preliminary x coordinate and modifier values to each node

    `_apportion` is called where tree balancing is needed

    Parameters:
    - `currNode`: type `Node`, required, local root
    - `level`: type `int`, required, current level

    Returns: None
    """
    if self.debug: print(f'[_firstwalk] Node {currNode.id}, Level: {level}, isLeaf: {currNode.isLeaf()}')

    currNode.modifier = 0
    midPoint = 0
    currNode.prev = self._prevAtLevel[level]
    self._prevAtLevel[level] = currNode

    if not (currNode.isLeaf() or level == self.config['MAX_DEPTH']):
    # currNode is not a leaf, so call _firstwalk recursively for each of its offspring
      left = currNode.getLeftMostChild()
      right = currNode.getRightMostChild()
      self._firstwalk(left, level + 1)

      while left.rightSibling:
        left = left.rightSibling
        self._firstwalk(left, level + 1)

      midPoint = (currNode.children[0].preX + currNode.children[-1].preX) / 2

      if currNode.leftSibling:
        currNode.preX = currNode.leftSibling.preX + self.config['NODE_SEPARATION'] + self.config['NODE_SIZE']
        currNode.modifier = currNode.preX - midPoint
        self._apportion(currNode, level)
      else: currNode.preX = midPoint

    else:
      if currNode.leftSibling: currNode.preX =currNode.leftSibling.preX + self.config['NODE_SEPARATION'] + self.config['NODE_SIZE']
      else: currNode.preX = 0

    if self.debug: print('[_firstwalk] leaving')

  def _apportion(self, currNode: Node, level: int) -> None:
    """
    trace subtree contours and determines whether they are OK or there's overlapping

    if overlap exists, this function will add spacing to the rightmost of the two 
    subtrees being compared.

    The function will then add up the number of subtrees in between the two trees 
    under comparison and will allocate the additional spacing among them

    Parameters:
    - `currNode`: type `Node`, required, left lowest descendent of a tree
    - `level`: type `int`, required, current level

    Returns: None

    """
    if self.debug: print(f'[_apportion] Node {currNode.id}, Level: {level}')

    leftMost = currNode.children[0]
    depthToStop = self.config['MAX_DEPTH'] - level
    neighbor = leftMost.prev
    compareDepth = 1

    while leftMost and neighbor and compareDepth <= depthToStop:
    # Compute the location of leftmost and where it should be with respect to neighbor
      rightModSum = leftModSum = 0
      leftMostAncestor = leftMost
      neighborAncestor = neighbor

      for i in range(0, compareDepth):
        leftMostAncestor = leftMostAncestor.parent
        neighborAncestor = neighborAncestor.parent
        rightModSum += leftMostAncestor.modifier
        leftModSum += neighborAncestor.modifier

      # Find the distance and apply it to currNode's subtree
      # Add appropriate portions to smaller interior subtrees
      distance = neighbor.preX + leftModSum + self.config['TREE_SEPARATION'] + self.config['NODE_SIZE'] - (leftMost.preX + rightModSum)
      if distance > 0:
      # Count interior sibling subtrees in LeftSiblings
        leftSiblings = 0
        tempNode = currNode
        while tempNode and tempNode is not neighborAncestor:
          leftSiblings += 1
          tempNode = tempNode.leftSibling
        
        if tempNode:
        # Apply portions to appropriate leftsibling subtrees
          proportion = distance / leftSiblings
          while tempNode and tempNode is not neighborAncestor:
            tempNode.preX += distance
            tempNode.modifier += distance
            distance -= proportion
            tempNode = tempNode.leftSibling
        else: return
      ### end of distance > 0 ###

      # Determine the leftmost descendant of currNode at the next lower level to compare its positioning against that of its neighbor
      compareDepth += 1
      if leftMost.isLeaf(): leftMost = currNode.getLeftMost(0, currNode)
      else: leftMost = leftMost.children[0]
      if leftMost: neighbor = leftMost.prev
    if self.debug: print('[_apportion] leaving')
    ### end of _apportion ###

  def _secondwalk(self, currNode: Node, level: int, modSum: int) -> bool:
    """
    pre-order traversal and calculates final x coordinates from modifier totals to each node

    Parameters:
    - `currNode`: type `Node`, required, current node
    - `level`: type `int`, required, current level
    - `modSum`: type `int`, required, current modSum

    Returns: `True` if no errors, otherwise `False`
    """
    if self.debug: print(f'[_secondwalk] Node: {currNode.id}, Level: {level}, modSum: {modSum}')

    result = True

    tempX = 0
    tempY = 0

    newModSum = 0

    if level < self.config['MAX_DEPTH']:
      tempX = self.config['X_TOP'] + currNode.preX + modSum
      tempY - self.config['Y_TOP'] + (level * self.config['LEVEL_SEPARATION'])

      if self._checkExtentsRange(tempX, tempY): 
        currNode.x = tempX
        currNode.y = tempY

        if len(currNode.children) != 0: result = self._secondwalk(currNode.children[0], level + 1, modSum + currNode.modifier)
        if result and currNode.rightSibling: result = self._secondwalk(currNode.rightSibling, level, modSum)
      else: result = False
    else: result = True

    if self.debug: print('[_secondwalk] leaving')
    return result

  def _checkExtentsRange(self, x: int, y: int) -> bool:
    return True