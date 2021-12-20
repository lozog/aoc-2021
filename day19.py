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
        if len(scanner1) - i < overlap_requirement:
            # optimization: if there are fewer than overlap_requirement left in scanner1, then there aren't enough overlaps between scanner0 and scanner1
            return None, None

        for j, beacon0 in enumerate(scanner0): # we need to pick a beacon from scanner0 that overlaps with scanner1
            # print(len(scanner0) - j)
            if len(scanner0) - j < overlap_requirement:
                # optimization: if there are fewer than overlap_requirement left in scanner0, then there aren't enough overlaps between scanner0 and scanner1
                continue

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
                    return difference, rotation
    return None, None

no_overlaps = defaultdict(list)

scanner_info = defaultdict(dict)
for i, scanner0 in enumerate(scanners):
    for j, scanner1 in enumerate(scanners):
        if i == j:
            continue
        if j in no_overlaps[i]:
            print(f"{i} has no overlaps in {j}")
            continue
        print(f"checking scanner{i} against scanner{j}")
        coords, rotation = find_scanner_coords(scanner0, scanner1, 12)
        if coords is not None:
            scanner_info[i][j] = [coords, rotation]
        else:
            no_overlaps[j].append(i)
pprint(scanner_info)


def convert_to_scanner0_space(beacon, i, scanner_info):
    # todo: this is hard-coded for the test input
    if i == 0:
        return beacon
    if i == 1:
        return change_reference(beacon, scanner_info[0][1][0], scanner_info[0][1][1])
    if i == 2:
        return convert_to_scanner0_space(
            change_reference(beacon, scanner_info[4][2][0], scanner_info[4][2][1]),
            4,
            scanner_info
        )
    if i == 3:
        return convert_to_scanner0_space(
            change_reference(beacon, scanner_info[1][3][0], scanner_info[1][3][1]),
            1,
            scanner_info
        )
    if i == 4:
        return convert_to_scanner0_space(
            change_reference(beacon, scanner_info[1][4][0], scanner_info[1][4][1]),
            1,
            scanner_info
        )



# todo: this is hard-coded for the test input
# scanner_info = defaultdict(dict)
# scanner_info = {0: {1: [np.array([   68, -1246,   -43]), 6]},
#  1: {0: [np.array([  68, 1246,  -43]), 6],
#      3: [np.array([  160, -1134,   -23]), 0],
#      4: [np.array([   88,   113, -1104]), 10]},
#  2: {4: [np.array([1125, -168,   72]), 11]},
#  3: {1: [np.array([-160, 1134,   23]), 0]},
#  4: {1: [np.array([-1104,   -88,   113]), 22],
#      2: [np.array([  168, -1125,    72]), 11]}}
# pprint(scanner_info)


# beacons_in_scanner0_space = []
# for i, scanner in enumerate(scanners):
#     for beacon in scanner:
#         beacon_in_scanner0_space = convert_to_scanner0_space(beacon, i, scanner_info)
#         # print(beacon_in_scanner0_space)
#         if not is_in_list(beacon_in_scanner0_space, beacons_in_scanner0_space):
#             beacons_in_scanner0_space.append(beacon_in_scanner0_space)
# pprint(beacons_in_scanner0_space)
