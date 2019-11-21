# Kiem tra xung quanh co diem nam tren canh nao khong 
# Ham nhan vao 1 node
# Tra ve True neu xung quanh node do co toi thieu 1 node nam trong da giac
# Tra ve False neu nguoc lai
def barrierAround(v) -> bool:
	for i in v.vertices:
		if i.barrier == True:
			return True
	return False

#Kiem tra xem co nam trong hinh da giac khong
#De nam trong 1 da giac thi 1 node tran tren phai thong qua 1 danh sach node tren canh da giac gap node chan duoi
def inBarrier(v, g):
	#Tim kiem diem chan tren
	blockPoint_Top = None
	blockPoint_Bottom = None
	for i in g.vertices:
		if i.coordinate[0] == v.coordinate[0] and i.coordinate[1] > v.coordinate[1] and i.barrier == True:
			blockPoint_Top = i
			break
	for i in g.vertices:
		if i.coordinate[0] == v.coordinate[0] and i.coordinate[1] < v.coordinate[1] and i.barrier == True:
			blockPoint_Bottom = i
			break

	#Khong tim thay diem chan tren, chan duoi => khong nam trong da giac		
	if blockPoint_Top == None or blockPoint_Bottom == None:
		return False
	open_list = []
	idex = 0
	open_list.append(blockPoint_Top)
	while idex < len(open_list):
		if barrierAround(open_list[idex]) is False:
			return False
		else:
			for i in open_list[idex].vertices:
				if i.barrier == True and i not in open_list:
					open_list.append(i)
			idex += 1
	if blockPoint_Bottom not in open_list:
		return False
	return True

# Tim kiem diem trong do thi
def findinGraph(g, x, y):
	for i in g.vertices:
		if i.coordinate == (x,y):
			return i
	return None

# Kiem tra xem node child cho nam cheo node current khong
# True neu dung va nguoc lai
def isDiagonalPoint(child, current_node) -> bool:
    if child.coordinate[0] == current_node.coordinate[0] - 1 and child.coordinate[1] == current_node.coordinate[1] + 1:
        return True
    if child.coordinate[0] == current_node.coordinate[0] - 1 and child.coordinate[1] == current_node.coordinate[1] - 1:
        return True
    if child.coordinate[0] == current_node.coordinate[0] + 1 and child.coordinate[1] == current_node.coordinate[1] + 1:
        return True
    if child.coordinate[0] == current_node.coordinate[0] + 1 and child.coordinate[1] == current_node.coordinate[1] - 1:
        return True
    return False

# Gia tri tu node current den start_point
def costpath(n):
	cost = 0
	while n != None:
		cost += n.weight
		n = n.parent
	return cost


class node():
		# Một node sẽ liên kết tối đa 8 node xung quanh
		# Node co the la nam trong/ ngoai da giac
		# Dist mac dinh la -1 
	def __init__(self, coordinate = (0,0), parent = None):
		self.vertices = [] #Danh sach list cac node lien ket
		self.coordinate = coordinate
		self.weight = - 1
		self.barrier = False
		self.parent = None
		pass
	def __isgoal__(self, other)->bool:
		return self.coordinate == other.coordinate

	def setBarrier(self, xBarrier, yBarrier):
		idex = 0
		while idex < len(xBarrier):
			if self.coordinate == (xBarrier[idex], yBarrier[idex]):
				self.barrier = True
				break
			else:
				idex += 1
		pass
	def addEdge(self, g):
		#(x-1,y+1)	(x,y+1)	(x+1,y+1)
		#(x-1,y)	(x,y)	(x+1,y)
		#(x-1,y-1)	(x,y-1)	(x+1,y-1)
		for i in g:
			if self.coordinate[0] - 1 == i.coordinate[0] :
				if self.coordinate[1] + 1 == i.coordinate[1]:
					self.vertices.append(i)
					continue
				if self.coordinate[1] == i.coordinate[1]:
					self.vertices.append(i)
					continue
				if self.coordinate[1] - 1 == i.coordinate[1]:
					self.vertices.append(i)
					continue

			if self.coordinate[0] == i.coordinate[0]:
				if self.coordinate[1] + 1 == i.coordinate[1]:
					self.vertices.append(i)
					continue
				if self.coordinate[1] - 1 == i.coordinate[1]:
					self.vertices.append(i)
					continue

			if self.coordinate[0] + 1 == i.coordinate[0]:
				if self.coordinate[1] + 1 == i.coordinate[1]:
					self.vertices.append(i)
					continue
				if self.coordinate[1] == i.coordinate[1]:
					self.vertices.append(i)
					continue
				if self.coordinate[1] - 1 == i.coordinate[1]:
					self.vertices.append(i)
					continue	



class graph():
	"""1 Do thi nhan vao chieu dai va chieu rong
		Sau do sinh ra cac node va sinh diem ke voi node ay	"""
	def __init__(self, width = 0, heigh = 0):
		self.vertices = []
		self.width = width
		self.heigh = heigh
	def generateNode(self, barrier):
		for i in range(self.width + 1):
			for j in range(self.heigh + 1):
					tmp = node((i,j))
					self.vertices.append(tmp)
		pass
	def generateEdge(self):
		for i in self.vertices:
			i.addEdge(self.vertices)


def bellman(xStart, yStart, xEnd, yEnd, width, heigh, xBarrier, yBarrier):
	#Initialize 
	g = graph(width,heigh)
	g.generateNode(None)
	#Các điểm thuộc nằm trên cạnh đa giác
	for i in g.vertices:
		i.setBarrier(xBarrier, yBarrier)
	#Initialize link
	for i in g.vertices:
		i.addEdge(g.vertices)
		pass
	#Initialize barrier
	for i in g.vertices:
		i.setBarrier(xBarrier, yBarrier)
	for i in g.vertices:
		if inBarrier(i,g) is True:
			i.barrier = True
	#Initialize start& end point
	start_node = findinGraph(g, xStart, yStart)
	start_node.weight = 0
	end_node = findinGraph(g, xEnd, yEnd)
	if start_node == None or end_node == None:
		print("Start point and end point can't find in graph")
	else:
		queue = []
		idex = 0
		j = 0
		#Dem so node co trong do thi khong nam trong da giac
		for i in g.vertices:
			if i.barrier == False:
				idex +=1
		queue.append(start_node)
		#Vong lap se ngung neu nhu trong queue khong the tao them node moi
		while (len(queue) < idex):
			current_node = queue[j]
			for i in current_node.vertices:
				tmp = 1
				if isDiagonalPoint(i, current_node):
					tmp = 1.5
					pass

				if i.barrier == False and i != start_node:
					if i not in queue:
						i.weight = tmp
						i.parent = current_node
						queue.append(i)
					else:
						cost = costpath(current_node) + tmp
						if cost < costpath(i):
							i.parent = current_node
							i.weight = tmp
			j += 1
			pass

	cost = costpath(end_node)
	X = []
	Y = []
	while end_node != None:
		X.append(end_node.coordinate[0])
		Y.append(end_node.coordinate[1])
		end_node = end_node.parent
	return X,Y,cost		






	

