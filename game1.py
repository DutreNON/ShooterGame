import pygame as pg
import math
from random import randint

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Hero():
    def __init__(self, size: tuple, offset: int, color: tuple) -> None:
        self.orig_image = pg.Surface(size)
        self.orig_image.fill(color)
        self.orig_image.set_colorkey(BLACK)
        self.image = self.orig_image
        self.a, self.b = map(lambda i: i/2, self.image.get_rect().size)
        self.min_x, self.max_x = 0, scr.get_width() - 2*self.a
        self.min_y, self.max_y = 0, scr.get_height() - 2*self.b          
        self.x, self.y = scr.get_width()/2 - self.a, scr.get_height()/2 - self.b
        self.offset = offset

    def update(self) -> None:
        if pg.mouse.get_focused(): 
            old_center_x, old_center_y = self.x + self.a, self.y + self.b
            self.image = pg.transform.rotate(self.orig_image, math.degrees(math.atan2(mouse_x - (self.x + self.a), mouse_y - (self.y + self.b))))
            self.a, self.b = map(lambda i: i/2, self.image.get_rect().size)
            self.min_x, self.max_x = 0, scr.get_width() - 2*self.a
            self.min_y, self.max_y = 0, scr.get_height() - 2*self.b            
            self.x, self.y = old_center_x - self.a, old_center_y - self.b
        if keys[pg.K_w]: self.y -= self.offset
        if keys[pg.K_s]: self.y += self.offset
        if keys[pg.K_a]: self.x -= self.offset
        if keys[pg.K_d]: self.x += self.offset
        if self.x < self.min_x: self.x = self.min_x
        elif self.x > self.max_x: self.x = self.max_x
        if self.y < self.min_y: self.y = self.min_y
        elif self.y > self.max_y: self.y = self.max_y  
              
    def fire(self) -> None:
        if pg.mouse.get_focused(): bullets.append(Bullet((5, 20), 30, YELLOW))

class Bullet():
    def __init__(self, size: tuple, offset: int, color: tuple) -> None:
        self.orig_image = pg.Surface(size)
        self.orig_image.fill(color)
        self.orig_image.set_colorkey(BLACK)
        vec_x, vec_y = mouse_x - (hero.x + hero.a), mouse_y - (hero.y + hero.b)
        sqrt = math.sqrt(vec_x**2 + vec_y**2)
        self.off_x, self.off_y = 0, 0
        if sqrt: self.off_x, self.off_y = vec_x / sqrt * offset, vec_y / sqrt * offset  
        self.image = pg.transform.rotate(self.orig_image, math.degrees(math.atan2(vec_x, vec_y)))
        self.a, self.b = map(lambda i: i/2, self.image.get_rect().size)
        self.min_x, self.max_x = -2*self.a, scr.get_width() 
        self.min_y, self.max_y = -2*self.b, scr.get_height()   
        self.x, self.y = (hero.x + hero.a) - self.a, (hero.y + hero.b) - self.b  

    def update(self) -> None:
        self.x += self.off_x
        self.y += self.off_y
        if self.x < self.min_x or self.x > self.max_x or self.y < self.min_y or self.y > self.max_y: bullets.remove(self)

class Enemy():
    def __init__(self, size: tuple, offset: int, color: tuple) -> None:
        self.orig_image = pg.Surface(size)
        self.orig_image.fill(color)
        self.orig_image.set_colorkey(BLACK)
        self.image = self.orig_image
        self.offset = offset
        self.a, self.b = map(lambda i: i/2, self.image.get_rect().size)
        max_rect = round(math.sqrt(2)*(self.a + self.b))
        self.min_x, self.max_x = -max_rect, scr.get_width() 
        self.min_y, self.max_y = -max_rect, scr.get_height()      
        self.x, self.y = self.randpos()
        vec_x, vec_y = (hero.x + hero.a) - (self.x + self.a), (hero.y + hero.b) - (self.y + self.b)
        sqrt = math.sqrt(vec_x**2 + vec_y**2)
        self.off_x, self.off_y = 0, 0
        if sqrt: self.off_x, self.off_y = vec_x / sqrt * self.offset, vec_y / sqrt * self.offset  
        old_center_x, old_center_y = self.x + self.a, self.y + self.b
        self.image = pg.transform.rotate(self.orig_image, math.degrees(math.atan2(vec_x, vec_y)))
        self.a, self.b = map(lambda i: i/2, self.image.get_rect().size)  
        self.x, self.y = old_center_x - self.a, old_center_y - self.b   

    def randpos(self) -> tuple: 
        side = randint(0, 1)
        if side: 
            x = randint(self.min_x, self.max_x)
            side = randint(0, 1)
            y = self.max_y if side else self.min_y
        else:
            y = randint(self.min_y, self.max_y)
            side = randint(0, 1)
            x = self.max_x if side else self.min_x
        return (x, y)
    
    def update(self) -> None:
        self.x += self.off_x
        self.y += self.off_y
        kill = False
        if collide(self, hero): kill = True
        for bullet in bullets: 
            if collide(self, bullet):
                bullets.remove(bullet)
                kill = True
        if self.off_x < 0:  
            if self.x < self.min_x: kill = True 
        else:
            if self.x > self.max_x: kill = True 
        if self.off_y < 0:  
            if self.y < self.min_y: kill = True   
        else:
            if self.y > self.max_y: kill = True  
        if kill:
            self.x, self.y = self.randpos()
            vec_x, vec_y = (hero.x + hero.a) - (self.x + self.a), (hero.y + hero.b) - (self.y + self.b)
            sqrt = math.sqrt(vec_x**2 + vec_y**2)
            self.off_x, self.off_y = 0, 0
            if sqrt: self.off_x, self.off_y = vec_x / sqrt * self.offset, vec_y / sqrt * self.offset  
            old_center_x, old_center_y = self.x + self.a, self.y + self.b
            self.image = pg.transform.rotate(self.orig_image, math.degrees(math.atan2(vec_x, vec_y)))
            self.a, self.b = map(lambda i: i/2, self.image.get_rect().size)  
            self.x, self.y = old_center_x - self.a, old_center_y - self.b 

def collide(obj1: object, obj2: object) -> bool: 
    return True if (obj2.x <= obj1.x <= obj2.x + 2*obj2.a or obj1.x <= obj2.x <= obj1.x + 2*obj1.a) and (obj2.y <= obj1.y <= obj2.y + 2*obj2.b or obj1.y <= obj2.y <= obj1.y + 2*obj1.b) else False

def blit(obj: object) -> None: 
    scr.blit(obj.image, (obj.x, obj.y))

scr = pg.display.set_mode((1500, 750))
pg.display.set_caption('game')

bullets = list()
hero = Hero((20, 20), 5, WHITE)
enemies = list()
for i in range(0, 5): enemies.append(Enemy((20, 20), 3, RED))

stop = 0
while 1:
    scr.fill(BLACK)
    mouse_x, mouse_y = pg.mouse.get_pos()
    keys = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT or (keys[pg.K_LCTRL] and keys[pg.K_c]): stop = 1
        elif event.type == pg.MOUSEBUTTONDOWN: hero.fire() 
    if stop: break
    hero.update()
    for bullet in bullets: 
        bullet.update()  
        blit(bullet) 
    for enemy in enemies: 
        enemy.update()  
        blit(enemy)           
    blit(hero) 
    pg.display.update()
    pg.time.Clock().tick(60)