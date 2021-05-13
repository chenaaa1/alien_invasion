import pygame
from pygame.sprite import Sprite    # 从模块pygame.sprite导入Sprite类


class Bullet(Sprite):
    """管理飞船所发射的子弹的类"""

    def __init__(self, ai_game):    #ai_game是因为需要当前的AlienInvasion实例
        """在飞船当前位置创建一个子弹对象"""
        super().__init__()  # 这里调用了super来继承Sprite
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # 在（0，0）处创建一个表示子弹的矩形，再设置正确的位置
        # 因为子弹不是图像产生的，所以要用pygame.Rect类从头开始创建一个矩形
        # 提供矩形左上角的x和y坐标，还有矩形的宽度和高度
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)    # 随便换行应该没什么问题
        self.rect.midtop = ai_game.ship.rect.midtop # 将子弹从飞船顶部出发，存为小数值方便微调

        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y)

    def update(self):
        """向上移动子弹"""
        # 更新表示子弹位置的小数值
        self.y -= self.settings.bullet_speed    # 减去速度相当于更新子弹位置
        # 更新表示子弹的rect的位置
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)    # draw.rect也是pygame的一个函数