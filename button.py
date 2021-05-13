import pygame.font  # 一个模块，用于将文本渲染到屏幕上

class Button:

    def __init__(self, ai_game, msg):   # msg是要在按钮中显示的文本
        """初始化按钮的属性"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # 设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)     # 亮绿色的按钮
        self.text_color = (255, 255, 255)   # 白色文本
        self.font = pygame.font.SysFont(None, 48)   # 指定字体，none代表默认字体，48代表字体大小

        # 创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 按钮的标签只需创建一次
        self._prep_msg(msg)     # 这个括号里的msg是内置函数或参数吧

    def _prep_msg(self, msg):
        """将msg渲染为图像，并使其在按钮上居中"""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        # font.render是将文本转换为图像，参数的True表示是否开启反锯齿功能
        self.msg_image_rect = self.msg_image.get_rect()  # 让文本图像在按钮上居中
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # 绘制一个用颜色填充的按钮，再绘制文本
        self.screen.fill(self.button_color, self.rect)  # screen.fill绘制表示按钮的矩形
        self.screen.blit(self.msg_image, self.msg_image_rect)   # screen.blit在屏幕上绘制文本图像