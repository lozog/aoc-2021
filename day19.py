from collections import defaultdict
import numpy as np
from pprint import pprint
import re
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path


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


input_file = open('input/day19_full', 'r')
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


# uncomment and run the following code to find the coordinates of beacons that overlap (i.e. to get scanner_info)
# no_overlaps = defaultdict(list)
# scanner_info = defaultdict(dict)
# for i, scanner0 in enumerate(scanners):
#     for j, scanner1 in enumerate(scanners):
#         if i == j:
#             continue
#         if j in no_overlaps[i]:
#             print(f"{i} has no overlaps in {j}")
#             continue
#         print(f"checking scanner{i} against scanner{j}")
#         coords, rotation = find_scanner_coords(scanner0, scanner1, 12)
#         if coords is not None:
#             print(f"found {coords}")
#             scanner_info[i][j] = [coords, rotation]
#         else:
#             no_overlaps[j].append(i)
# pprint(scanner_info)


# result from running the above. it took like 2h so i saved the result
scanner_info = {0: {8: [np.array([1097, -115, -112]), 1],
                 11: [np.array([  -33,   -61, -1239]), 11],
                 17: [np.array([ -55, 1187,  -97]), 21]},
             1: {7: [np.array([  160,   124, -1332]), 19],
                 21: [np.array([-1062,    40,   -52]), 9],
                 23: [np.array([  68,   36, 1090]), 23]},
             2: {8: [np.array([1085,   77,  167]), 9],
                 11: [np.array([ -42, 1207,  113]), 23],
                 13: [np.array([   33,    95, -1160]), 16],
                 23: [np.array([ -26,   43, 1328]), 17]},
             3: {15: [np.array([-107, 1244,  -34]), 1]},
             4: {16: [np.array([ -39,   81, 1302]), 18],
                 26: [np.array([  -63, -1084,    72]), 14],
                 31: [np.array([  -90,    62, -1218]), 0],
                 32: [np.array([-1272,    54,    46]), 6]},
             5: {7: [np.array([-1219,    17,   -76]), 10],
                 29: [np.array([ -139,   129, -1164]), 14]},
             6: {16: [np.array([ 120,   79, 1114]), 5],
                 23: [np.array([  41, 1222,  -38]), 4]},
             7: {1: [np.array([-1332,  -124,  -160]), 21],
                 5: [np.array([ -76, 1219,   17]), 22]},
             8: {0: [np.array([-1097,   112,  -115]), 3],
                 2: [np.array([   77, -1085,  -167]), 13],
                 12: [np.array([ -23,  157, 1160]), 4],
                 18: [np.array([  -27,    50, -1208]), 18],
                 24: [np.array([1298,   14,   -9]), 10]},
             9: {18: [np.array([-1241,   -92,   -15]), 9],
                 27: [np.array([   83,  -135, -1128]), 21]},
             10: {31: [np.array([-1157,   -78,    -1]), 4],
                  32: [np.array([  25,  -70, 1263]), 2]},
             11: {0: [np.array([   61,    33, -1239]), 11],
                  2: [np.array([ 113, 1207,  -42]), 23]},
             12: {8: [np.array([  -23,   157, -1160]), 4],
                  16: [np.array([-1200,   116,   -78]), 17],
                  21: [np.array([ -53,  138, 1143]), 6],
                  23: [np.array([ -57, 1268,    1]), 12]},
             13: {2: [np.array([ -95, 1160,  -33]), 8],
                  18: [np.array([   9,  119, 1102]), 23]},
             14: {22: [np.array([-1302,     0,    -8]), 6],
                  25: [np.array([  20,    1, 1129]), 9],
                  32: [np.array([  -22,    67, -1281]), 12]},
             15: {3: [np.array([ 107,   34, 1244]), 3],
                  31: [np.array([  -42,    51, -1199]), 17]},
             16: {4: [np.array([  81, 1302,   39]), 12],
                  6: [np.array([  120, -1114,   -79]), 5],
                  12: [np.array([  78,  116, 1200]), 17],
                  24: [np.array([-1091,   -27,  -121]), 7]},
             17: {0: [np.array([   97, -1187,   -55]), 19],
                  18: [np.array([   35,   -94, -1125]), 6],
                  27: [np.array([  -8, 1230,  -12]), 10]},
             18: {8: [np.array([   50, -1208,    27]), 12],
                  9: [np.array([ -92, 1241,   15]), 13],
                  13: [np.array([1102,  119,    9]), 23],
                  17: [np.array([   35,    94, -1125]), 6]},
             19: {29: [np.array([-1253,    48,   131]), 19]},
             20: {33: [np.array([-104, 1236,  -69]), 17]},
             21: {1: [np.array([  40, 1062,   52]), 13],
                  12: [np.array([ -53, -138, 1143]), 6],
                  34: [np.array([-1234,  -130,   -29]), 11]},
             22: {14: [np.array([-1302,     0,    -8]), 6],
                  33: [np.array([1072,  110,   71]), 10]},
             23: {1: [np.array([1090,   36,   68]), 23],
                  2: [np.array([-1328,    43,    26]), 17],
                  6: [np.array([  41, 1222,   38]), 4],
                  12: [np.array([  -1,  -57, 1268]), 18]},
             24: {8: [np.array([   -9, -1298,    14]), 22],
                  16: [np.array([-1091,  -121,   -27]), 7]},
             25: {14: [np.array([    1,   -20, -1129]), 13],
                  30: [np.array([1135,   51,    3]), 5]},
             26: {4: [np.array([  72,  -63, 1084]), 20],
                  28: [np.array([  -62,    86, -1264]), 16]},
             27: {9: [np.array([1128,  135,   83]), 19],
                  17: [np.array([ -12,    8, 1230]), 22]},
             28: {26: [np.array([ -86, 1264,   62]), 8]},
             29: {5: [np.array([-1164,  -139,  -129]), 20],
                  19: [np.array([ 131,  -48, 1253]), 21]},
             30: {25: [np.array([1135,   -3,  -51]), 5]},
             31: {4: [np.array([  90,  -62, 1218]), 0],
                  10: [np.array([-1157,   -78,     1]), 4],
                  15: [np.array([1199,   51,   42]), 17]},
             32: {4: [np.array([-1272,   -54,    46]), 6],
                  10: [np.array([ -25,  -70, 1263]), 2],
                  14: [np.array([1281,  -22,   67]), 18]},
             33: {20: [np.array([  69, 1236,  104]), 17],
                  22: [np.array([   71, -1072,   110]), 22]},
             34: {21: [np.array([ 130, 1234,  -29]), 11]}}


