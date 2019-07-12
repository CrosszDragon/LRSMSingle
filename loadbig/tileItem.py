# --coding:utf-8--
"""将tile转换为QGraphicsItem类

本类传入tile在大图片中的坐标，将该tile画到此item中
实例化本类则是实例化一个包含tile的GraphicsItem

"""
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PIL.ImageQt import ImageQt  # 可以将PIL格式图片转换为QPixmap
from loadbig.slide_helper import SlideHelper


class TileItem(QGraphicsItem):

    def __init__(self, x_y_w_h, slide: SlideHelper, level, downsample):
        super(TileItem, self).__init__()
        self.x_y_w_h = x_y_w_h  # tile_rect,相同的w和h，不同的坐标
        '''生成一个tile的rect，长宽可能不同，坐标依次紧挨着排列'''

        self.slide_rect_0 = QRect(int(x_y_w_h[0] * downsample), int(self.x_y_w_h[1] * downsample), x_y_w_h[2],
                                  x_y_w_h[3])
        self.level = level
        self.setAcceptedMouseButtons(Qt.NoButton)
        self.setAcceptHoverEvents(False)
        self.cache_key = "{}.{}".format(self.slide_rect_0.x(), self.slide_rect_0.y())  # 字符串
        self.slide = slide

    def pilimage_to_pixmap(self, pilimage):  # PIL图片转换为QPixmap
        qim = ImageQt(pilimage)
        pix = QPixmap.fromImage(qim)
        return pix

    def boundingRect(self):
        return QRectF(0, 0, self.slide_rect_0.width(), self.slide_rect_0.height())  # 返回一个tile大小矩形

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem,
              widget: QWidget = ...):
        self.pixmap = QPixmapCache.find(self.cache_key)  # 生成Pixmap图像
        if not self.pixmap:
            '''从原大图片读取tile'''
            tile_pilimage = self.slide.read_region_from_big(self.x_y_w_h[0], self.x_y_w_h[1], self.level,
                                                            (self.x_y_w_h[2], self.x_y_w_h[3]))
            '''pil图片转为pixmap'''
            self.pixmap = self.pilimage_to_pixmap(tile_pilimage)

            QPixmapCache.insert(self.cache_key, self.pixmap)  # 将生成tile存入QPixmanpCache中
        painter.drawPixmap(self.boundingRect().toRect(), self.pixmap)
