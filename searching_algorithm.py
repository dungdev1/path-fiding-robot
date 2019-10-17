# import numpy as np

  
# This code is contributed by Divyanshu Mehta 

# # A(x0, y0), B(x1, y1), xlist, ylist are array contain X coordinate and Y coordinate corresponding
# def bellman_ford(x0, y0, x1, y1, xlim, ylim, xlist, ylist):
#     """"""
#     x = [], y= []
    
#     vertices = np.zeros

#     return x, y # with x, y are arrays contain X coordinate and Y coordinate corresponding OF ROUTE


# print(np.empty(shape=5,dtype=np.int32))
def is_inside_polygon(xlist, ylist, x_parent, y_parent, x0, y0):
    """"""
    # if the point on edge of the polygons
    points = []
    i = 0
    while i < len(xlist):
        if xlist[i] == x0 and ylist[i] == y0:
            return True
        points.append((xlist[i], ylist[i]))
        i += 1

    if x0 > x_parent and y0 > y_parent:
        if (x_parent + 1, y_parent) in points and (x_parent, y_parent + 1) in points:
            return True
    if x0 < x_parent and y0 > y_parent:
        if (x_parent - 1, y_parent) in points and (x_parent, y_parent + 1) in points:
            return True
    if x0 < x_parent and y0 < y_parent:
        if (x_parent - 1, y_parent) in points and (x_parent, y_parent - 1) in points:
            return True
    if x0 > x_parent and y0 < y_parent:
        if (x_parent + 1, y_parent) in points and (x_parent, y_parent - 1) in points:
            return True

    return False

class Node():
    def __init__(self, parent = None , coordinateX = 0, coordinateY = 0, dist = 0):
        self.parent = parent
        self.coordinateX = coordinateX
        self.coordinateY = coordinateY
        self.dist = dist

class Graph():
    """"""
    def __init__(self, graph_lim, xlist, ylist, start_node, end_node):
        """
        Graph Constructor\n
        graph_lim: lim of graph, is a tuple, e.g: (18, 22)\n
        xlist: list of x coordinator of edges in map\n
        ylist: list of y coordinator of edges in map
        """
        self.nodes = []
        self.graph_lim = graph_lim
        self.xlist = xlist
        self.ylist = ylist
        self.start_node = start_node
        self.end_node = end_node
    
    def add_nodes(self, node):
        """
        Function to add a node to graph\n
        node: node which need to be added
        """
        self.nodes.append(node)
    
    def is_complete(self, node):
        """"""
        return self.end_node[0] == node.coordinateX and self.end_node[1] == node.coordinateY

    def is_exist(self, node_c):
        """Check node which exist in graph?"""
        for node in self.nodes:
            if node_c.coordinateX == node.coordinateX and node_c.coordinateY == node.coordinateY:
                return True
        return False

    def node_pos(self, node_c):
        i = 0
        while i < len(self.nodes):
            if node_c.coordinateX == self.nodes[i].coordinateX and node_c.coordinateY == self.nodes[i].coordinateY:
                return i
            i += 1

    def spread_node(self):
        """Function to spread node in map"""

        # Initialize start node 
        cur_node = Node(parent=None, coordinateX=self.start_node[0], coordinateY=self.start_node[1])
        self.add_nodes(cur_node)
        i = 0

        while self.is_complete(cur_node) is False:
            nodes_among_curnode = []
            nodes_among_curnode.append((cur_node.coordinateX - 1, cur_node.coordinateY - 1))
            nodes_among_curnode.append((cur_node.coordinateX - 1, cur_node.coordinateY))
            nodes_among_curnode.append((cur_node.coordinateX - 1, cur_node.coordinateY + 1))
            nodes_among_curnode.append((cur_node.coordinateX, cur_node.coordinateY + 1))
            nodes_among_curnode.append((cur_node.coordinateX + 1, cur_node.coordinateY + 1))
            nodes_among_curnode.append((cur_node.coordinateX + 1, cur_node.coordinateY))
            nodes_among_curnode.append((cur_node.coordinateX + 1, cur_node.coordinateY - 1))
            nodes_among_curnode.append((cur_node.coordinateX, cur_node.coordinateY - 1))

            for node in nodes_among_curnode:
                if (node[0] > 0 and node[0] < self.graph_lim[0]) and (node[1] > 0 and node[1] < self.graph_lim[1]):
                    if nodes_among_curnode.index(node) % 2 == 0:
                        new_node = Node(parent=cur_node, coordinateX=node[0], coordinateY=node[1], dist=cur_node.dist + 1.5)
                    else:
                        new_node = Node(parent=cur_node, coordinateX=node[0], coordinateY=node[1], dist=cur_node.dist + 1)

                    if cur_node.parent == None:
                        if is_inside_polygon(self.xlist, self.ylist, new_node.parent.coordinateX, new_node.parent.coordinateY, new_node.coordinateX, new_node.coordinateY) is False:
                            self.add_nodes(new_node)
                            continue

                    if self.is_exist(new_node):
                        if new_node.dist < self.nodes[self.node_pos(new_node)].dist:
                            self.nodes[self.node_pos(new_node)].parent = new_node.parent
                            self.nodes[self.node_pos(new_node)].dist = new_node.dist
                            continue
                    else:
                        if is_inside_polygon(self.xlist, self.ylist, new_node.parent.coordinateX, new_node.parent.coordinateY, new_node.coordinateX, new_node.coordinateY) is False:
                            if (new_node.coordinateX, new_node.coordinateY) != (cur_node.parent.coordinateX, cur_node.parent.coordinateY):
                                self.add_nodes(new_node)

            if i + 1 >= len(self.nodes):
                return -1
            cur_node = self.nodes[i + 1]
            i += 1 

        return i # position of end node in graph
    
    def find_node(self):
        """"""
        xlist = []
        ylist = []
        for node in self.nodes:
            xlist.append(node.coordinateX)
            ylist.append(node.coordinateY)
        
        return xlist, ylist

    def find_route(self, pos_end_node):
        """"""
        
        if pos_end_node < 0:
            return [], []
        node = self.nodes[pos_end_node]
        xlist = []
        ylist = []
        xlist.append(node.coordinateX)
        ylist.append(node.coordinateY)
        while node.parent != None:
            xlist.append(node.parent.coordinateX)
            ylist.append(node.parent.coordinateY)
            node = node.parent

        return xlist, ylist

# is_inside_polygon(self.xlist, self.ylist, new_node.coordinateX, new_node.coordinateY) is False and
#g = Graph((22, 18), [5, 5], [3, 4], (1, 1), (8, 12))
#print(g.spread_node())