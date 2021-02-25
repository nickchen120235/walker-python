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
    if self.debug: 
      print('[positionTree] _firstwalk completed')
      print('\tNode\tPRELIM\tMODIFIER')
      for node in self.nodes: print(f'\t{node.id}\t{node.preX}\t{node.modifier}')
    final = self._secondwalk(self.nodes[0], 0, 0)
    if self.debug:
      print(f'[positionTree] _secondwalk completed, returns {final}')
      print('\tNode\tX\tY')
      for node in self.nodes: print(f'\t{node.id}\t{node.x}\t{node.y}')

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
    currNode.prev = self._prevAtLevel[level]
    if self.debug: print(f'[_firstwalk] currNode.prev = {currNode.prev.id if currNode.prev else None}')
    self._prevAtLevel[level] = currNode
    if self.debug: print(f'[_firstwalk] _prevAtLevel[{level}] = {self._prevAtLevel[level].id}')

    if currNode.isLeaf() or level == self.config['MAX_DEPTH']:
      if self.debug: print(f'[_firstwalk] has left sibling: {bool(currNode.leftSibling)}')
      if currNode.leftSibling: currNode.preX = currNode.leftSibling.preX + self.config['NODE_SEPARATION'] + self.config['NODE_SIZE']
      else: currNode.preX = 0

    else:
    # currNode is not a leaf, so call _firstwalk recursively for each of its offspring
      left = right = currNode.getLeftMostChild()
      self._firstwalk(left, level + 1)

      while right.rightSibling:
        right = right.rightSibling
        self._firstwalk(right, level + 1)

      midPoint = (left.preX + right.preX) / 2

      if self.debug: print(f'[_firstwalk] has left sibling: {bool(currNode.leftSibling)}')
      if currNode.leftSibling:
        currNode.preX = currNode.leftSibling.preX + self.config['NODE_SEPARATION'] + self.config['NODE_SIZE']
        currNode.modifier = currNode.preX - midPoint
        self._apportion(currNode, level)
      else: currNode.preX = midPoint

    if self.debug: print(f'[_firstwalk] leaving from Node {currNode.id}')

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
    if self.debug: print(f'[_apportion] Node {currNode.id}, Level: {level}, leftMost: {currNode.children[0].id}, neighbor: {currNode.children[0].prev.id if currNode.children[0].prev else None}')

    leftMost = currNode.children[0]
    depthToStop = self.config['MAX_DEPTH'] - level
    neighbor = leftMost.prev
    compareDepth = 1

    while leftMost and neighbor and compareDepth <= depthToStop:
    # Compute the location of leftmost and where it should be with respect to neighbor
      leftModSum = 0
      rightModSum = 0
      leftMostAncestor = leftMost
      neighborAncestor = neighbor

      for i in range(0, compareDepth):
        leftMostAncestor = leftMostAncestor.parent
        neighborAncestor = neighborAncestor.parent
        rightModSum += leftMostAncestor.modifier
        leftModSum += neighborAncestor.modifier
        if self.debug: print(f'[_apportion] leftMostAncestor: {leftMostAncestor.id}, neighborAncestor: {neighborAncestor.id}, rightModSum: {rightModSum}, leftModSum: {leftModSum}')

      # Find the distance and apply it to currNode's subtree
      # Add appropriate portions to smaller interior subtrees
      distance = neighbor.preX + leftModSum + self.config['TREE_SEPARATION'] + self.config['NODE_SIZE'] - (leftMost.preX + rightModSum)
      if self.debug: print(f'[_apportion] distance: {distance}')
      if distance > 0:
      # Count interior sibling subtrees in LeftSiblings
        leftSiblings = 0
        tempNode = currNode
        if self.debug: print(f'[_apportion] tempNode: {tempNode.id}, neighborAncestor: {neighborAncestor.id}')
        while tempNode and tempNode is not neighborAncestor:
          leftSiblings += 1
          tempNode = tempNode.leftSibling
          if self.debug: print(f'[_apportion] tempNode: {tempNode.id if tempNode else None}, neighborAncestor: {neighborAncestor.id}')
        
        if tempNode:
        # Apply portions to appropriate leftsibling subtrees
          proportion = distance / leftSiblings
          tempNode = currNode
          while tempNode is not neighborAncestor:
            if self.debug: print(f'[_apportion] tempNode is not neighborAncestor')
            tempNode.preX += distance
            tempNode.modifier += distance
            distance -= proportion
            tempNode = tempNode.leftSibling
        else:
          return
      ### end of distance > 0 ###

      # Determine the leftmost descendant of currNode at the next lower level to compare its positioning against that of its neighbor
      compareDepth += 1
      if leftMost.isLeaf(): leftMost = currNode.getLeftMost(0, compareDepth)
      else: leftMost = leftMost.children[0]
      if leftMost: neighbor = leftMost.prev
    if self.debug: print(f'[_apportion] leaving from Node {currNode.id}')
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
      tempY = self.config['Y_TOP'] + (level * self.config['LEVEL_SEPARATION'])

      if self._checkExtentsRange(tempX, tempY): 
        currNode.x = tempX
        currNode.y = tempY

        if len(currNode.children) != 0: result = self._secondwalk(currNode.children[0], level + 1, modSum + currNode.modifier)
        if result and currNode.rightSibling: result = self._secondwalk(currNode.rightSibling, level, modSum)
      else: result = False
    else: result = True

    if self.debug: print(f'[_secondwalk] leaving from Node {currNode.id}')
    return result

  def _checkExtentsRange(self, x: int, y: int) -> bool:
    return True