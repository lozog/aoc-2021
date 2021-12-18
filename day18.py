from dataclasses import dataclass
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


# test1 = snail_from_list([[[[[9,8],1],2],3],4])
# test1 = snail_from_list([[[[4,3],4],4],[7,[[8,4],9]]])
# test2 = snail_from_list([1,1])
# test3 = add_snails(test1, test2)
test3, snails = snail_from_list([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]])
test3, snails = snail_from_list([7,[6,[5,[4,[3,2]]]]])
print(test3)
leftmost_id = find_leftmost_at_level_4(test3)
leftmost_snail = snails[leftmost_id]
