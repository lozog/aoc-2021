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


# test1 = snail_from_list([[[[4,3],4],4],[7,[[8,4],9]]])
# test2 = snail_from_list([1,1])
# test3 = add_snails(test1, test2)
# test, snails = snail_from_list([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]])
# test, snails = snail_from_list([7,[6,[5,[4,[3,2]]]]])
# test, snails = snail_from_list([[6,[5,[4,[3,2]]]],1])
# test, snails = snail_from_list([[[[[9,8],1],2],3],4])
test, snails = snail_from_list([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]])
print(test)

def explode(snail_id, snails):
    snail = snails[snail_id]
    leftmost_id = find_leftmost_at_level_4(snail)
    leftmost_snail = snails[leftmost_id]
    parent = leftmost_snail.parent

    # remove leftmost
    snails.pop(leftmost_id)
    snails.pop(leftmost_snail.r._id)
    snails.pop(leftmost_snail.l._id)
    new_child = Snail(uuid4(), val=0, parent=parent)
    snails[new_child._id] = new_child
    if parent.l._id == leftmost_id:
        parent.l = new_child
    else:
        parent.r = new_child

    left_neighbour_id = left_neighbour(new_child)
    if left_neighbour_id is not None:
        left_neighbour_snail = snails[left_neighbour_id]
        left_neighbour_snail.val += leftmost_snail.l.val

    right_neighbour_id = right_neighbour(new_child)
    if right_neighbour_id is not None:
        right_neighbour_snail = snails[right_neighbour_id]
        right_neighbour_snail.val += leftmost_snail.r.val

# explode(test._id, snails)

def split(snail_id, snails):
    snail = snails[snail_id]
    snail.l = Snail(uuid4(), val=floor(snail.val/2), parent=snail)
    snail.r = Snail(uuid4(), val=ceil(snail.val/2), parent=snail)
    snail.val = None
    snails[snail.l._id] = snail.l
    snails[snail.r._id] = snail.r

print(test)
pprint(snails)