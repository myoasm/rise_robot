import pyrealsense2 as rs
import cv2
import numpy as np


def access_pixels(image):
    ##相当于取反 例如白的变成黑的，黑的变成白的，
    for row in range(image.shape[0]):
        for col in range(image.shape[1]):
            pv = image[row, col]
            image[row, col] = 255 - pv  # 相当于取反 例如白的变成黑的，黑的变成白的，
    return image

class TargetRecognition():
    def __init__(self,minarea = 3000,threshold_value = 180):
        self.minarea=minarea
        self.threshold_value =threshold_value
        self.tuplelist = []
        # self.pipeline = rs.pipeline()
        # config = rs.config()
        # config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
        # config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
        # self.profile = self.pipeline.start(config)

        # 获取深度传感器的深度标尺（参见rs - align示例进行说明）
        # depth_sensor = self.profile.get_device().first_depth_sensor()
        # depth_scale = depth_sensor.get_depth_scale()
        # print("Depth Scale is: ", depth_scale)

        # 我们将删除对象的背景
        # #  clipping_distance_in_meters meters away
        # clipping_distance_in_meters = 1  # 1 meter
        # clipping_distance = clipping_distance_in_meters / depth_scale

        # 创建对齐对象
        # rs.align允许我们执行深度帧与其他帧的对齐
        # “align_to”是我们计划对齐深度帧的流类型。
        # align_to = rs.stream.color
        # self.align = rs.align(align_to)


    def take_img(self):
        pass
            # frames = self.pipeline.wait_for_frames()
            # # 将深度框与颜色框对齐
            # aligned_frames = self.align.process(frames)
            #
            # # 获取对齐的帧
            # depth_frame = aligned_frames.get_depth_frame()  # aligned_depth_frame是640x480深度图像
            # color_frame = aligned_frames.get_color_frame()
            #
            # # depth_frame = frames.get_depth_frame()
            # depth_image = np.asanyarray(depth_frame.get_data())
            # frame = np.zeros((540, 540), np.uint8)
            # frame[:, :] = depth_image[91: 631, 371:911]
            # # dst = cv2.GaussianBlur(frame, (5, 5), 0)  # 高斯滤波
            # depth_img1 = cv2.medianBlur(frame, 19)  # 中值滤波
            # # depth_img2= cv2.pyrDown(depth_img1)
            #
            # color_image = np.asanyarray(color_frame.get_data())
            # frame1 = np.zeros((540, 540, 3), np.uint8)
            # frame1[:, :, 0] = color_image[91: 631, 371:911, 0]
            # frame1[:, :, 1] = color_image[91: 631, 371:911, 1]
            # frame1[:, :, 2] = color_image[91: 631, 371:911, 2]
            # # color_img = cv2.pyrDown(frame1)
            # color_img = frame1
            #
            # return color_img,depth_img1

    def target(self,color_img, depth_img):
            # self.color_img,self.depth_img=self.take_img()
            frame = color_img
            ret, depth_img2 = cv2.threshold(depth_img, self.threshold_value, 255, cv2.THRESH_BINARY)  #二值化
            depth_img = access_pixels(depth_img2)
            imge, contours, hierarchy = cv2.findContours(depth_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.imshow('llal',depth_img)
            area = []
            cX = []
            cY = []
            i = 0
            hasobj = False
            try:
                for c in contours:
                    # 获取中心点
                    # y=int(M["m01"] / M["m00"])
                    if cv2.contourArea(c) > self.minarea//20:

                        M = cv2.moments(c)
                        y = int(M["m01"] / M["m00"])
                        if y < 500:
                            area.append(cv2.contourArea(c))
                            cX.append(int(M["m10"] / M["m00"]))
                            cY.append(int(M["m01"] / M["m00"]))
                            # 画出中点
                            cv2.circle(color_img, (cX[-1]*4, cY[-1]*4), 7, (255, 255, 255), -1)
                            cv2.putText(color_img, "obj" + str(i), (cX[-1]*4 - 20, cY[-1]*4 - 20),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                            i = i + 1
                            hasobj=True
                            self.tuplelist.append((cX[-1]*4, cY[-1]*4))
                    # x, y, w, h = cv.boundingRect(c)
                    # cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    # tuple = (int(x + w // 2), int(y + h // 2))
                    # self.tuplelist.append(tuple)





                # print(area)
                # max_num = area.index(max(area))
                # print(max_num)
                # print(cX[max_num], cY[max_num])
            except:
                print("无目标")
            #图片合并显示
            # depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(img5, alpha=0.03), cv2.COLORMAP_JET)
            # images = np.hstack((img11, depth_colormap))
            cv2.imshow('recgnize', color_img)
            cv2.waitKey(30)





# def main():
#     A=TargetRecognition(3000,199)
#     while True:
#         hasobj,(X,Y)=A.target()
#     pipeline.stop()
# 
# 
# if __name__ == '__main__':
#     main()








