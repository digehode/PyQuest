import pygame as pg
from pygame.locals import *
import random
import math


class Ship(pg.Rect):
        def __init__(self,x,y):
                pg.Rect.__init__(self,x,y,20,20)
                self.forceVect=[0,0]
                self.thrust=0.1
                
        def move(self,target):
                xdiff=target.left-self.left
                if xdiff>0:
                        xdiff=1
                elif xdiff<0:
                        xdiff=-1
                ydiff=target.top-self.top
                if ydiff>0:
                        ydiff=1
                elif ydiff<0:
                        ydiff=-1
                self.forceVect[0]+=xdiff*self.thrust
                self.forceVect[1]+=ydiff*self.thrust
                self.move_ip(self.forceVect)
        def draw(self,surf):
                surf.fill((255,0,0),rect=self)


class Projectile(pg.Rect):
        def __init__(self,x,y,w,h,a):
                pg.Rect.__init__(self,x,y,w,h)
                self.angle=a
                self.speed=10
                self.alive=True
        def move(self):
                self.move_ip(math.sin(math.radians(self.angle))*self.speed,
                             math.cos(math.radians(self.angle))*self.speed)
        def draw(self,surf):
                surf.fill((0,0,255),rect=self)

#Variables
screen_size=w,h=800,600

numShips=10
enemies=[]
for i in range(numShips):
        enemies.append(Ship(random.randint(0,w),random.randint(0,h)))



black=(0,0,0)
green=(0,100,0)
forceVect=[0,0]
speed=0.1
shallRun=True
linepos=[0,0,w,h]
shipAngle=0

#PyGame setup
pg.init()
screen = pg.display.set_mode(screen_size)
pg.display.set_caption("PyQuest")
clock = pg.time.Clock()
font1=pg.font.Font(None, 20)
ship=pg.image.load("ship.png").convert_alpha()
shipRect=ship.get_rect()
pg.mouse.set_visible(False)
pg.event.set_grab(True)
screen_rect=screen.get_rect()
energy=100
bullets=[]

def mag((a,b)):
        return (a**2+b**2)**0.5

while shallRun:
	screen.fill(black)
	pg.draw.aaline(screen, green, shipRect.center, linepos[2:])
	shipAngle=math.degrees(math.atan2(forceVect[0],forceVect[1]))
	tmpImg=pg.transform.rotate(ship,shipAngle)
	tmpRect=tmpImg.get_rect()
	tmpRect.center=shipRect.center
	screen.blit(tmpImg,tmpRect)
	
	
	mouseMove=pg.mouse.get_rel()
	
	forceVect[0]+=mouseMove[0]
	forceVect[1]+=mouseMove[1]
	shipRect=shipRect.move((forceVect[0]*speed,forceVect[1]*speed))

        for b in bullets:
                collides=b.collidelist(enemies)
                if collides>-1:
                   del enemies[collides]
                   b.alive=False
        bullets=filter(lambda x:x.alive,bullets)

        for i in enemies:
                i.move(shipRect)
                i.draw(screen)
        for i in bullets:
                i.move()
                i.draw(screen)
	
	if not screen_rect.contains(shipRect):
		shallRun=False
		print "YOU DEAD"
	t=font1.render("Foce vector: %d,%d"%(forceVect[0],forceVect[1]),True,green)
	
	screen.blit(t,(0,100))

        t=font1.render("Energy: %d"%(energy),True,green)
	screen.blit(t,(0,150))
	
	for i in range(len(linepos)):
		linepos[i]+=random.randint(-1,1)
	for e in pg.event.get():
		if e.type == QUIT:
			print "GOODBYE!"
			shallRun=False
		if e.type==KEYDOWN:
			if e.key == 113:
				shallRun=False
			elif e.key==32:
                                bullets.append(Projectile(shipRect.left,shipRect.top,5,5,shipAngle))
                                bullets[-1].speed+=mag(forceVect)*0.2
			else:
        			print "UNKNOWN KEY!",e.key
        		
	clock.tick(30)
	pg.display.flip()