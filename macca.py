#!/usr/bin/python3
# All software written by Tomas. (https://github.com/ryankruge)

import socket, struct, fcntl, random, json, re, os, sys

SIOCSIFHWADDR = 0x8924
ARPHRD_ETHER = 1

HELP_DIALOGUE = """Macca - A simple, low-level solution to MAC address spoofing.
 -m | Manually specify your desired MAC address.
 -i | Manually specify your desired network interface."""

BANNER = "Software written by Tomas. Available on GitHub. (https://github.com/ryankruge)"
DEFAULT_IFACE = "wlan0"

class Spoof:
	BYTE_RANGE = [ 0, 255]
	VENDOR_PATH = "Resources/manuf.json"

	def __init__(self, mac, interface):
		self.mac = str(mac)
		self.interface = str(interface)
		self.vendors = self.PopulateVendors(self.__class__.VENDOR_PATH)

	def PopulateVendors(self, path):
		full_path = os.path.join(os.path.dirname(__file__), path)

		try:
			with open(full_path, 'r', encoding='utf8') as file:
				return json.load(file)
		except Exception as error:
			print(f"Failed to populate vendor list due to an error. {error}")
			return {}

	def ValidateMAC(self, mac) -> bool:
		pattern = r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$'
		return bool(re.match(pattern, mac))

	def GenRandOUI(self, vendors):
		return random.choice(list(vendors.keys()))

	def GenRandByte(self, byte_range):
		choice = random.randint(byte_range[0], byte_range[1])
		return f"{choice:02x}"

	def GenRandMAC(self, byte_range):
		remaining = 3
		temp = [ self.GenRandOUI(self.vendors) ]
		for iteration in range(0, remaining):
			temp.append(f"{self.GenRandByte(byte_range)}")
		return ":".join(temp).upper()

	def ChangeMAC(self, mac, interface) -> bool:
		if not self.ValidateMAC(mac):
			print(f"Invalid MAC address {mac}.")
			return False

		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		mac_bytes = bytes.fromhex(mac.replace(":", ""))

		ifreq = struct.pack(
			'16sH6s8s',
			interface.encode('utf-8'),
			ARPHRD_ETHER,
			mac_bytes,
			b'\x00' * 8
		)

		try:
			fcntl.ioctl(sock.fileno(), SIOCSIFHWADDR, ifreq)
			return True
		except Exception as error:
			print(error)
			return False
		finally:
			sock.close()

def ParseArgs(args, params):
    temp = params.copy()
    try:
        for i in range(len(args)):
            match args[i]:
            	case '-h':
            		print(HELP_DIALOGUE)
            		sys.exit()
            	case '-m':
            		temp["MAC"] = args[i + 1]
            	case '-i':
            		temp["Interface"] = args[i + 1]
    except IndexError:
        print("Invalid argument format. Use -m <MAC> -i <INTERFACE>.")
        sys.exit(1)
    return temp

if __name__ == "__main__":
	print(BANNER)

	params = { "MAC": None, "Interface": DEFAULT_IFACE }
	params = ParseArgs(sys.argv, params)

	spoof = Spoof(params["MAC"], params["Interface"])

	target_mac = params["MAC"] or spoof.GenRandMAC(spoof.BYTE_RANGE)

	result = spoof.ChangeMAC(target_mac, params["Interface"])
	if result:
		print(f"Successfully spoofed MAC address of {params['Interface']}, now {target_mac}.")
	else:
		print("MAC spoof unsuccessful. Please ensure that the device is disabled before spoofing.")