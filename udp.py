import socket
import struct

# Offset constants
VERSION_OFF     = 0
IHL_OFF         = VERSION_OFF
DSCP_OFF        = IHL_OFF + 1
ECN_OFF         = DSCP_OFF
LENGTH_OFF      = DSCP_OFF + 1
ID_OFF          = LENGTH_OFF + 2
FLAGS_OFF       = ID_OFF + 2
OFF_OFF         = FLAGS_OFF
TTL_OFF         = OFF_OFF + 2
PROTOCOL_OFF    = TTL_OFF + 1
IP_CHECKSUM_OFF = PROTOCOL_OFF + 1
SRC_IP_OFF      = IP_CHECKSUM_OFF + 2
DEST_IP_OFF     = SRC_IP_OFF + 4
SRC_PORT_OFF    = DEST_IP_OFF + 4
DEST_PORT_OFF   = SRC_PORT_OFF + 2
UDP_LEN_OFF     = DEST_PORT_OFF + 2
UDP_CHECKSUM_OFF= UDP_LEN_OFF + 2
DATA_OFF        = UDP_CHECKSUM_OFF + 2




def send(data, dest_addr, src_addr=('127.0.0.1', 35869)):
    # Get ip's
    src_ip, dest_ip = src_addr[0], dest_addr[0]

    # Check if any is a localhost
    src_ip, dest_ip = check_localhost(src_ip), check_localhost(dest_ip)

    # Convert ip's to binary
    src_ip, dest_ip = parse_ip(src_ip), parse_ip(dest_ip)

    # Pack ips's
    src_ip, dest_ip = struct.pack('!4B', *src_ip), struct.pack('!4B', *dest_ip)

    reserved = 0

    # 17
    protocol = socket.IPPROTO_UDP 

    # Try to encode data
    try:
        data = data.encode()
    except ValueError:
        pass

    # Get ports
    src_port = src_addr[1]
    dest_port = dest_addr[1]

    # length en bytes
    data_len = len(data)
    
    header_length = 8
    udp_length = header_length + data_len

    checksum = 0

    # Build pseudo header
    pseudo_header = struct.pack('!BBH', reserved, protocol, udp_length)
    pseudo_header = src_ip + dest_ip + pseudo_header
    # Build header
    udp_header = struct.pack('!4H', src_port, dest_port, udp_length, checksum)
    checksum = calculate_checksum(pseudo_header + udp_header + data)
    udp_header = struct.pack('!4H', src_port, dest_port, udp_length, checksum)

    # Send packet
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP) as s:
        s.sendto(udp_header + data, dest_addr)

def calculate_checksum(data):
    checksum = 0
    data_len = len(data)

    if (data_len % 2):
        data_len += 1
        data += struct.pack('!B', 0)
    
    for i in range(0, data_len, 2):
        pair = (data[i] << 8) + (data[i + 1])
        checksum += pair

    checksum = (checksum >> 16) + (checksum & 0xFFFF)
    checksum = ~checksum & 0xFFFF
    return checksum

def check_localhost(addr):
    return '127.0.0.1' if addr == 'localhost' else addr

def parse_ip(ip_addr):
    return [int(byte) for byte in ip_addr.split('.')]






def recive(raw_socket, buffer_size):
    reserved = 0
    protocol = socket.IPPROTO_UDP 

    data, _ = raw_socket.recvfrom(buffer_size)

    packet = parse_data(data)
    
    ip_addr = struct.pack('!8B', *[data[x] for x in range(SRC_IP_OFF, SRC_IP_OFF + 8)])
    udp_psuedo = struct.pack('!BB5H', reserved, protocol, packet['udp_length'], packet['src_port'], packet['dest_port'], packet['udp_length'], 0)
    
    verify = verify_checksum(ip_addr + udp_psuedo + packet['data'].encode(), packet['UDP_checksum'])

    if verify == 0xFFFF:
        return (packet['src_ip'], packet['src_port']), packet['data'], True
    else:
        return (packet['src_ip'], packet['src_port']), 'Discard packet(checksum error)', False

def verify_checksum(data, checksum):
    data_len = len(data)
    if (data_len % 2) == 1:
        data_len += 1
        data += struct.pack('!B', 0)
    
    for i in range(0, data_len, 2):
        pair = (data[i] << 8) + (data[i + 1])
        checksum += pair
        checksum = (checksum >> 16) + (checksum & 0xFFFF)

    return checksum

def parse_data(data):
    udp_length = (data[UDP_LEN_OFF] << 8) + data[UDP_LEN_OFF + 1]
    packet = {
        'Checksum'     : (data[IP_CHECKSUM_OFF] << 8) + data[IP_CHECKSUM_OFF + 1],
        'src_ip'       : '.'.join(map(str, [data[x] for x in range(SRC_IP_OFF, SRC_IP_OFF + 4)])),
        'dest_ip'      : '.'.join(map(str, [data[x] for x in range(DEST_IP_OFF, DEST_IP_OFF + 4)])),
        'src_port'     : (data[SRC_PORT_OFF] << 8) + data[SRC_PORT_OFF + 1],
        'dest_port'    : (data[DEST_PORT_OFF] << 8) + data[DEST_PORT_OFF + 1],
        'udp_length'   : udp_length,
        'UDP_checksum' : (data[UDP_CHECKSUM_OFF] << 8) + data[UDP_CHECKSUM_OFF + 1],
        'data'         : ''.join(map(chr, [data[DATA_OFF + x] for x in range(0, udp_length - 8)]))
    }

    return packet