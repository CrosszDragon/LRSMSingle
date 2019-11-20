# --coding:utf-8--
"""openslide对象模块

根据输入路径利用openslide库生成slide对象，表示对于原图的切割对象
成员函数包括原图像素，切割为片的片单位大小
以及封装openslide库中read_region函数为red_region_from_big函数

"""
# import openslide


class SlideHelper():
    '''将openslide库要用到的封装为SlideHelper,主要用到DeepZoomGenerator获得tile'''

    def __init__(self, slide_path: str):
        self.slide_path = slide_path
        # 根据图片路径获取slide滑动对象(理解为在大图片中滑动切割)
        self.slide = openslide.OpenSlide(self.slide_path)

        # 获取slide对象level级别list，该list包含内容为将大图片划分为几个等级，本项目中只用到最后一级，切割最多tile(小片)出来
        self.levels = self.slide.level_count
        self.slide_dimension = self.slide.level_dimensions[0]  # 总像素
        t = ((self.slide_dimension[0] * self.slide_dimension[
            1]) / 2000) ** 0.5  # 将level这一层图片总像素除以2000形成大约2000个rect然后开根号
        if t < 1000:
            t = 1000  # 至少分为1000个rect
        self.tile_size = (int(t), int(t))  # 设置tile的大小

    def read_region_from_big(self, x, y, level, size: tuple):
        '''
        读取原大图中对应区域的切片返回
        :param x: 切片的左上角x坐标
        :param y:
        :param level: 切片所在slide对象的level级，本系统只使用level=0
        :param size:类型为tuple,包括所切切片的大小
        :return: 切出的切片图片，类型为PIL.Image，即python中图形库的图像类型
        '''
        # x,y是在原图中的像素位置
        pil_img = self.slide.read_region((x, y), level, size)
        return pil_img
