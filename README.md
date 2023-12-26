# Vpn data transfer

The project consists of a simulation of data traffic on a VPN server.



## Table of Contents

- [Tecnical Details]()
- [Project Structure]()
- [Functionalities]()
- [IP Ranges]()



## TecnicalDetails:

The project consists of a Console application, built on a set of files developed in Python 3.10, making it easy to run in a terminal on your OS.

One of the main objectives of the project is to display the data traffic of a VPN and provide an implementation of one of the transport layer protocols: User Datagram Protocol (UDP).

For the implementation of the UDP protocol, raw sockets from the Python `socket` library were utilized.



## Project Structure

`client.py` is a simple client implementation, send to the server whatever is entered through the console.

`server.py` is a simple server implementation, display a console log of what arrives at its address.

`vpn.py` is the interactive vpn server.

`utils.py` is a file of util functions.

`logs.txt` is a txt file to store vpn traffic logs.

`users.json`, `ips.json`, `vlans.json`, `restricted_users.json` and `restricted_vlans.json` are JSON files containing dictionaries to store relevant data for the application.



## Functionalities:

To run the VPN server, execute the `vpn.py` file in your operating system's terminal

> Socket Raw use to require administrator privileges.

#### VPN Commands:

`start`: Start the VPN server and begin listening for client requests.

`stop`: Stop listening for client requests.

`create_user NAME PASSWORD ID_VLAN`: Create credentials for a new VPN user, providing a username, password, and an integer representing the VLAN ID to which they belong. Upon creating the user, the server assigns them a virtual IP number, which will be used as the user's address in requests made to servers through the VPN.

`restrict_user USERNAME IP_NETWORK`: Prevent access for a specific user to a given subnet or a specific IP address. (Example: 192.168.x.x).

`restrict_vlan ID_VLAN P_NETWORK`: Prevent users belonging to a specific VLAN from accessing a given subnet or a specific IP address.

`list_users`: List the users of the VPN.

`list_ips`: List the virtual IPs assigned to the users of the VPN.

`list_vlans`: List the VLANs ID to which the users belong.

`list_users_restrictions`: List the restrictions on users.

`List the restrictions on VLANs.`: List the restrictions on VLANs.



## IP Ranges:
VPN: `127.1.1.1`:`9999`

Servers: `127.0.0.10` to `127.0.0.255`
> Current implemented server: `127.0.0.10`:`8888`

VPN Clients virtual ip's: `127.1.1.2` to `127.255.255.255`
