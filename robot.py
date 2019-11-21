import matplotlib.pyplot as plt
import numpy as np
import argparse
from searching_algorithm import breadth_first_search as searching
from searching_algorithm import Astar as astar
import travelling_salesman
import bresenham_line_algo as plot_line

parser = argparse.ArgumentParser()

parser.add_argument('--input_path', '-i', required=True, help='input path for the program')
parser.add_argument('specified_algo', type=int, help='index of specified algorithm: 1: BFS, 2: A*, 3:...')

args = parser.parse_args()

def read_file(filename):
    """Read data file and analysis that into needed informations

    Parameters
    ----------
    filename : string
        file name

    Returns
    -------
    space_lim
        The list that contain horizontal limit and vertical limit
    points_start_end
        The list that contain coordinate of start point and end point
    num_poly
        The number of polygons in the map
    polygons
        The information of polygons in map (coordinates of vertices)
    """

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
    }


def plot_polygons(ax, fig, polygons):
    """Ploting polygon with scatter

    Parameters
    ----------
    ax : Axes
        The Axes of the current figure
    fig : Figure
        The current figure
    polygons : list of dictionary
        Information of the polygons

    Returns
    -------
    xlist, ylist
        The list contains the entire x and y coordinates of the points that make up the polygons
    """

    xlist = []                  
    ylist = []
    for polygon in polygons:
        length = len(polygon["x"])
        i = 0
        while i < length:
            if i == length - 1:
                x, y = plot_line.plot_line(polygon["x"][-1], polygon["y"][-1], polygon["x"][0], polygon["y"][0])
            else:
                x, y = plot_line.plot_line(polygon["x"][i], polygon["y"][i], polygon["x"][i+1], polygon["y"][i+1])
            ax.scatter(polygon["x"][i], polygon["y"][i], marker='o', color='green', zorder=2)
            i += 1
            xlist.extend(x)
            ylist.extend(y)

    ax.scatter(xlist, ylist)
    return xlist, ylist

    """"""
    x = [], y= []
    return x, y # with x, y are arrays contain X coordinate and Y coordinate corresponding OF ROUTE

def main(filename, algorithm=1):
    """Main program processing

    - Get information from input file
    - Set information for figure
    - Plot polygons
    - Find shortest route
    - Print cost of the route
    - Plot route

    Parameters
    ----------
    filename : string
        The input file name
    algorithm : numbers
        The specified algorithm (default 1: BFS)
    """
    # Get information from input file
    # ---------------------------------------------------------------
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
    # ---------------------------------------------------------------

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
            if algorithm == 1:
                g = searching.Graph((xlim, ylim), xlist, ylist, points[i], points[j])
                pos_end_node = g.spread_node()
                my_dict[(i, j)] = g.nodes[pos_end_node].dist
            elif algorithm == 2:
                result = astar.searchAstar(points[i][0], points[i][1], points[j][0], points[j][1], ylim, xlim, xlist, ylist)
                my_dict[(i, j)] = astar.pathcost(result[0], result[1])

            j += 1
        i += 1

    stations = [x for x in range(num_points)]
    temp = stations[1]
    stations[1] = stations[len(stations)-1]
    stations[len(stations)-1] = temp

    route = travelling_salesman.nearest_neighbor(stations, my_dict)
    new_route = travelling_salesman.route_improvement(route, my_dict)
    total_cost = travelling_salesman.cal_total_distance(new_route, my_dict)
    print(new_route)

    print("Cost of the route: ", total_cost)
    #-----------------------------------------------

    i = 0
    while i < len(new_route) - 1:
        if algorithm == 1:
            g = searching.Graph((xlim, ylim), xlist, ylist, points[new_route[i]], points[new_route[i+1]])
            pos_end_node = g.spread_node()
            x, y = g.find_route(pos_end_node)
        elif algorithm == 2:
            result = astar.searchAstar(points[new_route[i]][0], points[new_route[i]][1], points[new_route[i+1]][0], points[new_route[i+1]][1], ylim, xlim, xlist, ylist)
            x = result[0]
            y = result[1]
        ax.scatter(x, y, marker='o', color='yellow', zorder=2)
        ax.scatter([x[0], x[-1]], [y[0], y[-1]], marker='o', color='red', zorder=2)
        i += 1

    x = [points[0][0], points[1][0]]
    y = [points[0][1], points[1][1]]
    ax.scatter(x, y, marker='o', color='black', zorder=2)

    plt.show()  

if __name__ == "__main__":
    main(args.input_path, args.specified_algo)