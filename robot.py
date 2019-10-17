import matplotlib.pyplot as plt
import numpy as np
import searching_algorithm as searching
import contruct_heuristic

def read_file(filename):
    """Read data file and analysis that into needed informations"""
    with open(filename) as f:
        lines = f.read().splitlines() 
    space_lim = [int(x) for x in lines[0].split(',')]
    points_start_end = [int(x) for x in lines[1].split(',')]
    num_poly = int(lines[2])
    polygons = []

    i = 3
    while(i<len(lines)):
        polygon = {}
        polygon["x"] = []
        polygon["y"] = []
        j = 0
        line = [int(x) for x in lines[i].split(',')]
        while(j<len(line)):
            if j%2==0:
                polygon["x"].append(line[j])
            else:
                polygon["y"].append(line[j])
            j += 1
        polygons.append(polygon)
        i += 1

    return {
        "space_lim": space_lim,
        "points_start_end": points_start_end,
        "num_poly": num_poly,
        "polygons": polygons,
        #"vert_poly":
    }

def plot_line_low(x0, y0, x1, y1):
    """Draw line with slope between 0 and 1 or between 0 and -1"""
    dx = x1 - x0
    dy = y1 - y0
    yi = 1
    if dy < 0:
        yi = -1
        dy = -dy
    P = 2*dy - dx
    y = y0
    xlist = []
    ylist = []
    while(x0 <= x1):
        # return point
        xlist.append(x0)
        ylist.append(y)

        x0 += 1
        if P < 0:
            P += 2*dy
        else:
            P += 2*dy -2*dx
            y += yi

    return xlist, ylist
    
def plot_line_high(x0, y0, x1, y1):
    """Draw line with slope > 1 or < -1"""
    dx = x1 - x0
    dy = y1 - y0
    xi = 1
    if dx < 0:
        xi = -1
        dx = -dx
    P = 2*dx - dy
    x = x0
    xlist = []
    ylist = []
    while(y0 <= y1):
        # return point
        xlist.append(x)
        ylist.append(y0)

        y0 += 1
        if P < 0:
            P += 2*dx
        else:
            P += 2*dx - 2*dy
            x += xi

    return xlist, ylist

def plot_line(x0, y0, x1, y1):
    """"""
    xlist = []
    ylist = []
    if abs(y1 - y0) < abs(x1 - x0):
        if x0 > x1:
            xlist, ylist = plot_line_low(x1, y1, x0, y0)
        else:
            xlist, ylist = plot_line_low(x0, y0, x1, y1)
    else:
        if y0 > y1:
            xlist, ylist = plot_line_high(x1, y1, x0, y0)
        else:
            xlist, ylist = plot_line_high(x0, y0, x1, y1)
    return xlist, ylist

def plot_polygons(ax, fig, polygons):
    """Ploting polygon with scatter"""
    xlist = []                  
    ylist = []
    for polygon in polygons:
        length = len(polygon["x"])
        i = 0
        while i < length:
            if i == length - 1:
                x, y = plot_line(polygon["x"][-1], polygon["y"][-1], polygon["x"][0], polygon["y"][0])
            else:
                x, y = plot_line(polygon["x"][i], polygon["y"][i], polygon["x"][i+1], polygon["y"][i+1])
            ax.scatter(polygon["x"][i], polygon["y"][i], marker='o', color='green', zorder=2)
            i += 1
            xlist.extend(x)
            ylist.extend(y)

    ax.scatter(xlist, ylist)
    return xlist, ylist

# A(x0, y0), B(x1, y1), xlist, ylist are array contain X coordinate and Y coordinate corresponding
def searching_argorithm_name(x0, y0, x1, y1, xlist, ylist):
    """"""
    x = [], y= []
    return x, y # with x, y are arrays contain X coordinate and Y coordinate corresponding OF ROUTE

def is_inside_polygon(xlist, ylist, x0, y0):
    """"""
    # if the point on edge of the polygons
    for x in xlist:
        if x == x0 and ylist[xlist.index(x)] == x0:
            return True

    x_right_x0 = []
    for x in xlist:
        if x > x0 and ylist[xlist.index(x)] == y0:
            x_right_x0.append(x)

    num_touch_edge = 0
    i = 0
    quanl = len(x_right_x0)
    if quanl <= 1:
        return False

    while(i < quanl):
        if x_right_x0[i] + 1 != x_right_x0[i+1]:
            num_touch_edge += 1
        i += 1
    if num_touch_edge % 2 == 0:
        return False

    return True

# def make_graph(xlist, ylist, vertices_poly, xlim, ylim):
#     """""""
#     vertices = {}
#     vertices["x"] = [], vertices["y"] = []

#     edges = []
    
#     for i in range(1, xlim):
#         for j in range(1, ylim):
#             if is_inside_polygon(xlist, ylist, i, j):
#                 continue
#             vertices


def main(filename):
    """Processing main program"""
    infor = read_file(filename)
    xlim = infor.get("space_lim")[0]
    ylim = infor.get("space_lim")[1]

    infor_points = infor.get("points_start_end")
    points = []

    i = 0
    while i < len(infor_points):
        points.append((infor_points[i], infor_points[i+1]))
        i += 2

    num_poly = infor.get("num_poly")

    polygons = infor.get("polygons")
    fig = plt.figure()
    ax = plt.axes()

    ax.set_autoscale_on(False)
    ax.set_xticks(np.arange(0, xlim + 1, 1))
    ax.set_yticks(np.arange(0, ylim + 1, 1))  
    ax.grid(True)

    # ploting polygons
    xlist, ylist = plot_polygons(ax, fig, polygons)

    #-----------------------------------------------
    my_dict = {}
    i = 0
    num_points = len(points)
    while i < num_points:
        j = 0
        while j < num_points:
            g = searching.Graph((xlim, ylim), xlist, ylist, points[i], points[j])
            pos_end_node = g.spread_node()
            my_dict[(i, j)] = g.nodes[pos_end_node].dist
            j += 1
        i += 1


    stations = [x for x in range(num_points)]
    temp = stations[1]
    stations[1] = stations[len(stations)-1]
    stations[len(stations)-1] = temp

    route = contruct_heuristic.nearest_neighbor(stations, my_dict)
    print(route)
    print(contruct_heuristic.cal_total_distance(route, my_dict))
    new_route = contruct_heuristic.route_improvement(route, my_dict)
    print(new_route)
    print(contruct_heuristic.cal_total_distance(new_route, my_dict))

    #-----------------------------------------------
    # graph

    i = 0
    while i < len(new_route) - 1:
        g = searching.Graph((xlim, ylim), xlist, ylist, points[new_route[i]], points[new_route[i+1]])
        pos_end_node = g.spread_node()
        x, y = g.find_route(pos_end_node)
        ax.scatter(x, y, marker='o', color='yellow', zorder=2)
        ax.scatter([x[0], x[-1]], [y[0], y[-1]], marker='o', color='red', zorder=2)
        i += 1

    x = [points[0][0], points[1][0]]
    y = [points[0][1], points[1][1]]
    ax.scatter(x, y, marker='o', color='black', zorder=2)
    # plotting route
    # x, y = searching_argorithm_name(...)
    #ax.scatter(x, y, marker='o', color='red', zorder=2)

    plt.show()  

#if __name__ == "__main__":
main('input.txt')