from node import Node
from walker import Walker

a = Node(id = 'A')
b = Node(id = 'B')
c = Node(id = 'C')
d = Node(id = 'D')
e = Node(id = 'E')
f = Node(id = 'F')
g = Node(id = 'G')
h = Node(id = 'H')
i = Node(id = 'I')
j = Node(id = 'J')
k = Node(id = 'K')
l = Node(id = 'L')
m = Node(id = 'M')
n = Node(id = 'N')
o = Node(id = 'O')

# level 0
o.children = [e, f, n]

# level 1
e.parent = o
e.rightSibling = f
e.children = [a, d]

f.parent = o
f.leftSibling = e
f.rightSibling = n

n.parent = o
n.leftSibling = f
n.children = [g, m]

# level 2
a.parent = e
a.rightSibling = d

d.parent = e
d.leftSibling = a
d.children = [b, c]

g.parent = n
g.rightSibling = m

m.parent = n
m.leftSibling = g
m.children = [h, i, j, k, l]

# level 3
b.parent = d
b.rightSibling = c

c.parent = d
c.leftSibling = b

h.parent = m
h.rightSibling = i

i.parent = m
i.leftSibling = h
i.rightSibling = j

j.parent = m
j.leftSibling = i
j.rightSibling = k

k.parent = m
k.leftSibling = j
k.rightSibling = l

l.parent = m
l.leftSibling = k

w = Walker(debug=True)

w.addNodes([o, e, f, n, a, d, g, h, b, c, h, i, j, k, l])

w.positionTree()

for node in [o, e, f, n, a, d, g, h, b, c, h, i, j, k, l]:
  print(f'Node: {node.id}, Final X: {node.x}')