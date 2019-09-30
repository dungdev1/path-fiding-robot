import matplotlib.pyplot as plt
import numpy as np 



def read_file(filename):
    """Read data file and analysis that into needed informations"""
    with open(filename) as f:
        lines = f.read().splitlines() 
    space_lim = [int(x) for x in lines[0].split(',')]
    points_start_end = [int(x) for x in lines[1].split(',')]
    num_poly = int(lines[2])
    points_arr = []

    i = 3
    while(i<len(lines)):
        points_arr.append([int(x) for x in lines[i].split(',')])
        i += 1

    return {
        "space_lim": space_lim,
        "points_start_end": points_start_end,
        "num_poly": num_poly,
        "points_arr": points_arr
    }

