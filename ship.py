import pygame


class Ship:
    """管理飞船的类"""

    def __init__(self,ai_game):
        """初始化飞船并设置其初始位置"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')   # pygame的加载文件函数pygame.image.load
        self.rect = self.image.get_rect()   # get_rect也是pygame的一个函数

        # 对于每艘新飞船，都将其放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom    # midbottom底部中央函数

        # 在飞船的属性x中存储小数值
        self.x = float(self.rect.x)

        # 移动标志
        self.moving_right = False
        self.moving_left = False    # 这里只是为了定义self.moving_right这个变量，而且定为false可以让它在开始时停止移动

    def update(self):
        """根据移动标志调整飞船的位置"""
        # 更新飞船而不是rect对象的x值
        if self.moving_right and self.rect.right < self.screen_rect.right:  # 保证飞船不飞出屏幕
            self.x += self.settings.ship_speed    # rect只能存储整数值
        if self.moving_left and self.rect.left > 0:    # 要是用elif则同时按左右键会只执行向右的命令
            self.x -= self.settings.ship_speed  # 对一个屏幕应该是从0往右算的

        # 根据self.x更新rect对象
        self.rect.x = self.x

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)