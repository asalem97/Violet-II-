import ctypes
import os
import subprocess

directory = "violet-decrypt-uplink/build"
filename = f"Encrypted.bin"

full_path = os.path.join(directory,filename)

with open(full_path, mode='rb') as file: 
    fileContent = file.read()

session = str(int.from_bytes(fileContent[:4],'big'))
frame = str(int.from_bytes(fileContent[4:8],'big'))
cipher = fileContent[8:136].hex()
auth = fileContent[136:].hex()

#print(fileContent)
print("Session ID: ",session)
print("Frame IV: ",frame)
print("Ciphertext: ",cipher)
print("Authentication tag: ",auth)

command = "./violet-decrypt-uplink/build/violet-encrypt-uplink" #executable file name
key = "violet-decrypt-uplink/build/key.hex" #primary key file name
storage = "violet-decrypt-uplink/build/storage" # storage file name
output = "violet-decrypt-uplink/build/Decrypted.bin" # Encrypted file name
fformat = "binary"

subprocess.run([command, "--primary-key-file",key,"--persistent-storage-file",storage, "--session-id",session , "--frame-iv",frame,"--ciphertext",cipher, "--ciphertext-size", "128","--auth-tag",auth, "--output-format",fformat,"--output-file", output ])

with open("violet-decrypt-uplink/build/Decrypted.bin", mode= 'rb') as file:
    message = file.read()

plaintext = message.decode('utf-8')
unwanted_characters = "#"  # List of unwanted characters
for char in unwanted_characters:
    plaintext = plaintext.replace(char, "")

with open('violet-decrypt-uplink/build/Decrypted.txt', mode='w') as file:
    file.write(plaintext)
    file.close()
#print("This is the decrypted plaintext: ",plaintext)
