from __future__ import annotations

from node import Node

class Walker:
  """
  #### Tree layout using Walker's Algorithm

  Properties:
  - `config`: configuration of spacing, maximum depth, etc.
  - `nodes`: all nodes in the tree

  Methods:
  - `add_node(node)`: add node to the tree, returns `None`
  - `add_nodes(nodes)`: add list of nodes to the tree, returns `None`
  - `position_tree()`: do the layout, returns `None`
  """
  def __init__(self, rootX: int = 50, rootY: int = 50, debug: bool = False) -> None:
    """
    constructor

    Parameters:
    - `rootX`: type `int`, optional, the least x coordinate of the graph, defaults to 50
    - `rootY`: type `int`, optional, the least y coordinate of the graph, defaults to 50
    - `debug`: type `bool`, optional, whether to print debugging information, defaults to False

    Returns: None
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
    self._prev_at_level: list[Node or None] = [None] * self.config['MAX_DEPTH']
    self.debug = debug

  def add_node(self, node: Node) -> None:
    """
    add node to the tree

    Parameters:
    - `node`: type `Node`, required

    Returns: None
    """
    self.nodes.append(node)

  def add_nodes(self, nodes: list[Node]) -> None:
    """
    add list of nodes to the tree

    Parameters:
    - `nodes`: type `list[Node]`, required

    Returns: None
    """
    for node in nodes:
      self.add_node(node)

  def position_tree(self) -> None:
    """
    do the layout

    Parameters: None

    Returns: None
    """
    self._firstwalk(self.nodes[0], 0)
    if self.debug:
      print('[position_tree] _firstwalk completed')
      print('\tNode\tPRELIM\tMODIFIER')
      for node in self.nodes:
        print(f'\t{node.id}\t{node.prelim}\t{node.modifier}')

    final = self._secondwalk(self.nodes[0], 0, 0)
    if self.debug:
      print(f'[position_tree] _secondwalk completed, returns {final}')
      print('\tNode\tX\tY')
      for node in self.nodes:
        print(f'\t{node.id}\t{node.x}\t{node.y}')

  def _firstwalk(self, curr: Node, level: int) -> None:
    """
    post-order traversal and assigns preliminary x coordinate and modifier values to each node

    `_apportion` is called where tree balancing is needed

    Parameters:
    - `curr`: type `Node`, required, local root
    - `level`: type `int`, required, current level

    Returns: None
    """
    if self.debug: print(f'[_firstwalk] Node {curr.id}, Level: {level}, isLeaf: {curr.is_leaf()}')

    curr.modifier = 0
    curr.left_neighbor = self._prev_at_level[level]
    if self.debug: print(f'[_firstwalk] curr.left_neighbor = {curr.left_neighbor.id if curr.left_neighbor else None}')
    self._prev_at_level[level] = curr
    if self.debug: print(f'[_firstwalk] _prev_at_level[{level}] = {self._prev_at_level[level].id}')

    if curr.is_leaf() or level == self.config['MAX_DEPTH']:
      if self.debug: print(f'[_firstwalk] has left sibling: {bool(curr.left_sibling)}')
      if curr.left_sibling:
        curr.prelim = curr.left_sibling.prelim + self.config['NODE_SEPARATION'] + self.config['NODE_SIZE']
      else: curr.prelim = 0

    else:
    # curr is not a leaf, so call _firstwalk recursively for each of its offspring
      left = right = curr.get_leftmost_child()
      self._firstwalk(left, level + 1)

      while right.right_sibling:
        right = right.right_sibling
        self._firstwalk(right, level + 1)

      midpoint = (left.prelim + right.prelim) / 2

      if self.debug: print(f'[_firstwalk] has left sibling: {bool(curr.left_sibling)}')
      if curr.left_sibling:
        curr.prelim = curr.left_sibling.prelim + self.config['NODE_SEPARATION'] + self.config['NODE_SIZE']
        curr.modifier = curr.prelim - midpoint
        self._apportion(curr, level)
      else: curr.prelim = midpoint

    if self.debug: print(f'[_firstwalk] leaving from Node {curr.id}')

  def _apportion(self, curr: Node, level: int) -> None:
    """
    trace subtree contours and determines whether they are OK or there's overlapping

    if overlap exists, this function will add spacing to the rightmost of the two
    subtrees being compared.

    The function will then add up the number of subtrees in between the two trees
    under comparison and will allocate the additional spacing among them

    Parameters:
    - `curr`: type `Node`, required, left lowest descendent of a tree
    - `level`: type `int`, required, current level

    Returns: None

    """
    if self.debug: print(f'[_apportion] Node {curr.id}, Level: {level}, leftMost: {curr.children[0].id}, neighbor: {curr.children[0].left_neighbor.id if curr.children[0].left_neighbor else None}')

    leftmost = curr.children[0]
    depth_to_stop = self.config['MAX_DEPTH'] - level
    neighbor = leftmost.left_neighbor
    compare_depth = 1

    while leftmost and neighbor and compare_depth <= depth_to_stop:
      if self.debug: print(f'[_apportion] compare_depth: {compare_depth}')
    # Compute the location of leftmost and where it should be with respect to neighbor
      left_mod_sum = 0
      right_mod_sum = 0
      leftmost_ancestor = leftmost
      neighbor_ancestor = neighbor

      for _ in range(0, compare_depth): # pylint: disable=unused-variable
        leftmost_ancestor = leftmost_ancestor.parent
        neighbor_ancestor = neighbor_ancestor.parent
        right_mod_sum += leftmost_ancestor.modifier
        left_mod_sum += neighbor_ancestor.modifier
        if self.debug: print(f'[_apportion] leftmost_ancestor: {leftmost_ancestor.id}, neighbor_ancestor: {neighbor_ancestor.id}, right_mod_sum: {right_mod_sum}, left_mod_sum: {left_mod_sum}')

      # Find the distance and apply it to curr's subtree
      # Add appropriate portions to smaller interior subtrees
      distance = neighbor.prelim + left_mod_sum + self.config['TREE_SEPARATION'] + self.config['NODE_SIZE'] - (leftmost.prelim + right_mod_sum)
      if self.debug: print(f'[_apportion] distance: {distance}')
      if distance > 0:
      # Count interior sibling subtrees in LeftSiblings
        left_siblings = 0
        temp = curr
        if self.debug: print(f'[_apportion] temp: {temp.id}, neighbor_ancestor: {neighbor_ancestor.id}')
        while temp and temp is not neighbor_ancestor:
          left_siblings += 1
          temp = temp.left_sibling
          if self.debug: print(f'[_apportion] temp: {temp.id if temp else None}, neighbor_ancestor: {neighbor_ancestor.id}')

        if temp:
        # Apply portions to appropriate leftsibling subtrees
          proportion = distance / left_siblings
          temp = curr
          while temp is not neighbor_ancestor:
            if self.debug: print('[_apportion] temp is not neighbor_ancestor')
            temp.prelim += distance
            temp.modifier += distance
            distance -= proportion
            temp = temp.left_sibling
        else:
          return
      ### end of distance > 0 ###

      # Determine the leftmost descendant of curr at the next lower level to compare its positioning against that of its neighbor
      compare_depth += 1
      if leftmost.is_leaf():
        leftmost = curr.get_leftmost(0, compare_depth)
      else: leftmost = leftmost.children[0]
      if leftmost: neighbor = leftmost.left_neighbor
    if self.debug: print(f'[_apportion] leaving from Node {curr.id}')
    ### end of _apportion ###

  def _secondwalk(self, curr: Node, level: int, mod_sum: int) -> bool:
    """
    pre-order traversal and calculates final x coordinates from modifier totals to each node

    Parameters:
    - `curr`: type `Node`, required, current node
    - `level`: type `int`, required, current level
    - `mod_sum`: type `int`, required, current mod_sum

    Returns: `True` if no errors, otherwise `False`
    """
    if self.debug: print(f'[_secondwalk] Node: {curr.id}, Level: {level}, mod_sum: {mod_sum}')

    result = True

    temp_x = 0
    temp_y = 0

    if level < self.config['MAX_DEPTH']:
      temp_x = self.config['X_TOP'] + curr.prelim + mod_sum
      temp_y = self.config['Y_TOP'] + (level * self.config['LEVEL_SEPARATION'])

      if self._checkExtentsRange(temp_x, temp_y):
        curr.x = temp_x
        curr.y = temp_y

        if len(curr.children) != 0: result = self._secondwalk(curr.children[0], level + 1, mod_sum + curr.modifier)
        if result and curr.right_sibling: result = self._secondwalk(curr.right_sibling, level, mod_sum)
      else: result = False
    else: result = True

    if self.debug: print(f'[_secondwalk] leaving from Node {curr.id}')
    return result

  def _checkExtentsRange(self, x: int, y: int) -> bool: # pylint: disable=invalid-name, unused-argument
    return True
