import sys  # sys模块包含了与Python解释器和它的环境有关的函数。
from time import sleep      # time是python标准库,sleep()函数可以让游戏暂停

import pygame   # 导入游戏显示的包


from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship   # 头部写完后最好隔两行再写类
from bullet import Bullet  # 导入Buttle类
from alien import Alien  # 导入外星人


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()   # 对库进行初始化
        self.settings = Settings()  # 导入类时注意后面的括号，有个bug就是在这产生的
        # 游戏全屏的操作
        # self.screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # display.set_mode是显示尺寸的函数
        pygame.display.set_caption("Alien Invasion")
        # display.set_caption是在游戏上方显示的字体相当于游戏名吧

        # 创建一个用于存储游戏统计信息的实例
        # 并创建记分牌
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        # 因为Ship类导入了pygame吧，所以后面才带个括号里面有self
        self.bullets = pygame.sprite.Group()    # pygame.sprite.Group是pygame的一个函数，功能类似于列表
        self.aliens = pygame.sprite.Group()  # 创建一个用于存储外星人群的编组

        self._create_fleet()

        # 创建play按钮
        self.play_button = Button(self, "play")     # "play"则是文本，即msg

        # 设置背景色
        self.bg_color = (230,230,230)   # 这里的数值代表颜色，不用太在意

    def _create_fleet(self):
        """创建外星人群"""
        # 创建一个外星人并计算一行可容纳多少个外星人
        # 外星人的间距为外星人的宽度
        alien = Alien(self)     # Alien是alien函数里的类,创建一个外星人，但它不是外星人群的成员
        alien_width, alien_height = alien.rect.size     # size是方法
        available_space_x = self.settings.screen_width - (2 * alien_width)  # 外星人的间距为外星人的宽度
                                                                            # 计算水平空间和一行内可容纳外星人数目
        numbers_aliens_x = available_space_x // (2 * alien_width)   # //是相除抛弃余数

        # 计算屏幕可容纳多少行外星人
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)  # 这个3中1是第一行外星人与上方的空白，二是飞船与外星人空白，
                                                                # 方便飞船射击
        number_rows = available_space_y // (2 * alien_height)

        # 创建外星人群
        for row_number in range(number_rows):
            # 创建一行外星人
            for alien_number in range(numbers_aliens_x):  # range是类
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """创建一个外星人并将其加入当前行"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size     # size 是方法,是一个元组，里面有对象的高度和宽度
        alien.x = alien_width + 2 * alien_width * alien_number  # 计算水平空间和一行内可容纳外星人数目
        alien.rect.x = alien.x  # 通过设置x坐标将其加入当前行，自己debug几次就清楚逻辑了
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        # 在第一行上方留出外星人等高的空白，每个外星人y方向距离一个外星人的高度，所以乘2
        self.aliens.add(alien)  # 将新创建的外星人加到编组里

    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():     # sprites是方法
        # 遍历外星人群并对每个外星人调用check_edges()
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群外星人下移，并改变他们的方向"""
        # 遍历所有外星人，将每个外星人下移设置fleet_drop_speed的值
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def run_game(self):
        """开始游戏的主循环"""
        while True: # 保证游戏的持续进行
            self._check_events()    # 监视键盘和鼠标事件

            if self.stats.game_active:
                self.ship.update()  # Ship类中的一个函数，令飞船移动位置
                self._update_bullets()   # 子弹的更新
                self._update_aliens()

            self._update_screen()   # 在游戏运行时时刻更新屏幕

    def _check_events(self):
        # 监视键盘和鼠标事件
        for event in pygame.event.get():    # pygame.event.get（）是获得当前用户操作的事件列表
            if event.type == pygame.QUIT:   # 检测用户是否点击退出键
                    sys.exit()  # 结束程序的代码
            elif event.type == pygame.KEYDOWN:  # KEYDOWN是用户按键的输入，每次按键都被注册为一个KEYDOMS事件
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:    # KEYUP为用户松开按键
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # pygame.mouse.get_pos返回一个元组，包含单击时鼠标的x和y坐标
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """在玩家单击play按钮时开始游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        # rect的方法collidepoint检查鼠标单击位置是否在play按钮的rect内
        if button_clicked and not self.stats.game_active:
            # 重置游戏设置
            self.settings.initialize_dynamic_settings()
            # initialize_dynamic_settings这个方法有点奇怪

            # 重置游戏统计信息
            self.stats.reset_stats()    # reset_stats是重置游戏统计信息
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人并让飞船居中
            self._create_fleet()
            self.ship.center_ship()

            # 隐藏鼠标光标
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """响应按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:   # 按q可退出游戏
            sys.exit()  # 前面那个sys要不要都可以
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """响应松开"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullet中"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)   # 创建一个BUllet实例并将其赋给new_bullet
            self.bullets.add(new_bullet)    # add是系统自带的方法，这里是将新子弹加入编组bullets中

    def _update_screen(self):
        # 每次循环时都重绘屏幕
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)   # draw是一个方法

        # 显示得分
        self.sb.show_score()

        # 如果游戏处于非活动状态，就绘制play按钮
        if not self.stats.game_active:
            self.play_button.draw_button()

        # 让最近绘制的屏幕可见
        pygame.display.flip()
        # pygame.display.flip这也是pygame的一个函数

    def _update_bullets(self):
        """更新子弹位置并删除消失的子弹"""
        # 更新子弹位置
        self.bullets.update()
        # 删除消失的子弹，因为子弹飞出后仍存在，要删除它节省内存
        # 若子弹的rect的bottom属性为0则表明子弹已飞过屏幕顶端
        for bullet in self.bullets.copy():  # copy是系统的一个函数
            # copy是深复制，就是复制了原对象里面的所有对象，比如原对象是个字典里的字典，
            # 则浅复制改动字典的值不影响原对象，但改字典里的字典会影响原对象
            # 而深复制是复制原对象的所有对象，包括字典的字典，改动其对原对象无影响
            # python中可变对象传引用（如字典，列表），不可变对象传值（如数字，字符串）
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)  # remove是系统的方法

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人碰撞"""
        # 检查是否有子弹击中了外星人
        # 如果是，就删除相应的子弹和外星人
        # sprite.groupcollide是pygame的一个函数,用来将2个rect进行比较生成字典，键为子弹，值为alien
        # 前面两个是删除对象，后面的true代表删除操作，改为flase则不会被删除
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                # 一个子弹可能会击中多个敌人，所以有len
            self.sb.prep_score()    # 更新得分
            self.sb.check_high_score()

        if not self.aliens:
            # 删除现有的子弹并新建一群外星人,if not 这个有点nb
            self.bullets.empty()    # 删除当前所有子弹，虽然不知道有什么用
            self._create_fleet()    # _create_fleet是一个方法,重新显示一群外星人
            self.settings.increase_speed()

            # 提高等级
            self.stats.level += 1
            self.sb.prep_level()


    def _update_aliens(self):
        """检查是否有外星人位于屏幕边缘，并更新整群外星人位置"""
        self._check_fleet_edges()
        # 对编组调用方法update()，这将自动对每个外星人调用方法update()
        self.aliens.update()

        # 检测外星人和飞船之间的碰撞
        # sprite.spritecollideany是pygame的函数，接受一个精灵一个编组，时刻遍历编组，检查2者是否发生碰撞，若是则返回与
        # 精灵碰撞的成员且停止遍历编组，反之返回none
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检查是否有外星人到达了屏幕底端
        self._check_aliens_bottom()

    def _ship_hit(self):
        """响应外星飞船被外星人撞倒"""

        if self.stats.ships_left > 0:
            # 将ship_left减1并更新记分牌
            self.stats.ships_left -= 1  # 将余下飞船数减1
            self.sb.prep_ships()    # 更新记分牌

            # 清空余下的外星人和子弹
            self.aliens.empty()     # empty是方法
            self.bullets.empty()

            # 创建一群新的外星人，并将飞船放到屏幕底部的中央
            self._create_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(0.9)  # sleep是功能函数
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)  # 游戏结束后重新显示play光标

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底端"""
        screen_rect = self.screen.get_rect()    # self.screen.get_rect是整个屏幕的大小
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:     # 到达屏幕底部
                # 像飞船被撞到一样处理
                self._ship_hit()
                break


if __name__ == '__main__':
    # 创建游戏实例并运行游戏，这个代码还是要背的

    ai = AlienInvasion()    # AlienInvasion是个类，一个类不包括函数在内的其他代码若含self则后面要放self

    ai.run_game()








