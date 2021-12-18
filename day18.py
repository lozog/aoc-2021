from dataclasses import dataclass
from pprint import pprint
from typing import Type, Union

@dataclass
class Snail:
    val: int = None
    l: Type["Snail"] = None
    r: Type["Snail"] = None
    parent: Type["Snail"] = None
    def __repr__(self):
        if self.val is not None:
            return f"{self.val}"
        return f"[{self.l},{self.r}]"


def snail_from_list(snail_list, parent=None):
    l = None
    r = None
    
    if type(snail_list[0]) == int:
        l = Snail(val=snail_list[0])
    else:
        l = snail_from_list(snail_list[0])

    if type(snail_list[1]) == int:
        r = Snail(val=snail_list[1])
    else:
        r = snail_from_list(snail_list[1])
    
    new_snail = Snail(l=l, r=r)
    new_snail.l.parent = new_snail
    new_snail.r.parent = new_snail

    return new_snail


def add_snails(s1, s2):
    new_snail = Snail(l=s1, r=s2)
    new_snail.l.parent = new_snail
    new_snail.r.parent = new_snail
    return new_snail

# def reduce_snail(snail):
#     return snail

# test1 = snail_from_list([[[[[9,8],1],2],3],4])
test1 = snail_from_list([[[[4,3],4],4],[7,[[8,4],9]]])
test2 = snail_from_list([1,1])


test3 = add_snails(test1, test2)
print(test3)
