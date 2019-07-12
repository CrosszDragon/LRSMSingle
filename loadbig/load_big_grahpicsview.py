# --coding:utf-8--
"""继承于GraphicsView的大图片加载view

实现本类，通过传入大图片路径生成实例，会在view中展示大图片的缩略图以及原始大图片的缩放场景展现

一个大坑：opencv处理的图片都会将原图宽高反向；因此图片处理时应该进行相应变换以原图为基准进行变换

"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from loadbig.tileItem import TileItem
from loadbig.pyr_img_item import PyrIMGItem
from loadbig.util import *
from loadbig.slide_helper import SlideHelper
from UILayer.Workbench.GraphicsView import GraphicsViewTest


class LoadIMGraphicsView(GraphicsViewTest):
    '''
    装载大图片和金字塔压缩图的view
    '''
    SCALE_FACTOR = 1.0  # 缩放因子，当scene放置的是大图时，将原始图像的SCALE_FACTOR置为1；缩放时记录缩放因子

    def __init__(self, gadget, toolbar_gadget, eraser_size, img_path, scene: QGraphicsScene, parent=None):
        super(LoadIMGraphicsView, self).__init__(gadget, toolbar_gadget, eraser_size, parent)
        # self.scene_pyr = QGraphicsScene()  # 放置缩略图的场景
        self.setBackgroundBrush(QColor(147, 147, 147))
        self.scene_big = scene  # 放置原始大图的场景
        self.setScene(scene)
        self.slide_helper = SlideHelper(img_path)  # 获取sldie对象
        self.scene_big.setSceneRect(0, 0, self.slide_helper.slide_dimension[0], self.slide_helper.slide_dimension[1])
        self.tile_items_group = self.get_tiles_group()  # 装载原图itemgroup

        self.is_so_big = is_img_so_big(path=img_path)  # 若图片大于2G
        if not self.is_so_big:  # 若大图没有超过2G
            self.pyr_item = PyrIMGItem(img_path)  # 放置压缩图的item
            self.is_big = self.pyr_item.is_big  # 判定是否是大图片

            self.cur_scene_img = True  # 当前场景图片，True表示放的是金字塔缩略图，False表示放的是原始大图的切片图
            self.pyr_factor = self.pyr_item.pyr_factor  # 原图与压缩总览图的压缩比

            self.w_dimension_change = self.slide_helper.slide_dimension[0] / self.slide_helper.slide_dimension[
                1]  # 表示opencv计算后导致改变的图片宽的维度伸缩比
            self.h_dimension_change = self.slide_helper.slide_dimension[1] / self.slide_helper.slide_dimension[0]

            self.scene_big.addItem(self.pyr_item)  # pyr场景放置缩略图

        else:   #加载的是大于2G的图片
            self.scene_big.addItem(self.tile_items_group)
            self.centerOn(self.mapToScene(QPoint(self.slide_helper.slide_dimension[0]/2,
                                                 self.slide_helper.slide_dimension[1] / 2)))

    def wheelEvent(self, event: QWheelEvent) -> None:
        """鼠标滑轮事件"""
        if not self.is_so_big:
            d_value = event.angleDelta().y() / 120
            d_value = -4 * d_value
            des_pos = self.mapToScene(event.pos())
            if self.is_big:  # 若是大图片
                if event.modifiers() & Qt.ControlModifier:  # 按下ctrl键和滑动滚轮，进行图像缩放
                    factor = 1.09 if d_value < 0 else 0.91
                    if factor > 1:  # 放大操作
                        if self.cur_scene_img:  # 表示当前secen中为金字塔缩略图
                            self.tilesgroup_put_in_scene()  # 切换scene为对应坐标的原始大图片
                            self.cur_scene_img = False  # 表示当前scene中为原始大图片
                            # 当从缩略图移动到大图，在缩略图鼠标滚轮操作坐标，放大到原始图时，自动移动场景到缩略图坐标处对应的原图图坐标区域
                            self.centerOn(self.mapToScene(QPoint(des_pos.x() * self.pyr_factor * self.w_dimension_change,
                                                                 des_pos.y() * self.pyr_factor * self.h_dimension_change)))
                        else:
                            self.scale(factor, factor)
                            self.SCALE_FACTOR = self.transform().m11()
                    else:  # 缩小操作
                        if not self.cur_scene_img:  # 若当前处于大图片场景
                            if factor * self.SCALE_FACTOR <= 1:  # 表示将缩小到比原图还小,切换为金字塔总览图
                                self.SCALE_FACTOR = 1.0
                                self.pyr_put_in_scene()  # 场景设置回金字塔缩略图
                                self.cur_scene_img = True
                            else:
                                self.scale(factor, factor)
                                self.SCALE_FACTOR = self.transform().m11()
                else:
                    GraphicsViewTest.wheelEvent(self, event)
        else:
            GraphicsViewTest.wheelEvent(self, event)

    def tilesgroup_put_in_scene(self):
        '''切换放缩略图的scene，view的scene设置为装载大图片的全部切片tiles的场景'''
        self.scene_big.removeItem(self.pyr_item)
        self.scene_big.addItem(self.tile_items_group)
        # self.centerOn(self.tile_items_group)

    def pyr_put_in_scene(self):
        '''当前处于大图片scene,切换为缩略图场景'''
        self.scene().removeItem(self.tile_items_group)
        self.scene().addItem(self.pyr_item)
        self.centerOn(self.pyr_item)

    def get_tiles_group(self) -> QGraphicsItemGroup:
        '''传入一个level总像素以及一个tile的size,返回一个铺满level的tile_rec的list'''
        tiles_group = QGraphicsItemGroup()
        tiles_rects = slice_rect(self.slide_helper.slide_dimension[0], self.slide_helper.slide_dimension[1],
                                 self.slide_helper.tile_size)
        downsample = self.slide_helper.slide.level_downsamples[0]
        for tile_rect in tiles_rects:  # 画出需要画出的所有tile
            item = TileItem(tile_rect, self.slide_helper, 0, downsample)
            item.moveBy(tile_rect[0], tile_rect[1])  # 移动到对应坐标
            tiles_group.addToGroup(item)
        return tiles_group
