# --**-- coding : utf-8 --**--
# --**-- author:dingchao --**--
# --**-- time :190726   --**--

import cv2  as cv
import numpy as np
import pyrealsense2 as rs
import threading



# using intel realsense



class Recognize():
    def  __init__(self, no_chess_img):
       self.first_img = no_chess_img
       self.white_min = np.array([70, 5, 180])###手动调整，主要是光线影响对这个有很大的干扰
       self.white_max = np.array([75, 30, 220])
       self.black_min = np.array([0, 0, 0])
       self.black_max = np.array([130, 120, 70])
       self.black_list = []   ###识别到的黑子白子，存放的是（x,y）
       self.white_list = []
       self.blackpointij = [] ###存放(i,j)，第几行，第几列
       self.whitepointij =[]
       self.intersection_list =  [[]for i in range(9)]###存放棋盘的交点坐标
       self.time_count = 0
       self.time_tag = 0
       self.len_w_and_b =0
       self.need2getreal =[]
       self.realist = [[]for i in range(9)] 
       for j in range(9):
           for i in range(9):
               self.realist[j].append((i * 3.1, round(24.8 - j * 3.1, 1)))

           

    def get_real(self):
        need2rel = self.need2getreal[0]
        positionij = (0,0)
        tag = 0
        for j in range(8):
            if need2rel[1] >= self.intersection_list[j][0][1] - 15 and need2rel[1] <= \
                    self.intersection_list[j + 1][0][1] + 15 and not tag==1:
                for i in range(8):
                    if need2rel[0] >= self.intersection_list[j][i][0]   and need2rel[0] <= \
                            self.intersection_list[j][i+1 ][0] :
                        if need2rel[1] >= self.intersection_list[j][i][1] and need2rel[1] <=self.intersection_list[j+1][i][1]:

                            positionij = (i, j)
                            positionij = (i, j)
                            tag = 1
                            break
                        elif need2rel[1] >= self.intersection_list[j-1][i][1] and need2rel[1] <=self.intersection_list[j][i][1]:
                            positionij = (i, j-1)
                            tag = 1
                            break
            if tag ==1:break
        if not positionij == (0,0):
           i = positionij[0]
           j = positionij[1]
           realx1 =  self.realist[j][i][0] + 3.1* (need2rel[0] - self.intersection_list[j][i][0])/(self.intersection_list[j][i+1][0] - self.intersection_list[j][i][0])
           realy1 = self.realist[j][i][1]  - 3.1* (need2rel[1]- self.intersection_list[j][i][1])/(self.intersection_list[j+1][i][1] - self.intersection_list[j][i][1])
           realx = realy1
           realy = 24.8 - realx1
        self.need2getreal =[]
        return realx, realy



    def board_rectify(self):#  输出坐标列表
        def perfect_it(ranked_list):
            new_list = []
            def delete_some(ranked_list):
                for i in range(len(ranked_list)):
                    repeat = False
                    repeat_back = False
                    if i < len(ranked_list) - 1:
                        repeat = (((ranked_list[i][1] - ranked_list[i + 1][1]) ** 2 + (
                                ranked_list[i][0] - ranked_list[i + 1][0]) ** 2) < 100)
                    if i > 1:
                        repeat_back = (((ranked_list[i][1] - ranked_list[i - 1][1]) ** 2 + (
                                ranked_list[i][0] - ranked_list[i - 1][0]) ** 2) < 100)
                    if i < len(ranked_list) - 1 \
                            and ranked_list[i][1] <= ranked_list[i + 1][1]  +5 \
                            and ranked_list[i][1] >= ranked_list[i + 1][1] - 5\
                            and not repeat:  ##可手动调整
                        new_list.append(ranked_list[i])
                    elif i > 1 \
                            and ranked_list[i][1] <= ranked_list[i - 1][1] + 5 \
                            and ranked_list[i][1] >= ranked_list[i - 1][1] - 5\
                            and not repeat_back:
                        new_list.append(ranked_list[i])
                    else:
                        pass
                print('删除部分后长度为',len(new_list))

            def add_some(deleted_some):
                list_good = [[] for i in range(9)]
                y_list = []
                x_list = []
                y = 0
                for point in deleted_some:
                    if not (y - 20 <= point[1] <= y + 20):
                        y = point[1]
                        y_list.append(point[1])
                for i in range(9):
                    for point in deleted_some:
                        if (y_list[i] - 20 <= point[1] <= y_list[i] + 20):
                            list_good[i].append(point)
                        else:
                            pass


                for i in range(9):
                    if len(list_good[i]) < 9:
                        dlist = []
                        for j in range(len(list_good[i]) - 1):
                            d = list_good[i][j + 1][0] - list_good[i][j][0]
                            dlist.append(d)
                        sort = dlist.copy()
                        sort.sort()
                        min = sort[0]
                        for j in range(len(dlist)):
                            tmp = (dlist[j] + 10) // min
                            if tmp == 1:
                                pass
                            elif tmp == 2:
                                list_good[i].insert(j + 1, (list_good[i][j][0] + min, list_good[i][j][1]))
                            elif tmp == 3:
                                list_good[i].insert(j + 1, (list_good[i][j][0] + min, list_good[i][j][1]))
                                list_good[i].insert(j + 2, (list_good[i][j][0] + 2 * min + 1, list_good[i][j][1]))
                    else:
                        pass
                print('list good', list_good)
                return list_good
            # def delete_more(added_list):
            #     tmp_list =[]
            #     for i in range(9):
            #         if i==0 and added_list[i][0][0]< added_list[i+1][0][0] - 10:
            #             added_list[i].remove((added_list[i][0][0],added_list[i][0][1]))
            #         elif 0< i <8 and ((added_list[i-1][0][0]+ added_list[i+1][0][0])//2 )-10 > added_list[i-1][0][0]:
            #             added_list[i].remove((added_list[i][0][0],added_list[i][0][1]))
            #         elif i ==8 and added_list[i][0][0]< added_list[i-1][0][0] - 10:
            #             added_list[i].remove((added_list[i][0][0], added_list[i][0][1]))
            #         else:pass
            #     return added_list

            delete_some(ranked_list)
            perfect_list = add_some(new_list)
           # perfect_list = delete_more(perfect_list)
            return perfect_list

        def point_rank(points_list): #初始化所有点的排序
            points = points_list
            def compare(point1, point2):
                if point2[1] >= point1[1] + 15:
                    return False
                elif point2[1] <= point1[1] - 15:
                    return True
                elif point2[0] >= point1[0]:
                    return False
                else:
                    return True

            def points_rank(points_list):  # 采用快排
                if len(points_list) >= 2:
                    mid = points_list[len(points_list) // 2]  # 选取基准值
                    left, right = [], []  # 定义基准值左右两侧的列表
                    points_list.remove(mid)  # 从原始数组中移除基准值
                    for point in points_list:
                        if compare(point, mid):  # 返回值为真，表示point点比mid大
                            right.append(point)
                        else:
                            left.append(point)
                    return points_rank(left) + [mid] + points_rank(right)
                else:
                    return points_list

            new_lists = points_rank(points)
            print(len(new_lists),'排列好的坐标点：',new_lists)
            return new_lists

        def get_good_line(binary, img):
            # print(~gray ==255 - gray.copy())
            cv.waitKey(30)
            rows, cols = binary.shape
            scale = 30  ###可手动调节
            # 识别横线
            kernel = cv.getStructuringElement(cv.MORPH_RECT, (cols // scale, 1))
            eroded = cv.erode(binary, kernel, iterations=1)
            # cv.imshow("Eroded Image",eroded)
            dilatedcol = cv.dilate(eroded, kernel, iterations=1)
            cv.imshow("row", dilatedcol)
            # 识别竖线
            kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, rows // scale))
            eroded = cv.erode(binary, kernel, iterations=1)
            dilatedrow = cv.dilate(eroded, kernel, iterations=1)
            cv.imshow("col", dilatedrow)
            points_list = []
            # 标识交点
            bitwiseAnd = cv.bitwise_and(dilatedcol, dilatedrow)
            cv.imshow("points", bitwiseAnd.copy())
            im2, points, blackhierarchy = cv.findContours(bitwiseAnd, cv.RETR_EXTERNAL,
                                                           cv.CHAIN_APPROX_SIMPLE)
            for point in points:
                (x, y), radius = cv.minEnclosingCircle(point)
                center = (int(x), int(y))
                points_list.append(center)
                # radius = int(radius)
                # 绘制闭圆
                # img = cv.circle(img, center, radius, (0, 255, 0), 3)
                # cv.imshow('oo', img)
            # 标识表格

            points = point_rank(points_list)
            finallist = perfect_it(points)
            for i in range(9):
                for j in range(9):
                    img2 = cv.circle(img, finallist[i][j], 2, (0, 255, 255), 2)

            cv.imshow('biaoding',img2)
            cv.waitKey(0)
            cv.destroyAllWindows()

            return finallist

        gray = cv.cvtColor(self.first_img, cv.COLOR_BGR2GRAY)
        binary = cv.adaptiveThreshold(~gray, 255,
                                      cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 25, -8) #可手动调整
        self.intersection_list= get_good_line(binary, self.first_img)
        print('终于矫正好棋盘了！！')
        return True, self.intersection_list




    def get_position(self, pipeline):
        self.time_count = 0
        self.time_tag = 0
        while(1):
            key = cv.waitKey(30)
            self.black_list = []  # 每次重调方法后列表都置零
            self.white_list = []
            def gethsv(event, x, y, flags, param):  # 获取鼠标点的hsv值
                if event == cv.EVENT_LBUTTONDOWN:
                    print((x,y),hsv[y, x])


            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            frame1 = np.asanyarray(color_frame.get_data())
            frame = np.zeros((540, 540, 3), np.uint8)
            frame[:, :, 0] = frame1[91: 631, 371:911, 0]
            frame[:, :, 1] = frame1[91: 631, 371:911, 1]
            frame[:, :, 2] = frame1[91: 631, 371:911, 2]
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            white_mask = cv.inRange(hsv, self.white_min, self.white_max)
            black_mask = cv.inRange(hsv, self.black_min, self.black_max)
            _,whitecontours, hierarchy = cv.findContours(white_mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            __,blackcontours, blackhierarchy = cv.findContours(black_mask.copy(), cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
            cv.imshow("black",black_mask)
            cv.imshow("white",white_mask)
            for cb in blackcontours:
                x, y, w, h = cv.boundingRect(cb)
                if w > 29 and h > 29 and w <46and h <46 and abs(h-w)<7:#后面可以加上x, y的限制
                    cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    tuple=  (int(x + w//2), int(y + h//2))#标记黑色为1
                    self.black_list.append(tuple)


            for cw in whitecontours:
                x, y, w, h = cv.boundingRect(cw)
                if w > 30 and h > 30 and w < 50 and h <50 :
                    cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    tuple = (int(x + w // 2), int(y + h // 2))#标记白色为2
                    self.white_list.append(tuple)


            len_w_and_b = len(self.white_list)+len(self.black_list)

            #print(self.white_list)
            cv.imshow('img', frame)
            cv.setMouseCallback('img',gethsv)
            
            self.time_count += 1
            if self.len_w_and_b == len_w_and_b - 1 and self.time_count >=40:
                self.time_tag += 1
            if self.len_w_and_b == len_w_and_b - 1  and self.time_tag >= 25:
                self.len_w_and_b = len_w_and_b
                print('玩家已落子!')
                cv.destroyAllWindows()
                return 0


            if key == 27:
                cv.destroyAllWindows()
                print("手动退出")
                break


    def output_point(self):
        black_ij_init = self.blackpointij
        white_ij_init = self.whitepointij
        self.whitepointij = []
        self.blackpointij = []
        positionij = (0, 0)
        realpositon = (0, 0)
        min = 5000

        def dis(point1, point2):
            return (point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2
        min = 5000
        if not len(self.black_list) == 0:
            for point_black in self.black_list:
                end = 0
                for j in range(9):
                    if point_black[1] >= self.intersection_list[j][0][1] - 15 and point_black[1] <= \
                            self.intersection_list[j ][0][1] + 15:
                        for i in range(9):
                            if point_black[0] >= self.intersection_list[j][i][0] - 15 and point_black[0] <= \
                                    self.intersection_list[j][i][0] + 15:
                                positionij = (i, j)
                                end = 1
                                break

                    if end == 1: break

                self.blackpointij.append(positionij)
        if len(white_ij_init) == len(self.whitepointij):
            print("There is no white chess add! ")
        elif len(white_ij_init) < len(self.whitepointij):
            print('the new white chess:', set(self.whitepointij).difference(set(white_ij_init)))
        else:
            print("white rec error!!!!!!")

        if len(black_ij_init) == len(self.blackpointij):
            print('There is no black chess add!')
        elif len(black_ij_init) < len(self.blackpointij):
            print('The new black chess:', set(self.blackpointij).difference(set(black_ij_init)))
            return set(self.blackpointij).difference(set(black_ij_init))
        else:
            print('Black rec error!!!')










