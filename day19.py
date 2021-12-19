import numpy as np
import pprint


def is_in_list(x, arr):
    return any((x == a).all() for a in arr)


scanner0 = [
    np.array([0,2]),
    np.array([4,1]),
    np.array([3,3]),
]

scanner1 = [
    np.array([-1,-1]),
    np.array([-5,0]),
    np.array([-2,1]),
]

def find_scanner_coords(scanner0, scanner1):
    """
    Given two lists of beacon coordinates from two scanners, returns the coordinates of
    scanner1 relative to scanner0 if it can, or None if there are not enough overlapping beacons.
    Assumes scanners have the same orientation
    """
    for beacon in scanner1:
        # if we know which beacons to match up, then we can find the coordinates of the scanner
        # so, we'll find which beacon in scanner1 is beacon0 of scanner0

        beacon0 = scanner0[0]
        difference = beacon0 - beacon

        # convert beacon0 (in scanner0 space) to scanner1 space
        beacon0_in_scanner1_space = beacon0 - difference
        # print(beacon0_in_scanner1_space)

        if (is_in_list(beacon0_in_scanner1_space, scanner1)):
            # it should match for enough beacons, and if so then we know that the coords of scanner1 in scanner0 space is (x_distance, y_distance)

            found = all([ # TODO: all? or do we just need at least 12
                is_in_list(scanner0_beacon - difference, scanner1)
                for scanner0_beacon in scanner0
            ])

            if found:
                return difference
    return None

res = find_scanner_coords(scanner0, scanner1)
print(res)