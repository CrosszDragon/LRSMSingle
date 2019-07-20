# --coding:utf-8--
"""提取区域图片信息类

本系统中，tile就是切片

在工具中对想标注的区域进行矩形框勾选区域后，
将该矩形框所涉及的那些切片tile从原图中提取出来，
然后进行拼接，
对拼接之后的图片拷贝出矩形框所占的区域形成numpy.array类型的图片，
作为成员变量area_img保存在该类中，

Example:
    当实例化该类后，可以直接调用area_img即可获得矩形框区域的图片
    ifr=ImgFromRect(QRect(),tile_size=1000,slide_helper=slide)      ;#  example：   生成slide对象例子：        slide_helper=SlideHelper("传入图片路径")
    target_area_img=ifr.area_img

"""
from PyQt5.QtCore import *
from loadbig.slide_helper import SlideHelper
from loadbig.util import *
import numpy as np
import cv2


class ImgFromRect:
    '''从指定rect区域中提取部分图片'''

    def __init__(self, ori_rec: QRect, slide_helper: SlideHelper, tile_size: int = 1000, ):
        '''最终从根据rect获取到area_img'''
        self.tile_size = tile_size
        self.ori_rec = ori_rec  # 传入的矩形框rec信息
        self.tiles_pilmap_group = []  # 放置区域所占据tile的图片
        self.slide_helper = slide_helper

        self.joint_img = None  # 保存tiles_pilmap_group中拼接的图片

        # ========================================================
        # area_img,调用本类主要希望获得的成员
        # =======================================================
        self.area_img = None  # 最终赋值为目标区域的numpy数组

        # 由于原图并不会被刚好整数倍的被tile_size切割出来，对于最右边的tile和最下边的tile
        # 很大程度上会出现tile的宽度和高度并不是tile_size
        self.r_tile_width = slide_helper.slide_dimension[0] % tile_size  # 图像中最右边tile的宽度
        self.b_tile_height = slide_helper.slide_dimension[1] % tile_size  # 图像中最下边tile的宽度
        self.r_tile_xcoor = slide_helper.slide_dimension[0] - self.r_tile_width  # 最右边tile的横坐标
        self.b_tile_ycoor = slide_helper.slide_dimension[1] - self.b_tile_height  # 最下边tile的纵坐标

        self.get_tiles_pixmap()
        self.joint_tiles_to_img()
        self.get_area_img()

    def get_tiles_pixmap(self):
        '''获取在原大图中哪些tiles被包含在区域内，并将这些tile放到tiles_group中'''
        l_t_tile = [0, 0]  # 初始化左上角tile
        row_n = self.ori_rec.x() // self.tile_size  # 获得所涉及到的左上角tile横向是第几个tile
        l_t_tile[0] = row_n * self.tile_size  # 左上角tile的x坐标
        col_n = self.ori_rec.y() // self.tile_size  # 获得所涉及的左上角tile列向是第几个tile
        l_t_tile[1] = col_n * self.tile_size  # 左上角tile的y坐标

        r_t_tile = [0, 0]  # 初始化左上角tile
        row_n = (self.ori_rec.x() + self.ori_rec.width()) // self.tile_size  # 获得所涉及到的右上角tile横向是第几个tile
        r_t_tile[0] = row_n * self.tile_size  # 右上角tile的x坐标
        r_t_tile[1] = l_t_tile[1]  # 右上角tile的y坐标

        n_tile_x = (r_t_tile[0] - l_t_tile[0]) // self.tile_size + 1  # 横向占据的tile数

        l_b_tile = [0, 0]  # 初始化左下角tile
        col_n = (self.ori_rec.y() + self.ori_rec.height()) // self.tile_size  # 获得所涉及的左下角tile列向是第几个tile
        l_b_tile[0] = l_t_tile[0]  # 左下角tile的横坐标确定
        l_b_tile[1] = col_n * self.tile_size  # 左下角tile的纵坐标确定

        n_tile_y = (l_b_tile[1] - l_t_tile[1]) // self.tile_size + 1  # 纵向占据的tile数

        cur_tile = l_t_tile.copy()  # 表示当前要获取tile图片的tile
        for i in range(n_tile_y):  # 获取所占据的tile的pixmap，放到tiles_pixmap_group中
            x_pilmap_group = []  # 用于装载每一行的tile_img
            cur_tile[0] = l_t_tile[0]  # 每次从最左边开始获取tile
            for j in range(n_tile_x):  # 对于每一行，从最左边开始获取tile的图像信息放入x_pilmap_group
                pilimg_rec = [cur_tile[0], cur_tile[1], 0, 0]  # 要在原图中截取区域的rec的坐标赋值

                '''对于要取图片的tile，先判断该tile所在坐标是否处于最右端'''
                if cur_tile[0] == self.r_tile_xcoor:  # 该tile处于最右边
                    pilimg_rec[2] = self.r_tile_width
                else:
                    pilimg_rec[2] = self.tile_size

                '''对于要取图片的tile，先判断该tile所在坐标是否处于最底部'''
                if cur_tile[1] == self.b_tile_ycoor:  # 该tile处于最底部
                    pilimg_rec[3] = self.b_tile_height
                else:
                    pilimg_rec[3] = self.tile_size

                # 从slide对象中获取tile图像
                pilimg = self.slide_helper.read_region_from_big(pilimg_rec[0], pilimg_rec[1], 0,
                                                                (pilimg_rec[2], pilimg_rec[3]))
                x_pilmap_group.append(pilimg)
                cur_tile[0] += self.tile_size  # 横向移动到下一个tile
            cur_tile[1] += self.tile_size  # 纵向移动到下一行tile
            self.tiles_pilmap_group.append(x_pilmap_group)
        '''成功获取所占据tile区域的pixmap图片，并放到了tiles_pixmap_group中'''

    def joint_tiles_to_img(self):
        '''将tiles_pilmap_group中图片进行拼接,赋给joint_img'''
        # 先将同一横坐标的pil image进行拼接
        hori_joint_img_group = []
        for item in self.tiles_pilmap_group:
            if len(item) == 1:  # 若横向方向本来就只有一张图片，不做拼接
                hori_joint_img_group.append(item[0])
            else:  # 有两张以上，进行拼接
                joint_img = item[0]
                for i in range(len(item) - 1):
                    joint_img = joint_two_image(joint_img, item[i + 1], 'horizontal')
                hori_joint_img_group.append(joint_img)
        '''将横向拼接好的图片进行纵向拼接'''
        final_img = hori_joint_img_group[0]
        if len(hori_joint_img_group) == 1:
            self.joint_img = final_img
        else:
            for i in range(len(hori_joint_img_group) - 1):
                final_img = joint_two_image(final_img, hori_joint_img_group[i + 1], 'vertical')
            self.joint_img = final_img

    def get_area_img(self):
        '''从拼接图中获取目标rect区域中部分图片，赋给area_img'''
        # 1.将原始矩形框转换为要截取部分的crop
        crop = [0, 0, 0, 0]  # 在拼接好的图像中要截取的区域，其中前俩参数为左上角坐标，后俩为右下角坐标
        crop[0] = self.ori_rec.x() % self.tile_size
        crop[1] = self.ori_rec.y() % self.tile_size
        crop[2] = crop[0] + self.ori_rec.width()
        crop[3] = crop[1] + self.ori_rec.height()

        # 2.传入crop截取目标区域像素到area_img
        self.area_img = self.joint_img.crop(crop)  # .crop()是传入一个左上角和右下角左边，将这俩坐标围成的矩形区域图像截取出来
        self.area_img = np.array(self.area_img)


if __name__ == '__main__':
    slide_he = SlideHelper('../sources/Level_17.tif')
    i = ImgFromRect(QRect(20662, 12900, 2000, 2000), tile_size=1000, slide_helper=slide_he)
    cv2.imshow('sd', i.area_img)
    cv2.waitKey(0)
