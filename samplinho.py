import socket

def get_doppler(sat_name='ISS', freq=100e6, host='localhost', port=4533):
    try:
        with socket.create_connection((host, port), timeout=5) as sock:
            # Gpredict expects frequency in Hz (e.g. 100 MHz = 100000000 Hz)
            cmd = f'GET_DOPPLER {sat_name} {int(freq)}\n'
            sock.sendall(cmd.encode('utf-8'))

            response = sock.recv(1024).decode('utf-8').strip()
            print(f"Doppler shift at {freq/1e6:.0f} MHz for {sat_name}: {response} Hz")
            return response
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
get_doppler('ISS', 100e6)


