from collections import defaultdict
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


def change_reference(coords, origin, rotation):
    return origin + all_rotations(np.array(coords))[rotation]
    # return change_reference(difference, np.array([68,-1246,-43]), 6)


def find_scanner_coords(scanner0, scanner1, overlap_requirement):
    """
    Given two lists of beacon coordinates from two scanners, returns the coordinates of
    scanner1 relative to scanner0 if it can, or None if there are not enough overlapping beacons.
    """
    for i, beacon in enumerate(scanner1):
        # if we know which beacons to match up, then we can find the coordinates of the scanner
        # so, we'll find which beacon in scanner1 is beacon0 of scanner0

        for beacon0 in scanner0: # we need to pick a beacon from scanner0 that overlaps with scanner1
            for rotation, beacon_rotated in enumerate(all_rotations(beacon)):
                difference = beacon0 - beacon_rotated # if this is correct, difference is the position of scanner1 relative to scanner0

                # all scanner1 beacons converted to scanner0 space
                scanner1_in_scanner0_space = [
                    all_rotations(scanner1_beacon)[rotation] + difference
                    for scanner1_beacon in scanner1
                ]

                overlaps = [
                    scanner1_beacon
                    for scanner1_beacon in scanner1_in_scanner0_space
                    if is_in_list(scanner1_beacon, scanner0)
                ]

                found = len(overlaps)
                # print(f"found {found} matching beacons")

                if found >= overlap_requirement:
                    return difference, overlaps, rotation
    return None, None, None

# res = [
#     [find_scanner_coords(base_scanner, scanner, 12)[0] for scanner in scanners]
#     for base_scanner in scanners
#     ]
# pprint(res)

scanner_info = defaultdict(dict)

# res, overlaps, rotation = find_scanner_coords(scanners[1], scanners[4], 12)
# pprint(res)
# coords, overlaps, rotation = find_scanner_coords(scanners[0], scanners[1], 12)
# pprint(coords)
# pprint(overlaps)
# pprint(rotation)



# scanner_info = dict(scanner_info)
scanner_info = {0: {1: [np.array([   68, -1246,   -43]), 6]},
 1: {0: [np.array([  68, 1246,  -43]), 6],
     3: [np.array([  160, -1134,   -23]), 0],
     4: [np.array([   88,   113, -1104]), 10]},
 2: {4: [np.array([1125, -168,   72]), 11]},
 3: {1: [np.array([-160, 1134,   23]), 0]},
 4: {1: [np.array([-1104,   -88,   113]), 22],
     2: [np.array([  168, -1125,    72]), 11]}}
# pprint(scanner_info)

zero_to_one = np.array([68, -1246, -43])
one_to_three = np.array([160, -1134, -23])
one_to_four = np.array([88, 113, -1104])
two_to_four = np.array([1125, -168, 72])
four_to_two = np.array([168, -1125, 72])


four_to_zero = change_reference(one_to_four, scanner_info[0][1][0], scanner_info[0][1][1])
# print(four_to_zero)

three_to_zero = change_reference(one_to_three, scanner_info[0][1][0], scanner_info[0][1][1])
# print(three_to_zero)

two_to_one = change_reference(four_to_two, scanner_info[1][4][0], scanner_info[1][4][1])
one_to_zero = change_reference(two_to_one, scanner_info[0][1][0], scanner_info[0][1][1])
# print(one_to_zero)




beacons_in_scanner0_space = []

coords, overlaps, rotation = find_scanner_coords(scanners[0], scanners[1], 12)
for overlap in overlaps:
    if not is_in_list(overlap, beacons_in_scanner0_space):
        beacons_in_scanner0_space.append(overlap)
pprint(beacons_in_scanner0_space)
# scanner_info[0][1] = [coords, rotation]
# coords, overlaps, rotation = find_scanner_coords(scanners[1], scanners[0], 12)
# scanner_info[1][0] = [coords, rotation]

# coords, overlaps, rotation = find_scanner_coords(scanners[1], scanners[3], 12)
# scanner_info[1][3] = [coords, rotation]
# coords, overlaps, rotation = find_scanner_coords(scanners[3], scanners[1], 12)

# pprint(overlaps)
# scanner_info[3][1] = [coords, rotation]

# coords, overlaps, rotation = find_scanner_coords(scanners[1], scanners[4], 12)
# scanner_info[1][4] = [coords, rotation]
# coords, overlaps, rotation = find_scanner_coords(scanners[4], scanners[1], 12)
# scanner_info[4][1] = [coords, rotation]

# coords, overlaps, rotation = find_scanner_coords(scanners[2], scanners[4], 12)
# scanner_info[2][4] = [coords, rotation]
# coords, overlaps, rotation = find_scanner_coords(scanners[4], scanners[2], 12)
# scanner_info[4][2] = [coords, rotation]