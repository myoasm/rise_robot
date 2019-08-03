from five_chess import Recognize
from online_rec import  Online_rec
import pyrealsense2 as rs
import numpy as np
import cv2 as cv
from gobang import  GUI
from target_recognition import  TargetRecognition
import socket


def get_pipeline():
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
    pipeline.start(config)
    return pipeline



class Socekt_connect():
    def __init__(self):   #socket的连接创建
        self.HOST = ''
        self.PORT = 3000
        self.BUFSIZ = 1024
        self.addr = (self.HOST, self.PORT)
        #self.client_addr = ''
        self.Sockt = socket(AF_INET, SOCK_STREAM)


    def start_wait(self):
        self.Sockt.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.Sockt.bind(self.addr)
        self.Sockt.listen(5)
        self.Conn, clien_addr = self.Sockt.accept()
       
    def sent_start(self, start_str):
        self.Conn.sendall(str(len(start_str)).zfill(4) +'1'.encode())
        self.Conn.sendall(start_str.encode())
    def sent_mode(self, mode_str):
        self.Conn.sendall(str(len(mode_str)).zfill(4) +'2'.encode())
        self.Conn.sendall(mode_str.encode())
    def sent_who_first(self,who_first_str):
        self.Conn.sendall(str(len(who_first_str)).zfill(4) + '3'.encode())
        self.Conn.sendall(who_first_str.encode())
    def sent_posision(self, position_str):
        self.Conn.sendall(str(len(positon_str)).zfill(4) + '4'.encode())
        self.Conn.sendall(mode_str.encode())
    def sent_show_words(self,words_str):
        self.Conn.sendall(str(len(words_str)).zfill(4) + '5'.encode())
        self.Conn.sendall(words_str.encode())
    



def get_540_pic():
    first_img = pipeline.wait_for_frames()
    color_frame = first_img.get_color_frame()
    frame1 = np.asanyarray(color_frame.get_data())
    frame = np.zeros((540, 540, 3), np.uint8)
    frame[:, :, 0] = frame1[91: 631, 371:911, 0]
    frame[:, :, 1] = frame1[91: 631, 371:911, 1]
    frame[:, :, 2] = frame1[91: 631, 371:911, 2]
    return  frame


def get_540_depth():
    frames = pipeline.wait_for_frames()
    align_to = rs.stream.color
    align = rs.align(align_to)
    aligned_frames = align.process(frames)
    depth_frame = aligned_frames.get_depth_frame()
    color_frame = aligned_frames.get_color_frame()
    depth_image = np.asanyarray(depth_frame.get_data())
    frame = np.zeros((540, 540), np.uint8)
    frame[:, :] = depth_image[91: 631, 371:911]
    frame = cv.resize(frame, (135, 135))
    depth_img1 = cv.medianBlur(frame, 19)
    color_image = np.asanyarray(color_frame.get_data())
    frame1 = np.zeros((540, 540, 3), np.uint8)
    frame1[:, :, 0] = color_image[91: 631, 371:911, 0]
    frame1[:, :, 1] = color_image[91: 631, 371:911, 1]
    frame1[:, :, 2] = color_image[91: 631, 371:911, 2]
    return  frame1, depth_img1


def get_mode():
    count_remote = 0
    count_bottle = 0
    count_chess = 0
    count_mess = 0
    while True:  # 判断进入的mode ----->>>>> 1:遥控    2：下棋   3：倒水  4：杂物抓取
        cv.waitKey(30)
        frame = get_540_pic()
        rec.onlion_rec(frame)
        img2 = rec.add_bbox(frame)
        #print(rec.objtuple)
        for tuple in rec.objtuple:
            if tuple[2] == 1 and len(rec.objtuple) == 1:
                count_remote += 1
            elif tuple[2] == 4 and len(rec.objtuple) == 2:
                count_bottle += 1
            elif tuple[2] == 5 and len(rec.objtuple) == 1:
                count_chess += 1
            elif len(tuple) > 0:
                count_mess += 1
            else:print('没有东西呀！！！！')

        if count_remote == 5:
            return 1
        elif count_chess == 5:
            return 2
        elif count_bottle == 5:
            return 3
        elif count_mess == 5:
            return 4
        cv.imshow('mode_rec', img2)


def to_do_chess():
    f = open(file_path+'mode.txt','w')
    f.write('2')
    f.close()
    mode = input('请输入1（AI先手）或者2（人类先手）：')
    chess = GUI(mode)
    if mode == '1':sock.sent_posision(str(chess.x) +','+str(chess.y) +',2')
    robot_did = "0"
    for i in range(81):
        if i < 1 or robot_did == '1':
            chess_rec.get_position(pipeline)
            print("self.black_list", chess_rec.black_list)
            print('self.white_list', chess_rec.white_list)
            out = chess_rec.output_point()
            out_tuple = out.pop()  # 取出集合中的元素
            outx, outy = int(out_tuple[0]), int(out_tuple[1])
            sock.sent_posision(str(8-outy)+','+str(8 - outx)+',1')
            robotx,roboty = chess.down(8-outy, 8 - outx)
            sock.sent_posision(str(robotx) + ',' + str(roboty) + ',2')
            

        while True:
            try:
                f = open(file_path+'tag.txt', 'r+')
                robot_did = f.read()
                if robot_did == "1":
                    f.write('0')
                    f.close()
                    break
                else:
                    f.close()
            except:
                cv.waitKey(200)
                pass


