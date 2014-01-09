# -*- coding:utf-8 -*-
import pygame
import random
from sys import exit

# 定义一个Bullet类，封装子弹相关数据和方法
class Bullet:
    def __init__(self):
        self.x = 0
        self.y = -1
        self.image = pygame.image.load('bullet.png').convert_alpha()
        #默认不激活
        self.active = False

    def move(self):
        #激活状态下，向上移动
        if self.active:
            self.y -= 3
        #当飞出屏幕，就设为不激活
        if self.y < 0:
            self.active = False

    def restart(self):
        #重置子弹位置
        mouseX, mouseY = pygame.mouse.get_pos()
        self.x = mouseX - self.image.get_width() / 2
        self.y = mouseY - self.image.get_height() / 2
        #激活子弹
        self.active = True
        
# 定义一个Enemy类，封装敌人相关数据和方法
class Enemy:
    def restart(self):
        # 重置敌机位置和速度
        self.x = random.randint(50, 400)
        self.y = random.randint(-200, -50)
        self.speed = random.random() + 0.1

    def __init__(self):
        # 初始化
        self.restart()
        self.image = pygame.image.load('enemy.png').convert_alpha()

    def move(self):
        if self.y < 800:
            # 向下移动
            self.y += self.speed
        else:
            # 重置
            self.restart()

pygame.init()
screen = pygame.display.set_mode((450, 800), 0, 32)
pygame.display.set_caption('Hello, world of pygame')
background = pygame.image.load('back.jpg').convert()
plane = pygame.image.load('plane.png').convert_alpha()
#创建子弹的list
bullets = []
#向list中添加5发子弹
for i in range(5):
    bullets.append(Bullet())
#子弹总数
count_b = len(bullets)
#即将激活的子弹序号
index_b = 0
#发射子弹的间隔
interval_b = 0
# 创建敌机
enemies = []
for i in range(5):
    enemies.append(Enemy())
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.blit(background, (0, 0))
    #发射间隔递减
    interval_b -= 1
    #当间隔小于0时，激活一发子弹
    if interval_b < 0:
        bullets[index_b].restart()
        #重置间隔时间
        interval_b = 100
        #子弹序号周期性递增
        index_b = (index_b + 1) % count_b
    #判断每个子弹的状态
    for b in bullets:
        #处于激活状态的子弹，移动位置并绘制
        if b.active:
            b.move()
            screen.blit(b.image, (b.x, b.y))
    for e in enemies:
        e.move()
        screen.blit(e.image, (e.x, e.y))
    x, y = pygame.mouse.get_pos()
    x -= plane.get_width() / 2
    y -= plane.get_height() / 2
    screen.blit(plane, (x, y))
    pygame.display.update()
    
