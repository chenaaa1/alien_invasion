import pygame.font

from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    """显示得分信息的类"""

    def __init__(self, ai_game):    # 要思考一下为什么每次都要传入ai_game
        """初始化显示得分涉及的属性"""
        self.ai_game = ai_game  # 将游戏实例赋给一个属性
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)   # 实例化一个字体对象

        # 准备初始得分图像
        self.prep_score()   # 将显示的文本转为图像

        #  准备包含最高得分和当前得分的图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """将得分转化为一幅渲染的图像"""
        rounded_score = round(self.stats.score, -1)
        # 函数round让小数精确到小数点后某一位，其中小数位数由第二个实参决定，若为负数则舍入到10的整数倍
        score_str = "{:,}".format(rounded_score)    # format是方法
        # 字符串格式设置指令，将得分每3位用逗号显示出来
        score_str = str(self.stats.score)   # str是一个类，python自带的吧
        # 将数值stats.score转为字符串,再将字符串传递给创建图像的render（）
        self.score_image = self.font.render(score_str, True,
                        self.text_color, self.settings.bg_color)
        # text_color, self.settings.bg_color是向render传递背景色和文本颜色

        # 在屏幕右上角显示得分
        self.score_rect =self.score_image.get_rect()
        # 让得分板右边缘与屏幕右边缘相距20像素
        self.score_rect.right = self.screen_rect.right - 20
        # 让其上边缘与屏幕上边缘也相距20像素
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高得分转换为渲染的图像"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        # 根据最高得分生成一幅图像
        self.high_score_image = self.font.render(high_score_str, True,
                                        self.text_color, self.settings.bg_color)

        # 将最高得分放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        # 使其水平居中
        self.high_score_rect.centerx = self.screen_rect.centerx
        # 将其top属性设置为当前得分图像的top属性
        self.high_score_rect.top = self.score_rect.top

    def show_score(self):
        """在屏幕上显示得分"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)    # 绘制每艘飞船

    def check_high_score(self):
        """检查是否诞生了新的最高分"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """将等级转换为渲染的图像"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                                self.text_color, self.settings.bg_color)

        # 将等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
        # 比得分图像的bottom属性大10像素

    def prep_ships(self):
        """显示还余下多少艘飞船"""
        self.ships = Group()    # 创建一个空编组self.ships，用于存储飞船实例
        for ship_number in range(self.stats.ships_left):     # 根据剩余飞船填充编组
            ship = Ship(self.ai_game)   # 创建新飞船
            ship.rect.x = 10 + ship_number * ship.rect.width
            # 让整个飞船编组位于屏幕左边，且每艘飞船左边距为10像素
            ship.rect.y = 10    # 让飞船出现在离屏幕上边缘10像素，即左上角
            self.ships.add(ship)    # 将每艘新飞船添加到编组ships中
