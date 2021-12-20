import numpy as np
from pprint import pprint
import re


def is_in_list(x, arr):
    return any((x == a).all() for a in arr)


def all_rotations(coords):
    """
    Given a 3D point, returns a list of all 24 rotations
    """
    return [
        np.array([coords[0], coords[1], coords[2]]),
        np.array([coords[0], -coords[2], coords[1]]),
        np.array([coords[0], -coords[1], -coords[2]]),
        np.array([coords[0], coords[2], -coords[1]]),

        np.array([-coords[0], -coords[1], coords[2]]),
        np.array([-coords[0], coords[2], coords[1]]),
        np.array([-coords[0], coords[1], -coords[2]]),
        np.array([-coords[0], -coords[2], -coords[1]]),

        np.array([coords[1], coords[2], coords[0]]),
        np.array([coords[1], -coords[0], coords[2]]),
        np.array([coords[1], -coords[2], -coords[0]]),
        np.array([coords[1], coords[0], -coords[2]]),

        np.array([-coords[1], -coords[2], coords[0]]),
        np.array([-coords[1], coords[0], coords[2]]),
        np.array([-coords[1], coords[2], -coords[0]]),
        np.array([-coords[1], -coords[0], -coords[2]]),

        np.array([coords[2], coords[0], coords[1]]),
        np.array([coords[2], -coords[1], coords[0]]),
        np.array([coords[2], -coords[0], -coords[1]]),
        np.array([coords[2], coords[1], -coords[0]]),

        np.array([-coords[2], -coords[0], coords[1]]),
        np.array([-coords[2], coords[1], coords[0]]),
        np.array([-coords[2], coords[0], -coords[1]]),
        np.array([-coords[2], -coords[1], -coords[0]])
    ]


input_file = open('input/day19_test', 'r')
lines = input_file.read().splitlines()
input_file.close()

scanners = []
beacons = []
for line in lines:
    if line == "":
        scanners.append(beacons)
    elif re.match("--- scanner [0-9]+ ---", line):
        beacons = []
    else:
        res = re.search("(-?[0-9]+),(-?[0-9]+),(-?[0-9]+)", line)
        beacons.append(
            np.array([int(res.group(1)), int(res.group(2)), int(res.group(3))])
        )
scanners.append(beacons)
# pprint(scanners)


def find_scanner_coords(scanner0, scanner1, overlap_requirement):
    """
    Given two lists of beacon coordinates from two scanners, returns the coordinates of
    scanner1 relative to scanner0 if it can, or None if there are not enough overlapping beacons.
    Assumes scanners have the same orientation
    """
    scanner0_beacons_in_scanner1_space = []
    for beacon in scanner1:
        # if we know which beacons to match up, then we can find the coordinates of the scanner
        # so, we'll find which beacon in scanner1 is beacon0 of scanner0

        # for beacon_rotated in all_rotations(beacon):
        # print("aye")

        beacon0 = scanner0[0]
        difference = beacon0 - beacon

        # convert beacon0 (in scanner0 space) to scanner1 space
        beacon0_in_scanner1_space = beacon0 - difference
        scanner0_beacons_in_scanner1_space.append(beacon0_in_scanner1_space)
        # print(beacon0_in_scanner1_space)

    pprint(scanner0_beacons_in_scanner1_space)

    found = len([
        scanner0_beacon_in_scanner1_space
        for scanner0_beacon_in_scanner1_space in scanner0_beacons_in_scanner1_space
        if (is_in_list(scanner0_beacon_in_scanner1_space, scanner1))
    ])
    
    print(f"found {found} matching beacons")
    
    # for scanner0_beacon_in_scanner1_space in scanner0_beacons_in_scanner1_space:
    #     if (is_in_list(scanner0_beacon_in_scanner1_space, scanner1)):
    #         # it should match for enough beacons, and if so then we know that the coords of scanner1 in scanner0 space is difference
    #         print(scanner0_beacon_in_scanner1_space)
    #         found = sum([
    #             1 if is_in_list(scanner0_beacon - difference, scanner1) else 0
    #             for scanner0_beacon in scanner0
    #         ])

    #         print(f"found {found} matching beacons")

    #         if found >= overlap_requirement:
    #             return difference
    return None

res = find_scanner_coords(scanners[0], scanners[1], 12)
print(res)
