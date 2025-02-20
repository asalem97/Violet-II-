import socket
import os
import time
import subprocess
import time
import json
import requests

filename = f"Encrypted.bin"


# Set the UDP recieve address and port
receive_host = "127.0.0.1"
receive_port = 27000

# Set the UDP server addresses and ports
UDP_HOST = "127.0.0.1" 
UDP_PORT = 27001

#DestinationCallsign = "VE9CNB" = CubeSatNB Ground Station
DestinationCallsign = "AC8A72869C84" # Converted to proper left shifted format in HEX

DestinationSSID = "E2" # Bit 7 set to 0 indicating source SSID **

# 7 bytes allocated for each callsign, byte 7 for SSID in Hex
#SourceCallsign = "VE9VLT" = VIOLET
SourceCallsign = "AC8A72AC98A8" # Converted to proper left shifted format in HEX

SourceSSID = "63" # Bit 7 set to 1 indicating destination SSID **

# Control byte
Control = "03"

# FCS
FCS = "0000"

# PID Byte
PID = "F0"


#subprocess.Popen(['python3','ettus_bpsk_loopback.py'])


def AX_25Send(Info):

    # Combine into a single byte string
   
	#AX25Packet = (
	#bytes.fromhex(DestinationCallsign) +
        #DestinationCallsign.encode('ascii') +
        #bytes.fromhex(DestinationSSID) +
        #bytes.fromhex(SourceCallsign) +
        #SourceCallsign.encode('ascii') +
	#bytes.fromhex(SourceSSID) +
	#bytes.fromhex(Control) +
	#bytes.fromhex(PID) +
	#bytes.fromhex(Info)
	#Info
        #)

	#print("AX.25 Packet Transmitted From SPC:")
	#print(AX25Packet.hex())
	#print()

	# push over udp
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.sendto(AX25Packet, (UDP_HOST, UDP_PORT))
	sock.close()
	return AX25Packet


def switch_case(Command_value):
    # Extract the first 4 characters
	prefix = Command_value[:3]
	Command_value = Command_value[3:]
	if prefix == 'ECH':
		Info = Command_value.encode('ascii')
		AX_25Send(Info)
	elif prefix == 'TX.':
	# If command is "Tx.", send the information 25 times
		for x in range(25):
			# TTL - sending non-junk data back
			#Info = '00000000100000000000100000000001A0070A30010800000E400C0D000708C03C02900003B00008E03C00200000000002300000000000000000000000000808C03C0910130E400C08A03C01D00002C00008C0130FF0FF00000004A0FF0FF0FF00000004F0FF0000000000000500FF0FF0FF0000000FF00C01300000600004A0FF0000000000000430FF00000000000004B0FF0FF0FF0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000C50000FF0FF00001A0070410010800010000010260150000000000000CB0000C601E0350010000000110000000000430A505A06501700B01400001000307E0010000000000000000000000000000000000000000000000000000000000000FB00605200606700C0AD00004500004D0020010000C10080BC00'
			Info = '00000000100000000000100000000001A0070A30010800000E400C0D000708C03C02900003B00008E03C00200000000002300000000000000000000000000808C03C0910130E400C08A03C01D00002C00008C0130FF0FF00000004A0FF0FF0FF00000004F0FF0000000000000500FF0FF0FF0000000FF00C01300000600004A0FF0000000000000430FF00000000000004B0FF0FF0FF0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000C50000FF0FF0000'

			#Info = b''.join([os.urandom(227)])
			#AX_25Send(Info)
			time.sleep(20/1000)
	else:
		Info = b'Unknown Command'
		AX_25Send(Info)
	return Info

        # Compute epoch timestamp in milliseconds
        # https://stackoverflow.com/questions/5998245/how-do-i-get-the-current-time-in-milliseconds-in-python
def current_milli_time():
	return round(time.time() * 1000)


while 1:
	#AX_25Send(Info)
	# Receive and print response as byte string over UDP
	print("\n")
	print("Waiting to receive packet...")
	print("\n")
	receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	receive_socket.bind((receive_host, receive_port))
	data, addr = receive_socket.recvfrom(1024)
	print("\n")
	print("Received Packet with AX.25 Frame: ",data.hex())
	print("\n")	
	command = 'http://131.202.21.3:12345/api/record/downlink'

	headers = {
		'Content-Type': 'application/json',
		'Authorization': 'Bearer 2c0ef2f0-5631-459b-8d81-ea4cd7a3df8e/d15b4d9a9383991a0bac1275361e05cf'
	}

	current_time = current_milli_time()

	data2 = {
		'timestamp':current_time,       # uplink timestamp as the numbe>
		'ax25_hex':data.hex()           # AX.25 frame, as a hexad>
	}

        #json_str = json.dumps(data2, indent=True)
        #print ("json_str=",json_str)

	#response = requests.post(command, json = data2, headers = headers)

	#EncryptedPacket = data[116:]
	EncryptedPacket = data[16:]
	filename = f"Encrypted.bin"
	directory = "violet-decrypt-uplink/build"
	full_path = os.path.join(directory,filename)
	with open(full_path, mode='wb') as file: 
		file.write(EncryptedPacket)
		file.close()
	p1 = subprocess.Popen(['python3', 'decrypt.py']) 
	p1.wait()
	filename = f"Decrypted.txt"
	full_path = os.path.join(directory,filename)
	with open(full_path, mode='r') as file:
		DecryptedCommand = file.read()
		file.close()
	response = data[16:].hex()
	print("\n")
	print(f"Encrypted Packet: ",EncryptedPacket.hex())
	print("\n")
	print("Decrypted Command:",DecryptedCommand)

	# Delete temp files
	#
	p1 = subprocess.Popen(['rm', 'violet-decrypt-uplink/build/Encrypted.bin']) 
	p1.wait()
	p1 = subprocess.Popen(['rm', 'violet-decrypt-uplink/build/Decrypted.txt']) 
	p1.wait()


	Info = switch_case(DecryptedCommand)



