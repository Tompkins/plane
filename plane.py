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

class Plane:
    def restart(self):
        self.x = 200
        self.y = 600

    def __init__(self):
        self.restart()
        self.image = pygame.image.load('plane.png').convert_alpha()

    def move(self):
        x, y = pygame.mouse.get_pos()
        x -= self.image.get_width() / 2
        y -= self.image.get_height() / 2
        self.x = x
        self.y = y

def checkHit(enemy, bullet):
    if (bullet.x > enemy.x and bullet.x < enemy.x + enemy.image.get_width()) \
       and (bullet.y > enemy.y and bullet.y < enemy.y + enemy.image.get_height()):
        # 重置敌机
        enemy.restart()
        # 重置子弹
        bullet.active = False
        # 增加返回值
        return True
    return False

def checkCrash(enemy, plane):
    if (plane.x + 0.7*plane.image.get_width() > enemy.x) and (plane.x + 0.3*plane.image.get_width() \
        < enemy.x + enemy.image.get_width()) and (plane.y + 0.7*plane.image.get_height() \
        > enemy.y) and (plane.y + 0.3*plane.image.get_height() < enemy.y + enemy.image.get_height()):
        return True
    return False

pygame.init()
screen = pygame.display.set_mode((450, 800), 0, 32)
pygame.display.set_caption('Hello, world of pygame')
background = pygame.image.load('back.jpg').convert()
plane = Plane()
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
gameover = False
score = 0
font = pygame.font.Font(None, 32)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        #判断在gameover状态下点击鼠标
        if gameover and event.type == pygame.MOUSEBUTTONUP:
            # 重置游戏
            plane.restart()
            for e in enemies:
                e.restart()
            for b in bullets:
                b.active = False
            score = 0
            gameover = False
    screen.blit(background, (0, 0))
    if not gameover:
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
                # 检测每一颗active的子弹是否与enemy碰撞
                for e in enemies:
                    if checkHit(e, b):
                        score += 100                        
                b.move()
                screen.blit(b.image, (b.x, b.y))
        for e in enemies:
            if checkCrash(e, plane):
                gameover = True
            e.move()
            screen.blit(e.image, (e.x , e.y))
        plane.move()
        screen.blit(plane.image, (plane.x, plane.y))
        #在屏幕左上角显示分数
        text = font.render("Socre: %d" % score, 1, (0, 0, 0))
        screen.blit(text, (0, 0))
    else:
        #在屏幕中央显示分数
        text = font.render("Score: %d" % score, 1, (0, 0, 0))
        screen.blit(text, (190, 400))
    pygame.display.update()
    
