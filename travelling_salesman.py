

def nearest_neighbor(points, dist_infor_points):
    """Building list containing points in order

    Parameters
    ----------
    points : list
        List contain the points
    dist_infor_points : dictionary
        The dictionary contain distance between points pair by pair of the tour

    Returns
    -------
    points list
        list the points have been visited
    """

    # initialization: start with a partial tour with the fist point in points
    tour = []
    start = 0
    tour.append(start)

    while start != points[-1]:
        i = 1
        for point in points:
            if point not in tour:
                id_min_dist = point
                break
        # Select a point that is not yet in the tour and that is closer to the last point of the partial tour
        while i < len(points):
            if i == start or i in tour:
                i += 1
                continue
            if i == points[-1] and len(tour) < len(points) - 1:
                i += 1
                continue

            if dist_infor_points[(start, i)] < dist_infor_points[(start, id_min_dist)]:
                id_min_dist = i
            i += 1
        start = id_min_dist

        # Insert the selected point at the end of the partial tour
        tour.append(start)

    return tour

def cal_total_distance(route, dist_route):
    """Calculate total distance of the route

    Parameters
    ----------
    route : list
        The route
    dist_route : dictionary
        The information of route: contain distance between points pair by pair of the tour
    
    Returns
    -------
    total distance
        The total distance that be calculated between points along the route
    """

    total_dist = 0

    i = 0
    num_point = len(route)
    while i < num_point - 1:
        total_dist += dist_route[(route[i], route[i+1])]
        i += 1

    return total_dist


def two_opt_swap(route, i, k):
    """Swap two partial route in a route
    
    Parameters
    ----------
    route : list
        The route need to exchange
    i, k : numbers
        position of the route that needs to swap 

    Returns
    -------
    new route
        new route after be changed
    """

    a = route[i:k+1]
    a.reverse()
    return route[:i] + a + route[k+1:]


def route_improvement(route, dist_route):
    """Improve the route by applying 2-opt
    
    Parameter
    ---------
    route : list
        The route need to improve
    dist_route : dictionary
        The information of route: contain distance between points pair by pair of the tour

    Returns
    -------
    new route
        new route after be improved
    """

    no_improvement = False
    while no_improvement is False:
        best_dist = cal_total_distance(route, dist_route)
        num_point = len(route)
        i = 1
        done = False
        while i < num_point - 1:
            k = i + 1
            while k < num_point - 1:
                new_route = two_opt_swap(route, i, k)
                new_dist = cal_total_distance(new_route, dist_route)
                if new_dist < best_dist:
                    route = new_route
                    best_dist = new_dist
                    done = True
                    break
                k += 1
            if done:
                break
            i += 1
        if done is False:
            no_improvement = True

    return route
