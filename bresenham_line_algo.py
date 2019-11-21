def plot_line_low(x0, y0, x1, y1):
    """Draw line with slope between 0 and 1 or between 0 and -1

    Parameters
    ----------
    x0, y0 : numbers
        The corresponding x and y coordinate of the first point
    x1, y1 : numbers
        The corresponding x and y coordinate of the second point

    Returns
    -------
    xlist, ylist
        The list that contain coordinates of points from the first point and second points
    """

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
    """Draw line with slope > 1 or < -1
    
    Parameters
    ----------
    x0, y0 : numbers
        The corresponding x and y coordinate of the first point
    x1, y1 : numbers
        The corresponding x and y coordinate of the second point

    Returns
    -------
    xlist, ylist
        The list that contain coordinates of points from the first point and second points
    """

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
    """The main function performs drawing polygons
    
    Determine the first point and last point according to the octant

    Parameters
    ----------
    x0, y0
    x1, y1

    Returns
    -------
    xlist, ylist
        The list that contain coordinates of points from the first point and second points
    """

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