def to_do_remote():
    f = open(file_path+'mode.txt','w')
    f.write('1')
    f.close()
    print('遥控模式')
    #等待命令，对即将来到的进行识别



def to_do_water():
    f = open(file_path+'mode.txt', 'w')
    f.write('3') #模式3为倒水模式
    f.close()
    print('倒水模式')
    bottle_list = []
    cup_list = []
    count_bottle = 0
    count_cup = 0
    tag = True
    while True:
        key = cv.waitKey(30)
        frame = get_540_pic()
        rec.onlion_rec(frame)
        img2 = rec.add_bbox(frame)
        # print(rec.objtuple)#识别到的tuple
        cv.imshow('pic', img2)
        for tuple in rec.objtuple:
            if tuple[2] == 4:
                x = tuple[0]
                y = tuple[1]
                bottle_list.append((x,y))
                count_bottle += 1
            if tuple[2] == 5:
                x = tuple[0]
                y = tuple[1]
                cup_list.append((x, y))
                count_cup += 1
        if count_bottle>5 and abs(bottle_list[count_bottle-1][0]- bottle_list[count_bottle-2][0])< 4 and  abs(bottle_list[count_bottle-1][1]- bottle_list[count_bottle-5][1])< 4 and tag:
            chess_rec.need2getreal.append(bottle_list[count_bottle-1])
            realx, realy = chess_rec.get_real()
            print(realx,realy)
            tag = False

            while True:
                try:
                    f = open(file_path+'setoff.txt', 'w')
                    f.write(str(realx) + ',' + str(realy) + ',1,2' )
                    f.close()
                    f = open(file_path+'flag.txt', 'w')
                    f.write('0')
                    f.close()
                    break
                except:
                    cv.waitKey(100)
                    pass
        f = open(file_path+'flag.txt', 'r+')
        if f.read() == '1' and tag ==False and count_cup>5 and abs(cup_list[count_cup-1][0]- cup_list[count_cup-5][0])< 4 and  abs(cup_list[count_cup-1][1]- cup_list[count_cup-5][1])< 4:
            chess_rec.need2getreal.append(cup_list[count_cup - 1])
            realx, realy = chess_rec.get_real()
            while True:
                try:
                    f = open(file_path+'setoff.txt', 'w')
                    f.write(str(realx) + ',' + str(realy) + ',1,2' )
                    print(str(realx) + ',' + str(realy) + ',' + '1')
                    f.close()
                    f = open(file_path+'flag.txt', 'w')
                    f.write('0')
                    f.close()
                    break
                except:
                    cv.waitKey(100)
                    pass
        f.close()
        if key =='27':
            print("倒水已完成！！！！")
            break











def to_do_obj_grab():
    print('物品抓取')
    flat_list = [] #选取扁平物的坐标
    #not_flat_list =[] #只能用大手抓的目标坐标
    did_it = False #初始化进入识别模式
    add_count = 0
    count_begin = False
    loop = 0
    switch_tag = 0 #初始化为吸取物体
    while True:
        try:
            f = open(file_path+'mode.txt','w')
            f.write('4')
            f.close()
            break
        except:
            cv.waitKey(100)
            pass
  
    while True:
        cv.waitKey(30)
        color, depth = get_540_depth()
        rec.onlion_rec(color)
        img2 = rec.add_bbox(color)
        # print(rec.objtuple)#识别到的tuple
        # cv.imshow('pic', img2)
        depth_rec = TargetRecognition(3000, 199)
        depth_rec.target(img2, depth)
        if not did_it:
            if len(depth_rec.tuplelist) == 0 and len(rec.objtuple) == 0:
                print("桌面上啥也没有！！")

            if (switch_tag == 1 and len(depth_rec.tuplelist) > 0)or (switch_tag ==0  and len(rec.tuplelist) == 0):
                tuple = depth_rec.tuplelist[0]
                chess_rec.need2getreal.append(tuple)
                realx, realy = chess_rec.get_real()
                while True:
                    try:
                        f = open(file_path+'setoff.txt', 'w')
                        f.write(str(realx) + ',' + str(realy) + ',1,2')
                        print('已经写好了杂物的坐标了！！！！   ')
                        f.close()
                        f = open(file_path+'flag.txt', 'w')
                        f.write('0')
                        f.close()
                        did_it = True
                        switch_tag = 0
                        break
                    except:
                        cv.waitKey(100)
                        pass








            if switch_tag == 0 or len(depth_rec.tuplelist)==0:
                for tuple in rec.objtuple:
                    if tuple[2] == 2  and len(flat_list) == 0:
                        count_begin = True
                        add_count =  1
                        flat_list.append((tuple[0], tuple[1]))
                    elif tuple[2] == 2 and not len(flat_list) == 0 and abs(
                            tuple[0] - flat_list[0][0]) < 5 and abs(tuple[1] - flat_list[0][1]) < 5:
                        add_count += 1
                        flat_list.append((tuple[0], tuple[1]))

                if loop > 10 and  add_count <8:
                    flat_list = []
                    add_count =0
                    loop =0
                    count_begin =False
                if add_count == 6:
                    chess_rec.need2getreal.append(flat_list[3])
                    realx, realy = chess_rec.get_real()
                    while True:
                        try:
                            f = open(file_path+'setoff.txt', 'w')
                            f.write(str(realx) + ',' + str(realy) + ',1,1')
                            print('已经写好了扁平物体的坐标了！！！！   ')
                            f.close()
                            f = open(file_path+'flag.txt', 'w')
                            f.write('0')
                            f.close()
                            add_count = 0
                            flat_list = []
                            count_begin = False
                            loop = 0
                            switch_tag =1
                            did_it = True
                            break
                        except:
                            cv.waitKey(100)
                            pass
            if count_begin:loop += 1
        try:
            f = open(file_path+'flag.txt', 'r+')
            if f.read() == '1': did_it =False
            f.close()
        except:
            f.close()









