import pygame,math,sys,os
from pygame.locals import *
from random import randint

#class for the life sprite is the bottom right corner
class Lives(pygame.sprite.Sprite):
	def __init__(self,gs=None,pos=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.pos = pos

		self.image = pygame.image.load('Sprites/life.png')
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(self.pos,600)

#class for the floating objects in the river
class Floaters(pygame.sprite.Sprite):
	def __init__(self,gs=None, number=None,pos=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.number = number

		#images of the objects
		self.objects = ['Sprites/small_log.png','Sprites/seal.png','Sprites/medium_log.png','Sprites/close_gator.png','Sprites/long_log.png','Sprites/turtle1.png']
		self.pos = [270, 225, 185,145,105,70]
		self.speed = [-1.4,1.6,-1.2,1.8,-1.6,1.75]
		self.count = 1
		self.gators = {1:'Sprites/close_gator.png',-1:'Sprites/open_gator.png'}
		#loading image
		self.image = pygame.image.load(self.objects[number])
		self.rect = self.image.get_rect()
		if self.number == 5:
			self.rect = self.rect.move(-50+pos,self.pos[number])
		elif self.number % 2 == 0:
			self.rect = self.rect.move(640, self.pos[number])
		else:
			self.rect = self.rect.move(-10, self.pos[number])

	def tick(self,counter=None):

		if self.number == 5:
			if (counter % 60) / 3 == 0:
				self.image = pygame.image.load('Sprites/turtle1.png')
			if (counter % 60) / 3 == 4:
				self.image = pygame.image.load('Sprites/turtle2.png')
			if (counter % 60) /4 == 8:
				self.image = pygame.image.load('Sprites/turtle3.png')

		if self.number == 3:
			if counter % 100 == 0:
				self.image = pygame.image.load(self.gators[self.count])
				self.count = self.count * -1
		self.rect = self.rect.move(self.speed[self.number],0)

#class for the cars
class Cars(pygame.sprite.Sprite):
	def __init__(self, gs=None, number=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.number = number

		#cars image and location list
		self.cars = ['Sprites/left_car1.png','Sprites/right_car1.png','Sprites/left_car2.png','Sprites/right_car2.png','Sprites/left_car1.png']
		self.pos = [550,510,450,410,350]
		self.speed = [1.5,1.1,1.6,1.3,2]

		#loading image
		self.image = pygame.image.load(self.cars[number])
		self.rect = self.image.get_rect()
		if self.number % 2 == 0:
			self.rect = self.rect.move(640, self.pos[number])
		else:
			self.rect = self.rect.move(-10, self.pos[number])

	def tick(self):
		if self.number % 2 == 0:
			self.rect = self.rect.move(-1*self.speed[self.number],0)
		else:
			self.rect = self.rect.move(self.speed[self.number],0)

#class for frogger
class Player(pygame.sprite.Sprite):
	def __init__(self, gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.image = pygame.image.load("Sprites/up_still.png")
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(320,600)

		#sprite movement dictionaries
		self.image_up = {1:"Sprites/up_still.png", -1:"Sprites/up_move.png"}
		self.image_down = {1:"Sprites/down_still.png", -1:"Sprites/down_move.png"}
		self.image_right = {1:"Sprites/right_still.png", -1:"Sprites/right_move.png"}
		self.image_left = {1:"Sprites/left_still.png", -1:"Sprites/left_move.png"}

		#sprite movement counts
		self.up_count = 1
		self.down_count = 1
		self.right_count = 1
		self.left_count = 1
		self.timer = 0

	def tick(self):
		if self.gs.pressed["right"] == True:
			self.rect = self.rect.move(5,0)
			self.image = pygame.image.load(self.image_right[self.right_count])
			#chaning the sprites
			if self.timer % 3 == 0:
				self.right_count = self.right_count * -1
		if self.gs.pressed["left"] == True:
			self.rect = self.rect.move(-5,0)
			self.image = pygame.image.load(self.image_left[self.left_count])
			#changing the sprites
			if self.timer % 3 == 0:
				self.left_count = self.left_count * -1
		if self.gs.pressed["up"] == True:
			self.rect = self.rect.move(0,-5)
			self.image = pygame.image.load(self.image_up[self.up_count])
			#changing the sprite
			if self.timer % 2 == 0:
				self.up_count = self.up_count * -1
		if self.gs.pressed["down"] == True:
			self.rect = self.rect.move(0,5)
			self.image = pygame.image.load(self.image_down[self.down_count])
			#chaning the sprite
			if self.timer % 2 == 0:
				self.down_count = self.down_count * -1


		#increment counter
		self.timer = self.timer + 1

class GameSpace:

	def player_hit(self,car):
		if self.player.rect.colliderect(car.rect):
			self.player.rect = self.player.image.get_rect()
			self.player.rect = self.player.rect.move(320,580)
			self.lives = self.lives - 1
			self.lives_list.pop()

	def player_float(self,obj):
		if self.player.rect.colliderect(obj.rect):
			self.player.rect = self.player.rect.move(obj.speed[obj.number],0)

	def inbounds(self,car,lst):
		if car.rect[0] >= -100 and car.rect[0] <= 650:
			lst.append(car)

	def game_screen(self):
		pygame.init()
		self.size = self.width, self.height = 640,640
		self.bg = pygame.image.load("Sprites/background.png")
		self.go = pygame.image.load("Sprites/game_over.jpg")
		self.black = 0,0,0

		#variables for object generation
		self.object_list = []
		self.temp_object = []

		#variables for car generation
		self.counter = 0
		self.car_list = []
		self.temp_car = []

	def frog_start(self):
		#creating lives image
		self.lives_list = []
		self.lives_list.append(Lives(self,560))
		self.lives_list.append(Lives(self,580))
		self.lives_list.append(Lives(self,600))

		#creating game objects
		self.player = Player(self)
		self.score = 0

		#setting up screen
		self.screen = pygame.display.set_mode(self.size)
		self.clock = pygame.time.Clock()

		#gameplay variables
		self.lives = 3

	def wait(self):
		while True:
			event = pygame.event.wait()
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN and event.key == K_y:
				break

	def frog_restart(self):
		self.lives = 3

		#creating lives image
		self.lives_list = []
		self.lives_list.append(Lives(self,560))
		self.lives_list.append(Lives(self,580))
		self.lives_list.append(Lives(self,600))

		self.pressed = {"up":False, "down":False, "right":False, "left":False}


		self.screen.fill(self.black)
		self.screen.blit(self.go,(0,0))

		pygame.display.flip()

		self.wait()

	def main(self):

		self.game_screen()

		self.frog_start()

		#pressed keys
		self.pressed = {"up":False, "down":False, "right":False, "left":False}

		#starting game loop
		while 1:
			#handle user inputs
			for event in pygame.event.get():
				if event.type == QUIT:
					sys.exit()

				if event.type == KEYDOWN:
					if(event.key == pygame.K_RIGHT):
						self.pressed['right'] = True
					if(event.key == pygame.K_LEFT):
						self.pressed['left'] = True
					if(event.key == pygame.K_UP):
						self.pressed['up'] = True
					if(event.key == pygame.K_DOWN):
						self.pressed['down'] = True

				if event.type == KEYUP:
					if(event.key == pygame.K_RIGHT):
						self.pressed['right'] = False
					if(event.key == pygame.K_LEFT):
                        			self.pressed['left'] = False
					if(event.key == pygame.K_UP):
                        			self.pressed['up'] = False
					if(event.key == pygame.K_DOWN):
                        			self.pressed['down'] = False

			#generating Cars
			if self.counter % 40 == 0:
				if randint(0,5) == 0:
					self.car_list.append(Cars(self,0))
			if self.counter % 40 == 0:
				if randint(0,5) == 1:
					self.car_list.append(Cars(self,1))
			if self.counter % 40 == 0:
				if randint(0,5) == 0:
					self.car_list.append(Cars(self,2))
			if self.counter % 80 == 0:
				if randint(0,5) == 0:
					self.car_list.append(Cars(self,3))
			if self.counter % 40 == 0:
				if randint(0,5) == 0:
					self.car_list.append(Cars(self,4))

			#generating objects:
			if self.counter % 200 == 0:
				self.object_list.append(Floaters(self,0))
				self.object_list.append(Floaters(self,3))
			if self.counter % 110 == 0:
				self.object_list.append(Floaters(self,1))
			if self.counter % 225 == 0:
				self.object_list.append(Floaters(self,2))
			if self.counter % 300 == 0:
				self.object_list.append(Floaters(self,4))
			if self.counter % 150 == 0:
				self.object_list.append(Floaters(self,5,0))
				self.object_list.append(Floaters(self,5,40))
				self.object_list.append(Floaters(self,5,80))

			#Clock and Object ticks
			self.clock.tick(60)
			self.player.tick()
			# print self.player.rect[1]
			for car in self.car_list:
				car.tick()
				self.inbounds(car,self.temp_car)
				self.player_hit(car)

			if self.lives == 0:
				self.frog_restart()

			for obj in self.object_list:
				obj.tick(self.counter)
				self.inbounds(obj,self.temp_object)
				if self.player.rect[1] <=280:
					self.player_float(obj)

			if self.player.rect[1] <= 280 and self.player.rect[1] >= 50:
				if self.player.rect.collidelist(self.object_list) == -1:
					self.lives = self.lives - 1
					self.lives_list.pop()
					self.player.rect = self.player.image.get_rect()
					self.player.rect = self.player.rect.move(320,590)

			if self.player.rect[1] < 50:
				self.score += 1
				self.player.rect = self.player.image.get_rect()
				self.player.rect = self.player.rect.move(320,590)


			#clearing the off screen cars
			self.car_list = self.temp_car
			self.temp_car = []

			#clearing off screen floaters
			self.object_list = self.temp_object
			self.temp_object = []

			self.counter = self.counter + 1
			#send tick to game objects

			#display
			self.screen.fill(self.black)
			self.screen.blit(self.bg,(0,0))

			for car in self.car_list:
				self.screen.blit(car.image,car.rect)

			for obj in self.object_list:
				self.screen.blit(obj.image,obj.rect)

			for life in self.lives_list:
				self.screen.blit(life.image,life.rect)

			self.screen.blit(self.player.image, self.player.rect)

			pygame.display.flip()


if __name__ == '__main__':
	gs = GameSpace()
	gs.main()
