import cv2
import numpy as np
from matplotlib import pyplot as plt


def get_contours(img_data):
    """
    :param img_data: 图像数据
    :return: 所有区域轮廓; contours,contours_inv
    """
    img2gray = cv2.cvtColor(img_data, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img2gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    ret_inv, thresh_inv = cv2.threshold(img2gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)  # 黑白二值颠倒，用于识别剩余区域
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    contours_inv, hierarchy_inv = cv2.findContours(thresh_inv, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    # cv2.imshow('thresh', thresh)
    # cv2.imshow('thresh_inv', thresh_inv)
    # cv2.waitKey(0)
    return contours, contours_inv


def original_contour(img_data, drop_area=10):
    '''
    原始轮廓检测
    获得部分区域图像值
    正向反向标注出轮廓区域后，将小于“舍弃轮廓区域（area值：用户输入）”的轮廓区域删除
    :return:各个区域轮廓坐标
    '''
    contours, contours_inv = get_contours(img_data)
    area1, area2 = [],[]  # 图像的区域坐标
    for con in contours:
        if (cv2.contourArea(con) > drop_area):  # 筛选轮廓区域，小于用户要求区域大小的轮廓不显示
            cv2.drawContours(img_data, con, -1, (0, 255, 0), 1)
            area1.append(con)
    for con_inv in contours_inv:
        if (cv2.contourArea(con_inv) > drop_area):  # 筛选轮廓区域，小于用户要求区域大小的轮廓不显示
            cv2.drawContours(img_data, con_inv, -1, (0, 0, 255), 1)
            area2.append(con_inv)

    # cv2.imshow('all_contour', img_data)
    # cv2.waitKey(0)
    return area1, area2


def approx_poly(img_data, drop_area=0, epsilon_user=0.001):
    """
    凸性轮廓检测
    获得部分区域图像值
    根据用户输入epsilon获取轮廓区域后，将小于“舍弃轮廓区域（area值：用户输入）”的轮廓区域删除
    :param img_data:
    :param drop_area:
    :param epsilon_user: 0.0<epsilon<1.0
    :return: 各个区域轮廓坐标
    """

    area1, area2 = [], []  # 图像的区域坐标
    contours, contours_inv = get_contours(img_data)

    for con in contours:
        if cv2.contourArea(con) > drop_area:  # 筛选轮廓区域，小于用户要求区域大小的轮廓不显示
            epsilon = epsilon_user * cv2.arcLength(con, True)
            approx = cv2.approxPolyDP(con, epsilon, True)
            cv2.drawContours(img_data, [approx], -1, (0, 255, 0), 1)
            area1.append([approx])
    for con_inv in contours_inv:
        if (cv2.contourArea(con_inv) > drop_area):  # 筛选轮廓区域，小于用户要求区域大小的轮廓不显示
            epsilon = epsilon_user * cv2.arcLength(con_inv, True)
            approx_inv = cv2.approxPolyDP(con_inv, epsilon, True)
            cv2.drawContours(img_data, [approx_inv], -1, (0, 0, 255), 1)
            area2.append([approx_inv])
    # cv2.imshow('all_contour', img_data)
    # cv2.waitKey(0)
    return area1, area2


def hull_contour(img_data, drop_area=100):
    '''
    多边形检测
    获得部分区域图像值
    用convexHull()标识轮廓，将小于“舍弃轮廓区域（area值：用户输入）”的轮廓区域删除
    :return: 各个区域轮廓坐标
    '''
    area1, area2 = [],[]  # 图像的区域坐标
    contours, contours_inv = get_contours(img_data)
    for con in contours:
        if (cv2.contourArea(con) > drop_area):  # 筛选轮廓区域，小于用户要求区域大小的轮廓不显示
            hull = cv2.convexHull(con)
            cv2.drawContours(img_data, [hull], -1, (0, 255, 0), 1)
            area1.append([hull])

    for con_inv in contours_inv:
        if (cv2.contourArea(con_inv) > drop_area):  # 筛选轮廓区域，小于用户要求区域大小的轮廓不显示
            hull = cv2.convexHull(con_inv)
            cv2.drawContours(img_data, [hull], -1, (0, 0, 255), 1)
            area2.append([hull])

    #cv2.imshow('all_contour', img_data)
    #cv2.waitKey(0)
    return area1, area2


def distinguish(img):
    histG = plt.hist(img.ravel(), 256, [0, 256])
    plt.show()
    hist_content = histG[0].tolist()
    crest_top = max(hist_content)
    peak_index = hist_content.index(crest_top)
    print(peak_index)


def drawContour(img):  # 根据输入图，利用大津算法确认阈值然后分离二值图
    img1 = img.copy()
    img2gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    histG = plt.hist(img2gray.ravel(), 256, [0, 256])
    plt.show()
    ret2, thresh = cv2.threshold(img2gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(img1, contours, -1, (0, 0, 255), 1)
    cv2.imshow('thresh_ostu', img1)
    cv2.waitKey(0)


def detect_outline(outline_type, img_data, drop_area=0, epsilon_user=0.001):
    res1, res2 = [], []
    if outline_type == 1:
        res1, res2 = original_contour(img_data, drop_area)
        #print(res1,res2)
    elif outline_type == 2:
        res1, res2 = hull_contour(img_data, drop_area)
    else:
        res1, res2 = approx_poly(img_data, drop_area, epsilon_user)
    return res1, res2


if __name__ == '__main__':
    img = cv2.imread('D:/my.png')
    print(img)
    print(type(img))
    # distinguish(img)
    # drawContour(img)
    # original_contour(img)
    area1, area2 = approx_poly(img)
    print(area1)
    # hull_contour(img)
