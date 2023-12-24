from datetime import datetime
import json

def invalidate_args(args, args_count):
    if args != args_count:
        print(f"Given {args} arguments, but expected {args_count}")
        return True
    else:
        return False

def format_dict(dictionary):
    formatted_str = "\n"
    for key, value in dictionary.items():
        formatted_str += f"{key}: {value}\n"
    return formatted_str

def is_subnet(x: str, ip: str):
    x_bytes = x.split(".")
    ip_bytes = ip.split(".")

    for i in range(4):
        if ip_bytes[i] != "x":
            if ip_bytes[i] == x_bytes[i]:
                continue
            else: 
                return False
        else:
            return True
   
    return True

def write_log(log):
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open('logs.txt', 'a') as file:
        file.write(date_time + ': ' + log + '\n')


def validate_input_ip(ip: str):
    ip_arr = ip.split(".")

    if len(ip_arr) != 4:
        print("Invalid ip")
        return False
    
    valid_bytes = are_bytes_valid(ip_arr)
    if not valid_bytes:
        print("Invalid ip")
        return False
    
    return True
    

def are_bytes_valid(bytes):
    found = False
    for s in bytes:
        try:
            value = int(s)

            if found:
                return False

            if not 0 <= value <= 255:
                return False
        except ValueError:
            found = True
            if not s == 'x':
                return False
    return True
