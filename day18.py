from dataclasses import dataclass
from pprint import pprint
from typing import Type, Union

@dataclass
class Snail:
    l: Union[int, Type["Snail"]] = None
    r: Union[int, Type["Snail"]] = None
    parent: Type["Snail"] = None
    def __repr__(self):
        return f"[{self.l},{self.r}]"

def snail_from_list(snail_list, parent=None):
    l = snail_list[0]
    r = snail_list[1]
    
    if type(l) != int:
        l = snail_from_list(l, None)
    
    if type(r) != int:
        r = snail_from_list(r, None)

    new_snail = Snail(l=l, r=r, parent=parent)
    new_snail.l = l
    new_snail.r = r

    if type(l) != int:
        new_snail.l.parent = new_snail
    
    if type(r) != int:
        new_snail.r.parent = new_snail

    return new_snail


def add_snails(s1, s2):
    new_snail = Snail(l=s1, r=s2)
    if type(new_snail.l) != int:
        new_snail.l.parent = new_snail
    if type(new_snail.r) != int:
        new_snail.r.parent = new_snail
    return new_snail

# def reduce_snail(snail):
#     return snail

# test1 = snail_from_list([[[[[9,8],1],2],3],4])
test1 = snail_from_list([1,2])
test2 = snail_from_list([[3, 4], 5])
print(test2.l)
print(test2.l.l.parent)

# test3 = add_snails(test1, test2)
# print(test3)

# print(test3.r.l.parent)