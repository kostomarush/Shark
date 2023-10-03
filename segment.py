import ipaddress


network_address = "10.0.0.1/24"


def split_network(network_address, num_segments):
    network = ipaddress.IPv4Network(network_address, strict=False)
    subnet_list = list(network.subnets(prefixlen_diff=num_segments))

    return subnet_list


num_segments = 4


segments = split_network(network_address, num_segments)


for i, segment in enumerate(segments):
    print(f"Сегмент {i+1}: {segment}")