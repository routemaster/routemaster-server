import itertools
from math import acos, ceil, cos, pi, sin
import operator

# http://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html
EARTH_RADIUS_M = 6371000

def journey_scores(*waypoints):
    traveled_m = path_length_m(*waypoints)
    straight_line_m = path_length_m(waypoints[0], waypoints[-1])
    try:
        efficiency = max(0, ceil(200 * straight_line_m**2 / traveled_m**2 - 100))
    except ZeroDivisionError:
        efficiency = 0
    return efficiency, traveled_m

def path_length_m(*waypoints):
    ll = operator.attrgetter("latitude", "longitude")
    quads = (ll(w1) + ll(w2) for w1, w2 in zip(waypoints, waypoints[1:]))
    return sum(itertools.starmap(distance_between_m, quads))

def distance_between_m(lat1, lon1, lat2, lon2):
    """Return the distance along a spherical Earth between two lat/lon pairs.

    From http://www.johndcook.com/python_longitude_latitude.html
    """
    phi1 = (90. - lat1) * pi / 180.
    phi2 = (90. - lat2) * pi / 180.
    theta1 = lon1 * pi / 180.
    theta2 = lon2 * pi / 180.
    arc_length = acos(sin(phi1) * sin(phi2) * cos(theta1 - theta2) +
                      cos(phi1) * cos(phi2))
    return arc_length * EARTH_RADIUS_M
