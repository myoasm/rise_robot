import socket

if __name__ == '__main__':
     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     sock.connect(('localhost',8080))
     for i in range(12):
         data = sock.recv(1024)
         print(data.decode())