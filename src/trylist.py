# import  numpy
#
# realist = [[] for i in range(9)]
# for j in range(9):
#     for i in range(9):
#         realist[j].append((i * 3.1, round(24.8 - j * 3.1,1)))
# print(realist)
#
# f = open('C:\\Users\\myosam\\Desktop\\zuobiao\\mode.txt', 'w')
# f = f.write('2')

from socket import *


class Socekt_connect():
    def __init__(self):   #socket的连接创建
        self.HOST = ''
        self.PORT = 3000
        self.BUFSIZ = 1024
        self.addr = (self.HOST, self.PORT)
        self.Sockt = socket(AF_INET, SOCK_STREAM)


    def start_wait(self):
        self.Sockt.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.Sockt.bind(self.addr)
        self.Sockt.listen(5)
        self.Conn, clien_addr = self.Sockt.accept()
        # self.Conn.sendall('okay'.encode())
        # self.Conn.sendall('1'.encode())

    def sent_mode(self):
        self.Conn.sendall(str(1,1,1).encode())
    def sent_posision(self):
        pass
    def sent_chess_result(self):
        pass



if __name__ == '__main__':
    socket = Socekt_connect()
    socket.start_wait()
    for i in range(10):
        string = input('请输入：')
        #
        socket.Conn.sendall((str(len(string)).zfill(4) +'4').encode())
        #socket.Conn.sendall('00054'.encode())
        socket.Conn.sendall(string.encode())