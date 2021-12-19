import ast
from dataclasses import dataclass
from itertools import permutations
from math import ceil, floor
from pprint import pprint
from typing import Type
from uuid import uuid4, UUID

@dataclass
class Snail:
    _id: UUID
    val: int = None
    l: Type["Snail"] = None
    r: Type["Snail"] = None
    parent: Type["Snail"] = None

    def __repr__(self):
        if self.val is not None:
            return f"{self.val}"
        return f"[{self.l},{self.r}]"


def snail_from_list(snail_list, parent=None):
    snails = dict()
    l = None
    r = None
    l_snails = dict()
    r_snails = dict()
    
    if type(snail_list[0]) == int:
        l = Snail(uuid4(), val=snail_list[0])
        l_snails[l._id] = l
    else:
        l, l_snails = snail_from_list(snail_list[0])

    if type(snail_list[1]) == int:
        r = Snail(uuid4(), val=snail_list[1])
        r_snails[r._id] = r
    else:
        r, r_snails = snail_from_list(snail_list[1])
    
    new_snail = Snail(uuid4(), l=l, r=r)
    new_snail.l.parent = new_snail
    new_snail.r.parent = new_snail

    snails[new_snail._id] = new_snail

    return new_snail, {**snails, **r_snails, **l_snails}


def add_snails(s1, s2):
    new_snail = Snail(uuid4(), l=s1, r=s2)
    new_snail.l.parent = new_snail
    new_snail.r.parent = new_snail
    return new_snail


def find_leftmost_at_level_4(snail, level=0):
    if snail is None or snail.val is not None:
        return None
    if level == 4:
        return snail._id
    else:
        res = find_leftmost_at_level_4(snail.l, level+1)
        if res is not None:
            return res
        res = find_leftmost_at_level_4(snail.r, level+1)
        if res is not None:
            return res
    return None

def find_leftmost_gte_10(snail):
    if snail.val is not None:
        return snail._id if snail.val >= 10 else None
    else:
        res = find_leftmost_gte_10(snail.l)
        if res is None:
            return find_leftmost_gte_10(snail.r)
        return res


def leftmost_leaf(snail):
    if snail.val is not None:
        return snail._id
    else:
        return leftmost_leaf(snail.l)


def rightmost_leaf(snail):
    if snail.val is not None:
        return snail._id
    else:
        return rightmost_leaf(snail.r)


# climb tree until you don't come from the parent's R, then go down there and find the leftmost left
def right_neighbour(snail):
    # parent = snail.parent
    if snail.parent.r._id == snail._id:
        if snail.parent.parent is None:
            return None
        return right_neighbour(snail.parent)
    else:
        return leftmost_leaf(snail.parent.r)


def left_neighbour(snail):
    if snail.parent.l._id == snail._id:
        if snail.parent.parent is None:
            return None
        return left_neighbour(snail.parent)
    else:
        return rightmost_leaf(snail.parent.l)


def explode(leftmost_id, snails):
    leftmost_snail = snails[leftmost_id]
    parent = leftmost_snail.parent
    # delete leftmost
    snails.pop(leftmost_id)
    snails.pop(leftmost_snail.r._id)
    snails.pop(leftmost_snail.l._id)

    # create new snail with val=0
    new_child = Snail(uuid4(), val=0, parent=parent)
    snails[new_child._id] = new_child

    # set it as the correct child of the parent
    if parent.l._id == leftmost_id:
        parent.l = new_child
    else:
        parent.r = new_child

    # take the left value and apply it to the left neighbour, if there is one
    left_neighbour_id = left_neighbour(new_child)
    if left_neighbour_id is not None:
        left_neighbour_snail = snails[left_neighbour_id]
        left_neighbour_snail.val += leftmost_snail.l.val

    # take the right value and apply it to the right neighbour, if there is one
    right_neighbour_id = right_neighbour(new_child)
    if right_neighbour_id is not None:
        right_neighbour_snail = snails[right_neighbour_id]
        right_neighbour_snail.val += leftmost_snail.r.val

# explode(test._id, snails)

def split(root_id, snails):
    snail = snails[root_id]
    snail.l = Snail(uuid4(), val=floor(snail.val/2), parent=snail)
    snail.r = Snail(uuid4(), val=ceil(snail.val/2), parent=snail)
    snail.val = None
    snails[snail.l._id] = snail.l
    snails[snail.r._id] = snail.r

# returns True if an action was performed
def reduce_once(root_id, snails):
    snail = snails[root_id]
    leftmost_at_level_4 = find_leftmost_at_level_4(snail)
    if leftmost_at_level_4 is not None:
        explode(leftmost_at_level_4, snails)
        return True
    
    leftmost_gte_10 = find_leftmost_gte_10(snail)
    if leftmost_gte_10 is not None:
        split(leftmost_gte_10, snails)
        return True
    return False


def reduce_until_done(root_id, snails):
    while reduce_once(root_id, snails):
        pass

def magnitude(snail):
    if snail.val is not None:
        return snail.val
    else:
        return 3*magnitude(snail.l) + 2*magnitude(snail.r)


input_file = open("input/day18_full", 'r')
lines = input_file.read().splitlines()
snail_numbers_as_lists = []
for line in lines:
    snail_numbers_as_lists.append(ast.literal_eval(line))
input_file.close()

# snail_numbers_as_lists = [
#     [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],
#     [7,[[[3,7],[4,3]],[[6,3],[8,8]]]],
#     [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]],
#     [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]],
#     [7,[5,[[3,8],[1,4]]]],
#     [[2,[2,2]],[8,[8,1]]],
#     [2,9],
#     [1,[[[9,3],9],[[9,0],[0,7]]]],
#     [[[5,[7,4]],7],1],
#     [[[[4,2],2],6],[8,7]],
# ]

# p1
# snail_numbers = []
# snails = dict() # map of snail_id -> snail
# for snail_number_as_list in snail_numbers_as_lists:
#     new_snail, new_snails = snail_from_list(snail_number_as_list)
#     snail_numbers.append(new_snail)
#     snails = {**snails, **new_snails}

# root = snail_numbers[0]
# for i, next_snail in enumerate(snail_numbers):
#     if i == 0:
#         continue
#     root = add_snails(root, next_snail)
#     snails[root._id] = root
#     reduce_until_done(root._id, snails)

# res = magnitude(root)
# print(root)
# print(res)

# p2
magnitudes = []
snail_permutations = list(permutations(range(len(snail_numbers_as_lists)), 2))
for permutation in snail_permutations:
    s1_list = snail_numbers_as_lists[permutation[0]]
    s2_list = snail_numbers_as_lists[permutation[1]]
    s1, s1_snails = snail_from_list(s1_list)
    s2, s2_snails = snail_from_list(s2_list)
    snails = {**s1_snails, **s2_snails}

    root = add_snails(s1, s2)
    snails[root._id] = root
    reduce_until_done(root._id, snails)
    magnitudes.append(magnitude(root))

res = max(magnitudes)
print(res)
