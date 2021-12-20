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


scanner4_in_scanner0_space = [
    np.array([459,-707,401]),
    np.array([-739,-1745,668]),
    np.array([-485,-357,347]),
    np.array([432,-2009,850]),
    np.array([528,-643,409]),
    np.array([423,-701,434]),
    np.array([-345,-311,381]),
    np.array([408,-1815,803]),
    np.array([534,-1912,768]),
    np.array([-687,-1600,576]),
    np.array([-447,-329,318]),
    np.array([-635,-1737,486]),
]


def find_scanner_coords(scanner0, scanner1, overlap_requirement):
    """
    Given two lists of beacon coordinates from two scanners, returns the coordinates of
    scanner1 relative to scanner0 if it can, or None if there are not enough overlapping beacons.
    """
    for i, beacon in enumerate(scanner1):
        # if we know which beacons to match up, then we can find the coordinates of the scanner
        # so, we'll find which beacon in scanner1 is beacon0 of scanner0

        for beacon0 in scanner0:
            for rotation, beacon_rotated in enumerate(all_rotations(beacon)):
                # beacon0 = scanner0[0] # they MUST share this beacon
                # beacon0 = scanner0[-1]
                difference = beacon0 - beacon_rotated

                scanner1_in_scanner0_space = [
                    all_rotations(scanner1_beacon)[rotation] + difference
                    for scanner1_beacon in scanner1
                ]

                overlaps = [
                    scanner1_beacon
                    for scanner1_beacon in scanner1_in_scanner0_space
                    if is_in_list(scanner1_beacon, scanner0)
                ]

                # if i == 3 and rotation == 10:
                #     print(f"{difference} = {beacon0} - {beacon_rotated}")
                #     print(f"{change_reference(difference, np.array([68,-1246,-43]), 6)} = {beacon0} - {beacon_rotated} { rotation }")
                #     for overlap in overlaps:
                #         print(change_reference(overlap, np.array([68,-1246,-43]), 6))

                # scanner0_in_scanner1_space = [
                #     all_rotations(scanner0_beacon - difference)[rotation]
                #     for scanner0_beacon in scanner0
                # ]

                # overlaps2 = [
                #     scanner0_beacon
                #     for scanner0_beacon in scanner0_in_scanner1_space
                #     if is_in_list(scanner0_beacon, scanner1)
                # ]

                found = len(overlaps)
                # found2 = len(overlaps2)
                # if found2 > 3:
                #     print(f"{difference}, {rotation}: found {found}")
                #     pprint(overlaps2)
                # if (rotation == 18):
                # if (rotation == 6):
                #     print(f"{difference}, {rotation}: found {found}")

                # print(f"found {found} matching beacons")

                if found >= overlap_requirement:
                    return difference
                    # return change_reference(difference, np.array([68,-1246,-43]), 6)
    return None

# res = [
#     [find_scanner_coords(base_scanner, scanner, 12) for scanner in scanners]
#     for base_scanner in scanners
#     ]
res = find_scanner_coords(scanners[1], scanners[4], 12)
pprint(res)
res = find_scanner_coords(scanners[0], scanners[1], 12)
pprint(res)

# scanner4_in_0 = np.array([-20,-1133,1061])

# 0 > 1 > 4
# 459,-707,401 > -391,539,-444 > -660, -479, -426