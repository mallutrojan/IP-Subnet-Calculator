#!/usr/bin/env python3

import ipaddress
import textwrap

# Script Name and Credits
SCRIPT_NAME = "IP Address and Subnet Calculator"
CREDITS = "Credits: mallutrojan"

def print_header():
    """Print the header with script name and credits."""
    print(f"{'='*50}\n{SCRIPT_NAME}\n{'='*50}")
    print(f"{CREDITS}\n")
    print(f"{'='*50}")

def ip_to_binary(ip):
    """Convert an IP address to binary."""
    return '.'.join(format(int(octet), '08b') for octet in ip.split('.'))

def subnet_info(subnet):
    """Calculate network, broadcast addresses, and number of usable IPs."""
    net = ipaddress.ip_network(subnet, strict=False)
    return {
        'Network Address': str(net.network_address),
        'Broadcast Address': str(net.broadcast_address),
        'Total Number of IP Addresses': net.num_addresses,
        'Number of Usable IP Addresses': net.num_addresses - 2
    }

def cidr_to_subnet_mask(cidr):
    """Convert CIDR notation to subnet mask."""
    return str(ipaddress.IPv4Network(f'0.0.0.0/{cidr}').netmask)

def network_and_broadcast(ip, subnet_mask):
    """Calculate network and broadcast addresses from IP address and subnet mask."""
    ip_obj = ipaddress.ip_address(ip)
    net = ipaddress.ip_network(f'{ip}/{subnet_mask}', strict=False)
    return {
        'Network Address': str(net.network_address),
        'Broadcast Address': str(net.broadcast_address)
    }

def calculate_subnets(network, new_prefix):
    """Calculate subnets for a given network with a new prefix."""
    try:
        net = ipaddress.ip_network(network, strict=False)
        new_prefix = int(new_prefix)
        if new_prefix <= net.prefixlen:
            raise ValueError("New prefix must be greater than the original prefix.")

        subnets = list(net.subnets(new_prefix=new_prefix))
        return {
            'Number of Subnets': len(subnets),
            'Subnets': [{'Subnet': str(subnet), 
                         'Range': f'{subnet.network_address + 1} to {subnet.broadcast_address - 1}', 
                         'Broadcast': str(subnet.broadcast_address)} for subnet in subnets]
        }
    except ValueError as e:
        return str(e)

def block_size_and_subnets(subnet_mask):
    """Calculate block size and number of subnets created with a given subnet mask."""
    net = ipaddress.ip_network(f'0.0.0.0/{subnet_mask}', strict=False)
    block_size = net.num_addresses
    num_subnets = 2 ** (32 - int(subnet_mask))
    return {
        'Block Size': block_size,
        'Number of Subnets': num_subnets
    }

def main():
    print_header()
    while True:
        print("\nOptions:")
        print("1. Convert IP address to binary")
        print("2. Calculate subnet information")
        print("3. Convert CIDR notation to subnet mask")
        print("4. Calculate network and broadcast addresses")
        print("5. Calculate subnets from a larger network")
        print("6. Calculate block size and number of subnets for a given subnet mask")
        print("7. Exit")

        choice = input("Choose an option (1-7): ")

        if choice == '1':
            ip = input("Enter IP address (e.g., 192.168.1.1): ")
            try:
                binary_ip = ip_to_binary(ip)
                print(f"Binary representation of {ip} is {binary_ip}")
            except ValueError:
                print("Invalid IP address format. Please enter a valid IP address.")

        elif choice == '2':
            subnet = input("Enter subnet (e.g., 192.168.1.0/24): ")
            try:
                info = subnet_info(subnet)
                print(f"Network Address: {info['Network Address']}")
                print(f"Broadcast Address: {info['Broadcast Address']}")
                print(f"Total Number of IP Addresses: {info['Total Number of IP Addresses']}")
                print(f"Number of Usable IP Addresses: {info['Number of Usable IP Addresses']}")
            except ValueError:
                print("Invalid subnet format. Please enter a valid subnet.")

        elif choice == '3':
            cidr = input("Enter CIDR notation (e.g., 24): ")
            try:
                subnet_mask = cidr_to_subnet_mask(cidr)
                print(f"Subnet mask for /{cidr} is {subnet_mask}")
            except ValueError:
                print("Invalid CIDR notation. Please enter a valid number.")

        elif choice == '4':
            ip = input("Enter IP address (e.g., 192.168.1.10): ")
            subnet_mask = input("Enter subnet mask (e.g., 255.255.255.0): ")
            try:
                addresses = network_and_broadcast(ip, subnet_mask)
                print(f"Network Address: {addresses['Network Address']}")
                print(f"Broadcast Address: {addresses['Broadcast Address']}")
            except ValueError:
                print("Invalid IP address or subnet mask format. Please enter valid values.")

        elif choice == '5':
            network = input("Enter the network (e.g., 172.16.0.0/16): ")
            new_prefix = input("Enter new prefix (e.g., 20): ")
            result = calculate_subnets(network, new_prefix)
            if isinstance(result, dict):
                print(f"Number of Subnets: {result['Number of Subnets']}")
                for idx, subnet in enumerate(result['Subnets'], start=1):
                    print(f"Subnet {idx}: {subnet['Subnet']}, Range: {subnet['Range']}, Broadcast: {subnet['Broadcast']}")
            else:
                print(result)  # Print error message if any

        elif choice == '6':
            subnet_mask = input("Enter subnet mask (e.g., 29): ")
            try:
                result = block_size_and_subnets(subnet_mask)
                print(f"Block Size: {result['Block Size']} IP addresses")
                print(f"Number of Subnets: {result['Number of Subnets']}")
            except ValueError:
                print("Invalid subnet mask format. Please enter a valid value.")

        elif choice == '7':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please select 1, 2, 3, 4, 5, 6, or 7.")

if __name__ == "__main__":
    main()