# we need to find out how to convert from any scanner to scanner 0
path_matrix = np.array([
    np.array([1 if i in scanner_info[start].keys() else 0 for i in range(len(scanners))])
    for start in scanner_info.keys()
])
path_graph = csr_matrix(path_matrix)
D, Pr = shortest_path(path_graph, directed=False, return_predecessors=True)
# stolen from https://stackoverflow.com/questions/53074947/examples-for-search-graph-using-scipy/53078901
def get_path(Pr, i, j):
    path = [j]
    k = j
    while Pr[i, k] != -9999:
        path.append(Pr[i, k])
        k = Pr[i, k]
    return path[::-1]


def convert_to_scanner0_space(beacon, path, scanner_info):
    if (len(path) == 1):
        return beacon

    src_scanner = path[0]
    dst_scanner = path[1]

    return convert_to_scanner0_space(
        change_reference(
            beacon,
            scanner_info[dst_scanner][src_scanner][0],
            scanner_info[dst_scanner][src_scanner][1]
        ),
        path[1:],
        scanner_info
    )


beacons_in_scanner0_space = []
for i, scanner in enumerate(scanners):
    path = get_path(Pr, i, 0)
    for beacon in scanner:
        beacon_in_scanner0_space = convert_to_scanner0_space(beacon, path, scanner_info)
        if not is_in_list(beacon_in_scanner0_space, beacons_in_scanner0_space):
            beacons_in_scanner0_space.append(beacon_in_scanner0_space)

# pprint(beacons_in_scanner0_space)
print(len(beacons_in_scanner0_space))