if __name__ == "__main__":

    file_path ='C:\\Users\\myosam\\Desktop\\zuobiao\\'
    pipeline = get_pipeline()
    for i  in  range(10): #不要前面20帧
        _img = pipeline.wait_for_frames()

    rec = Online_rec()#实例化在线识别
    while True: #初始棋盘矫正
        try:
            frame = get_540_pic()
            chess_rec = Recognize(frame) #实例化棋盘识别以便矫正
            ret, list = chess_rec.board_rectify()
            if ret == True:break
        except: pass
    sock = Socekt_connect()
    prin('等待连接！！')
    sock.start_wait()

    while True:  #语音输入等待

        try:
            f = open(file_path+'is_start.txt')
            if f.read() == '1':
                sock.sent_start('yes')
                f.close()
                break
        except:
            pass
                
    
    while True:
        #if input('是否开始？(y/n)：') == 'y':
            mode = get_mode()
            if mode == 1:
                sock.sent_mode('one')
                to_do_remote()
            elif mode == 2:
                sock.sent_mode('two')
                to_do_chess()
            elif mode == 3:
                sock.sent_mode('three')
                to_do_water()
            elif mode == 4:
                sock.sent_mode('four')
                to_do_obj_grab()

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    # for i in range(9):
    #     print("self.坐标系list", len(chess_rec.intersection_list[i]),chess_rec.intersection_list[i])
    # # cv.imshow('first_img',frame)

    # whattodo = input('下棋（1）还是其他（2）： ')
    # if whattodo == '1':
    #     mode = input('请输入1（AI先手）或者2（人类先手）：')
    #     chess = GUI(mode)
    #     #if mode == '1': cv.waitKey(1000)
    #     robot_did = "0"
    #     for i  in range(81):
    #         if i < 1 or robot_did == '1':
    #             chess_rec.get_position(pipeline)
    #             print("self.black_list", chess_rec.black_list)
    #             print('self.white_list', chess_rec.white_list)
    #             out = chess_rec.output_point()
    #             out_tuple = out.pop() #取出集合中的元素
    #             outx, outy = int(out_tuple[0]), int(out_tuple[1])
    #             chess.down(outx,8 - outy)
    # 
    #         while True:
    # 
    #             try:
    #                 f = open(file_path+'tag.txt','r+')
    #                 robot_did = f.read()
    #                 if  robot_did == "1":
    #                     f.write('0')
    #                     f.close()
    #                     break
    #                 else: f.close()
    #             except:
    #                 cv.waitKey(100)
    #                 pass
    # else:
    # 
    #      def getxy(event, x, y, flags, param):  # 获取鼠标点的hsv值
    #         if event == cv.EVENT_LBUTTONDOWN:
    #             x1= x
    #             y1 = y
    #             chess_rec.need2getreal.append((x1, y1))
    #             realx, realy = chess_rec.get_real()
    #             print(realx, realy)
    #      while True:
    #          cv.waitKey(30)
    # 
    #          rec.onlion_rec(frame)
    #          img2 = rec.add_bbox(frame)
    # 
    #          #print(rec.objtuple)#识别到的tuple
    #          cv.imshow('pic',img2 )
    #          cv.waitKey(20)
    #          cv.setMouseCallback('pic',getxy)