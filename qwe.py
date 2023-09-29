import ipaddress
import math

network = ipaddress.IPv4Network('192.168.113.0/24')
segments = [ipaddr for ipaddr in network.subnets(prefixlen_diff=4)]


num_parts = 2

# Вычисляем, сколько элементов нужно поместить в каждую часть
part_size = math.ceil(len(segments) / num_parts)

# Создаем список, в котором каждый элемент - это одна из частей
segment_parts = [segments[i:i + part_size] for i in range(0, len(segments), part_size)]
for i in segment_parts:
    for o in i:
        print(o)