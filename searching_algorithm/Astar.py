class node():
    def __init__(self, parent = None , X = 0, Y = 0):
        self.parent = parent
        self.X = X
        self.Y = Y
        self.f = 0
        self.h = 0
        self.g = 0
    def __isGoal__(self, other):
        return (self.X == other.X) and (self.Y == other.Y)



##Ham tim khoang cach ngan nhat
def find_least_fValue(open_list) -> node:
    current_node = open_list[0]
    current_index = 0
    for idex, item in enumerate(open_list):
        if item.f < current_node.f:
            current_node = item
            current_index = idex
    return current_node, current_index

##Duong di tu startoint toi endpoint
def path(current_node) -> list:
    X = []
    Y = []
    while current_node is not None:
        X.append(current_node.X)
        Y.append(current_node.Y)
        current_node = current_node.parent
    X[::-1]
    Y[::-1]
    return X, Y

#Kiem tra xem no co nam tren da giac hay khong
def inBarrier(x , y , Barrier):
    if (x,y) in Barrier:
        return True
    return False


#Kiem tra nam trong khoang cho phep
def outRange(x, y, heigh, width):
    if x < 0 or x > width:
        return True
    if y < 0 or y > heigh:
        return True
    return False

#Khong di cheo neu 2 o ben canh o cheo nam tren canh da giac
def Rule(currentX, currentY , x, y , Barrier):
    ## (x - 1 , y + 1)  (x, y + 1)  (x + 1, y + 1)
    ## (x -1 , y)       (x, y)      (x + 1, y)
    ## (x - 1, y - 1)   (x, y - 1)  (x + 1, y - 1)
    ## De di cheo duoc thi cac o lan can khong duoc nam tren canh da giac
    if (x, y) == (currentX + 1, currentY + 1):
        if(currentX, currentY + 1) in Barrier and (currentX + 1, currentY) in Barrier:
            return False
        return True
    if (x, y) == (currentX - 1 , currentY + 1):
        if(currentX - 1, currentY) in Barrier and (currentX, currentY + 1) in Barrier:
            return False
        return True
    if (x, y) == (currentX - 1, currentY - 1):
        if (currentX - 1, currentY) in Barrier and (currentX, currentY - 1) in Barrier:
            return False
        return True
    if (x, y) == (currentX + 1, currentY -1):
        if (currentX, currentY - 1) in Barrier and (currentX + 1, currentY) in Barrier:
            return False
        return True


#Sinh ra con, toi da 8 con
def generate_child(current_node, Barrier, heigh, width) -> list:
    ## x, y
    ## (x, y - 1), (x, y + 1)
    ## (x - 1, y), (x + 1 ,y)
    ## (x + 1, y - 1), (x + 1 , y + 1)
    ## (x - 1, y - 1), (x - 1 , y + 1)
    ## Thong thuong se sinh ra 1 node se sinh ra 8 node
    ## Nhung tuy vao dieu kien ma se sinh ra duoc so luong node khac nhau

    result = []
    for newposition in [(0, - 1), (0, 1), (-1, 0), (1, 0), (1, -1), (1, 1), (-1, -1), (-1, 1)]:
        px = current_node.X + newposition[0]
        py = current_node.Y + newposition[1]

        ##Neu la vat can
        if inBarrier(px, py, Barrier) is True:
            continue
        
        ##Nam ngoai range
        if outRange(px, py, heigh, width) is True:
            continue

        ##Khong cho phep di cheo 2 giua 2 o tren canh da giac
        if Rule(current_node.X, px, py, current_node.Y, Barrier) is False:
            continue

        ##Neu thoa man luat tao node moi
        child_node = node(current_node, px, py)
        result.append(child_node)
    
    return result


#Kiem tra diem do co phai diem cheo cua currentnode hay khong
def isDiagonalPoint(child, current_node) -> bool:
    if child.X == current_node.X - 1 and child.Y == current_node.Y + 1:
        return True
    if child.X == current_node.X - 1 and child.Y == current_node.Y - 1:
        return True
    if child.X == current_node.X + 1 and child.Y == current_node.Y + 1:
        return True
    if child.X == current_node.X + 1 and child.Y == current_node.Y - 1:
        return True
    return False

def searchAstar(xStart, yStart, xEnd, yEnd, heigh, width, xBarrier, yBarrier):
    ##Conver x,y barrier to tuple barrier
    #import pdb; pdb.set_trace()
    index = 0
    Barrier = []
    while index < len(xBarrier):
        tmp = (xBarrier[index], yBarrier[index])
        Barrier.append(tmp)
        index += 1   

    ##Initialize 
    start_node = node(None, xStart, yStart)
    end_node = node(None, xEnd, yEnd)
    open_list = []
    closed_list = []

    #import pdb; pdb.set_trace()
    ##Add the start node
    open_list.append(start_node)

    while len(open_list) > 0:
        current_node, current_index = find_least_fValue(open_list)

        ##Remove from openList and add closedList
        open_list.pop(current_index)
        closed_list.append(current_node)
        if current_node.__isGoal__(end_node) is True:
            ##Backtrack list path
            return path(current_node)
        
        #Generate children
        children = []
        children = generate_child(current_node, Barrier, heigh, width)
        #import pdb; pdb.set_trace()   
        for child in children:
            #for closed_child in closed_list:
            #    if child == closed_list:
            #        continue

            ##Use Phytagorean theorem
            #Set f, g, h value
            if isDiagonalPoint(child, current_node) is True:
                child.g = current_node.g + 1.5
            else:
                child.g = current_node.g + 1

            child.h =  ((child.X - end_node.X)**2) + ((child.Y - end_node.Y)**2)

            child.f = child.g + child.h
        
            for open_node in open_list:
                 if child == open_node and child.g > open_node.g:
                    continue
        
            open_list.append(child)
    pass

def pathcost(xList, yList) -> float:
    cost = 0
    idex = 0
    #import pdb; pdb.set_trace()
    ## (x - 1 , y + 1)  (x, y + 1)  (x + 1, y + 1)
    ## (x -1 , y)       (x, y)      (x + 1, y)
    ## (x - 1, y - 1)   (x, y - 1)  (x + 1, y - 1)
    while idex < len(xList) - 1:
        if xList[idex] == xList[idex + 1]:
            if yList[idex] + 1 == yList[idex + 1]:
                cost += 1.0
            if yList[idex] - 1 == yList[idex + 1]:
                cost += 1.0

        if xList[idex] - 1 == xList[idex + 1]:
            if yList[idex] + 1 == yList[idex + 1]:
                cost += 1.5
            if yList[idex] - 1 == yList[idex + 1]:
                cost += 1.5
            if yList[idex] == yList[idex + 1]:
                cost += 1
        #import pdb; pdb.set_trace()
        if xList[idex] + 1 == xList[idex + 1]   :
            if yList[idex] + 1 == yList[idex + 1]:
                cost += 1.5

            if yList[idex] == yList[idex + 1]:
                cost += 1

            if yList[idex] - 1 == yList[idex + 1]:
                cost += 1.5

        idex += 1
    return cost

