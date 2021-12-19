from dataclasses import dataclass
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


def magnitude(snail):
    if snail.val is not None:
        return snail.val
    else:
        return 3*magnitude(snail.l) + 2*magnitude(snail.r)


# test_input = [
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

test_input = [
    [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]],
    [[[5,[2,8]],4],[5,[[9,9],0]]],
    [6,[[[6,2],[5,6]],[[7,6],[4,7]]]],
    [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]],
    [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]],
    [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]],
    [[[[5,4],[7,7]],8],[[8,3],8]],
    [[9,3],[[9,9],[6,[4,9]]]],
    [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]],
    [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
]

test_snails = []
snails = dict()
for snail_input in test_input:
    new_snail, new_snails = snail_from_list(snail_input)
    test_snails.append(new_snail)
    snails = {**snails, **new_snails}

root = test_snails[0]
for i, next_snail in enumerate(test_snails):
    if i == 0:
        continue
    root = add_snails(root, next_snail)
    snails[root._id] = root
    while True:
        # print(root)
        res = reduce_once(root._id, snails)
        if not res:
            break

res = magnitude(root)
print(root)
print(res)
