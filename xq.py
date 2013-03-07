from pygame.locals import *
import random
import math

#Variables
screen_size=w,h=800,600
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


while shallRun:
	screen.fill(black)
	pg.draw.aaline(screen, green, shipRect.center, linepos[2:])
	shipAngle=math.degrees(math.atan2(forceVect[0],forceVect[1]))+180
	tmpImg=pg.transform.rotate(ship,shipAngle)
	tmpRect=tmpImg.get_rect()
	tmpRect.center=shipRect.center
	screen.blit(tmpImg,tmpRect)
	
	
	mouseMove=pg.mouse.get_rel()
	
	forceVect[0]+=mouseMove[0]
	forceVect[1]+=mouseMove[1]
	shipRect=shipRect.move((forceVect[0]*speed,forceVect[1]*speed))
	
	if not screen_rect.contains(shipRect):
		shallRun=False
		print "YOU DEAD"
	t=font1.render("Foce vector: %d,%d"%(forceVect[0],forceVect[1]),True,green)
	
	screen.blit(t,(0,100))
	for i in range(len(linepos)):
		linepos[i]+=random.randint(-1,1)
	for e in pg.event.get():
		if e.type == QUIT:
			print "GOODBYE!"
			shallRun=False
		if e.type==KEYDOWN:
			if e.key == 113:
				shallRun=False
			else:
				print "UNKNOWN KEY!",e.key
	clock.tick(30)
	pg.display.flip()
