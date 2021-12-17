from functools import reduce
import operator
from pprint import pprint

def int_from_hex_string(s):
    return bin(int('0x1'+s, 16))[3:]

def int_from_bin_string(s):
    return int("0b"+s, 2)

def string_from_int(n, base=2):
    if base == 2:
        return bin(int(n))
    else:
        return hex(int(n))

def p(n, base=2):
    print(string_from_int(n, base))

def split_string(s, pos):
    return s[0:pos], s[pos:]

def prod(iterable):
    return reduce(operator.mul, iterable, 1)

def process_packets(cur, process_one=False):
    # print(f"start: {cur}")
    values = []
    version_numbers = []
    while True:
        # print(cur)
        cur_version, cur = split_string(cur, 3)
        version_numbers.append(cur_version)
        cur_type, cur = split_string(cur, 3)
        # print(cur_version)
        # print(cur_type)
        if cur_type == "100": # literal
            literal = ""
            while True:
                first_bit, cur = split_string(cur, 1)
                # print(first_bit)
                is_last_group = first_bit == "1"
                group, cur = split_string(cur, 4)
                # print(group)
                literal += group
                if not is_last_group:
                    break
            # print(literal)
            values.append(literal)
        else: # operator
            length_type, cur = split_string(cur, 1)
            # print(length_type)
            length = 15 if length_type == "0" else 11
            subpacket_length, cur = split_string(cur, length)
            subpacket_length = int_from_bin_string(subpacket_length)
            if length_type == "0":
                # process subpackets for this length
                # print(subpacket_length)
                subpackets, cur = split_string(cur, subpacket_length)
                # print(subpackets)
                new_values, new_version_numbers, _ = process_packets(subpackets)
                version_numbers = [*version_numbers, *new_version_numbers]
            else:
                new_values = []
                for i in range(subpacket_length):
                    # process this many subpackets
                    new_values_i, new_version_numbers, cur = process_packets(cur, True)
                    new_values = [*new_values, *new_values_i]
                    version_numbers = [*version_numbers, *new_version_numbers]

            if cur_type == "000":
                value = sum([int_from_bin_string(v) for v in new_values])
            elif cur_type == "001":
                value = prod([int_from_bin_string(v) for v in new_values])
            elif cur_type == "010":
                value = min([int_from_bin_string(v) for v in new_values])
            elif cur_type == "011":
                value = max([int_from_bin_string(v) for v in new_values])
            elif cur_type == "101":
                value = int_from_bin_string(new_values[0]) > int_from_bin_string(new_values[1])
            elif cur_type == "110":
                value = int_from_bin_string(new_values[0]) < int_from_bin_string(new_values[1])
            elif cur_type == "111":
                value = int_from_bin_string(new_values[0]) == int_from_bin_string(new_values[1])
            else:
                raise Exception("unexpected type ID")
            # print(f"from {new_values} {cur_type}: {string_from_int(value)[2:]}")
            values.append(string_from_int(value)[2:])
        if process_one or cur == "" or int_from_bin_string(cur) == 0:
            break
    # print(f"returning: {values}")
    return values, version_numbers, cur

tests = [
    "D2FE28",
    "38006F45291200",
    "EE00D40C823060",
    "8A004A801A8002F478",
    "620080001611562C8802118E34",
    "C0015000016115A2E0802F182340",
    "A0016C880162017C3686B18A3D4780",
    "60552F100693298A9EF0039D24B129BA56D67282E600A4B5857002439CE580E5E5AEF67803600D2E294B2FCE8AC489BAEF37FEACB31A678548034EA0086253B183F4F6BDDE864B13CBCFBC4C10066508E3F4B4B9965300470026E92DC2960691F7F3AB32CBE834C01A9B7A933E9D241003A520DF316647002E57C1331DFCE16A249802DA009CAD2117993CD2A253B33C8BA00277180390F60E45D30062354598AA4008641A8710FCC01492FB75004850EE5210ACEF68DE2A327B12500327D848028ED0046661A209986896041802DA0098002131621842300043E3C4168B12BCB6835C00B6033F480C493003C40080029F1400B70039808AC30024C009500208064C601674804E870025003AA400BED8024900066272D7A7F56A8FB0044B272B7C0E6F2392E3460094FAA5002512957B98717004A4779DAECC7E9188AB008B93B7B86CB5E47B2B48D7CAD3328FB76B40465243C8018F49CA561C979C182723D769642200412756271FC80460A00CC0401D8211A2270803D10A1645B947B3004A4BA55801494BC330A5BB6E28CCE60BE6012CB2A4A854A13CD34880572523898C7EDE1A9FA7EED53F1F38CD418080461B00440010A845152360803F0FA38C7798413005E4FB102D004E6492649CC017F004A448A44826AB9BFAB5E0AA8053306B0CE4D324BB2149ADDA2904028600021909E0AC7F0004221FC36826200FC3C8EB10940109DED1960CCE9A1008C731CB4FD0B8BD004872BC8C3A432BC8C3A4240231CF1C78028200F41485F100001098EB1F234900505224328612AF33A97367EA00CC4585F315073004E4C2B003530004363847889E200C45985F140C010A005565FD3F06C249F9E3BC8280804B234CA3C962E1F1C64ADED77D10C3002669A0C0109FB47D9EC58BC01391873141197DCBCEA401E2CE80D0052331E95F373798F4AF9B998802D3B64C9AB6617080"
]
tests = [int_from_hex_string(test) for test in tests]

tests2 = [
    "C200B40A82",
    "04005AC33890",
    "880086C3E88112",
    "CE00C43D881120",
    "D8005AC2A8F0",
    "F600BC2D8F",
    "9C005AC2F8F0",
    "9C0141080250320F1802104A08",
]
tests2 = [int_from_hex_string(test) for test in tests2]

test = tests[7]
values, version_numbers, _ = process_packets(test)

# p1 = sum([int_from_bin_string(v) for v in version_numbers])
# print(p1)

p2 = int_from_bin_string(values[0])
print(p2)
