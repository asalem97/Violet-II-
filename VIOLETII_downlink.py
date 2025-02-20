import socket
import os
import time
import subprocess
import time
import json
import requests
from time import sleep

filename = f"Encrypted.bin"


# Set the UDP recieve address and port
receive_host = "127.0.0.1"
receive_port = 27000

# Set the UDP server addresses and ports
UDP_HOST = "127.0.0.1" 
UDP_PORT = 27001

#DestinationCallsign = "VE9CNB" = CubeSatNB Ground Station
#DestinationCallsign = "AC8A72869C84" # Converted to proper left shifted format in HEX
DestinationCallsign = "AC8A72AA9C84"
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

        #DestinationCallsign.encode('ascii') +        #SourceCallsign.encode('ascii') +
def AX_25Send(arg):

    #Combine into a single byte string
	ME = "FFFF0000FFFFFFFF0000FFFFFFFF0000FFFFFFFF0000FFFFFFFF0000FFFFFFFF0000FFFFFFFF0000FFFFFFFF0000FFFFFFFF0000FFFFFFFF0000FFFFFFFF0000FFFFFFFF0000FFFFFFFF0000FFFFFFFF0000FFFFFFFF0000FFFFFFFF0000FFFFFFFF0000FFFFFFFF0000FFFFFFFF0000FFFFFFFF00FF00FF00FF00FF00FF00FF"
	Info = ME
	print(Info)
	print ("Payload = ", len(Info)/2, "Bytes")
	AX25Packet = (
		bytes.fromhex(DestinationCallsign) +
		#DES CALL SIGN ENCODE HERE
		bytes.fromhex(DestinationSSID) +
		bytes.fromhex(SourceCallsign) +
		#COURCE CALL SIGN ENCODE HERE
		bytes.fromhex(SourceSSID) +
		bytes.fromhex(Control) +
		bytes.fromhex(PID) +
		bytes.fromhex(Info)
	)
	print("AX.25 Packet Transmitted From SPC:")
	print(AX25Packet.hex())
	#print()
	def current_milli_time():
		return round(time.time() * 1000)
	return AX25Packet

# push over udp
#     sock.sendto(AX25Packet, (UDP_HOST, UDP_PORT))
#     sock.close()
#     return AX25Packet


#def switch_case(Command_value):
    # Extract the first 4 characters
#	prefix = Command_value[:3]
#	Command_value = Command_value[3:]
#	if prefix == 'ECH':
#		Info = Command_value.encode('ascii')
		#AX_25Send(Info)
#	elif prefix == 'TX.':
	# If command is "Tx.", send the information 25 times
#		for x in range(25):
		# TTL - sending non-junk data back
		#Info = '00000000100000000000100000000001A0070A30010800000E400C0D000708C03C02900003B00008E03C00200000000002300000000000000000000000000808C03C0910130E400C08A03C01D00002C00008C0130FF0FF00000004A0FF0FF0FF00000004F0FF0000000000000500FF0FF0FF0000000FF00C01300000600004A0FF0000000000000430FF00000000000004B0FF0FF0FF0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000C50000FF0FF00001A0070410010800010000010260150000000000000CB0000C601E0350010000000110000000000430A505A06501700B01400001000307E0010000000000000000000000000000000000000000000000000000000000000FB00605200606700C0AD00004500004D0020010000C10080BC00'
		#Info = '00000000100000000000100000000001A0070A30010800000E400C0D000708C03C02900003B00008E03C00200000000002300000000000000000000000000808C03C0910130E400C08A03C01D00002C00008C0130FF0FF00000004A0FF0FF0FF00000004F0FF0000000000000500FF0FF0FF0000000FF00C01300000600004A0FF0000000000000430FF00000000000004B0FF0FF0FF0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000C50000FF0FF0000'
#			Info = 'Az'
#			Info = b''.join([os.urandom(227)])
			#AX_25Send(Info)
#			time.sleep(20/1000)
#	else:
#		Info = b'Unknown Command'
		#AX_25Sesnd(Info)
#	return Info

        # Compute epoch timestamp in milliseconds
        # https://stackoverflow.com/questions/5998245/how-do-i-get-the-current-time-in-milliseconds-in-python


counter = 0
Packet1 = AX_25Send(0)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("AX.25 Packet Transmitted From SPC:")
while (counter < 75):
	counter+=1
	print("Downlink Packet #", counter)
	sock.sendto(Packet1, (UDP_HOST,UDP_PORT))
	sleep(1.1)
#Info = switch_case(DecryptedCommand)

sock.close()


