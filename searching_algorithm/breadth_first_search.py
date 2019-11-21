def is_goes_into_poly(xlist, ylist, x_parent, y_parent, x0, y0):
    """Check if a point goes into a polygon or not?

    Parameters
    ----------
    xlist : list
        x coordinate of the points
    ylist : list
        y coordinate of the points
    x_parent : numbers
        x coordinate of the parent node of the point needs to be checked
    y_parent : numbers
        y coordinate of the parent node of the point needs to be checked
    x0 : numbers
        x coordinate of the point needs to be checked
    y0 : numbers
        y coordinate of the point needs to be checked
    """

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
    """
    A class used to represent a Node

    Attributes
    ----------
    parent : Node
        the parent node of the current node (default None)
    coordinateX : int
        x coordinate of the current node (default 0)
    coordinateY : int
        y coordinate of the current node (default 0)
    dist : numbers
        the distance of the first node in the graph to current node (default 0)
    """

    def __init__(self, parent=None, coordinateX=0, coordinateY=0, dist=0):
        """
        Parameters
        ----------
        parent : Node
            The parent node of the current node (default None)
        coordinateX : int
            x coordinate of the current node (default 0)
        coordinateY : int
            y coordinate of the current node (default 0)
        dist : numbers
            The distance of the first node in the graph to current node (default 0)
        """

        self.parent = parent
        self.coordinateX = coordinateX
        self.coordinateY = coordinateY
        self.dist = dist

class Graph():
    """
    A class used to represent a Graph

    Atributes
    ---------
    nodes : list
        the list of nodes in the graph
    graph_lim : tuple
        the limit of the graph(horizontal axis, vertical axis)
    xlist : list
        x coordinate of the points
    ylist : list
        y coordinate of the points
    start_node : tuple
        the start node of the graph
    end_node : tuple
        the end node of the graph

    Methods
    -------
    add_nodes(node)
        Add a node to the graph
    is_complete(node)
        Check whether the graph spread is over
    is_exist(node_c)
        Check whether a node is in the graph
    node_pos(node_c)
        Get the position of a node in the graph
    spread_node()
        Spread nodes in the graph
    find_route(pos_end_node)
        Find the route from the last node to the fist node
    """

    def __init__(self, graph_lim, xlist, ylist, start_node, end_node):
        """
        Parameters
        ----------
        graph_lim : tuple
            The limit of the graph (horizontal axis, vertical axis)
        xlist : list
            x coordinate of the points
        ylist : list
            y coordinate of the points
        start_node : tuple
            The start node of the graph
        end_node : tuple
            The end node of the graph
        """

        self.nodes = []
        self.graph_lim = graph_lim
        self.xlist = xlist
        self.ylist = ylist
        self.start_node = start_node
        self.end_node = end_node
    
    def add_nodes(self, node):
        """Add a node to the graph

        Parameters
        ----------
        node : Node
            The node needs to be added
        """

        self.nodes.append(node)
    
    def is_complete(self, node):
        """Check whether the graph spread is over

        Parameters
        ----------
        node : Node
            The node needs to be checked
        """

        return self.end_node[0] == node.coordinateX and self.end_node[1] == node.coordinateY

    def is_exist(self, node_c):
        """Check whether a node is in the graph

        Parameters
        ----------
        node_c : Node
            The node needs to be checked
        """

        for node in self.nodes:
            if node_c.coordinateX == node.coordinateX and node_c.coordinateY == node.coordinateY:
                return True
        return False

    def node_pos(self, node_c):
        """Get the position of a node in the graph

        Parameters
        ----------
        node_c : Node
            The node that we need to get position
        
        Returns
        -------
        index
            the position of the node
        """

        i = 0
        while i < len(self.nodes):
            if node_c.coordinateX == self.nodes[i].coordinateX and node_c.coordinateY == self.nodes[i].coordinateY:
                return i
            i += 1

    def spread_node(self):
        """Spread nodes in the graph

        Returns
        -------
        index
            the position of the end node in the graph
        """

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
                        if is_goes_into_poly(self.xlist, self.ylist, new_node.parent.coordinateX, new_node.parent.coordinateY, new_node.coordinateX, new_node.coordinateY) is False:
                            self.add_nodes(new_node)
                            continue

                    if self.is_exist(new_node):
                        if new_node.dist < self.nodes[self.node_pos(new_node)].dist:
                            self.nodes[self.node_pos(new_node)].parent = new_node.parent
                            self.nodes[self.node_pos(new_node)].dist = new_node.dist
                            continue
                    else:
                        if is_goes_into_poly(self.xlist, self.ylist, new_node.parent.coordinateX, new_node.parent.coordinateY, new_node.coordinateX, new_node.coordinateY) is False:
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
        """Find the route from the last node to the fist node

        Parameters
        ----------
        pos_end_node : Node
            the position of the end node

        Returns
        -------
        list x coordinate, list y coordinate
            x coordinate and the corresponding y coordinate of the points in route 
        """
        
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