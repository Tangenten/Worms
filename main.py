import math
import random
import numpy
import pygame

class graphicHandler:
	
	def __init__(self):
		pygame.init()
		pygame.display.set_caption("Worms")
		
		self.clock = pygame.time.Clock()
		self.width = 920
		self.height = 920
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.deltaTime = 0
		self.running = False
		
		self.swimmers = swimmers(self.width, self.height)
		
	def start(self):
		self.render()
	
	def stop(self):
		self.running = False
		
	def render(self):
		self.running = True
		while self.running:
			self.screen.fill((0, 0, 0))
			self.deltaTime = 0.016 if self.deltaTime == 0.0 else self.clock.get_time() / 1000
			
			swimmerPoints = self.swimmers.getSwimmerPoints()
			
			for point in swimmerPoints:
				i = self.swimmers.trailPointer % point[4]
				for trailPoint in point[3]:
					i += 1
					
					scalar = numpy.interp(i % point[4], [0, point[4]], [0,1])
					color = (point[1] * scalar).astype(int)
					pygame.draw.rect(self.screen, color, [trailPoint, point[2]])
				pygame.draw.rect(self.screen, [255, 255, 255], [point[0], point[2]])
			
			pygame.display.flip()
			self.clock.tick(60)
			self.input()
			self.swimmers.update()
	
	def input(self):
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				self.stop()
				pygame.quit()
		
class swimmers():
	def __init__(self, width, height):
		self.width = width
		self.height = height
		
		self.ringBufferSize = 256
		self.writePointer = 0
		
		self.trailPointer = 0
		
		pos = numpy.asarray([0,0])
		color = numpy.asarray([0, 0, 0])
		size = numpy.asarray([0, 0])
		trails = numpy.asarray([[0, 0]] * 0)
		trailLength = 0
		velocity = 0
		radian = 0
		
		self.swimmers = numpy.asarray([[pos, color, size, trails, trailLength, velocity, radian]] * self.ringBufferSize)

		self.insertSwimmers(self.ringBufferSize)
		
	def update(self):
		tp = self.trailPointer
		for i in range(len(self.swimmers)):
			# swimmer[0] [x ,y] coordinates
			# swimmer[1] [r, g, b, a] color
			# swimmer[2] size
			# swimmer[3] trail [[x, y]]
			# swimmer[4] trail length
			# swimmer[5] velocity
			# swimmer[6] radian
			
			if self.swimmers[i][5] <= 1:
				pass
			else:
				
				self.swimmers[i][0][0] += self.swimmers[i][5] * math.cos(self.swimmers[i][6])
				self.swimmers[i][0][1] += self.swimmers[i][5] * math.sin(self.swimmers[i][6])
				
				self.swimmers[i][5] -= 0.0005
				self.swimmers[i][6] += random.uniform(-0.4, 0.4)
				
				if self.swimmers[i][0][0] < 0:
					if math.sin(self.swimmers[i][6]) > 0:
						self.swimmers[i][6] = math.acos(-math.cos(self.swimmers[i][6]))
					else:
						self.swimmers[i][6] = -math.acos(-math.cos(self.swimmers[i][6]))
					self.swimmers[i][0][0] = 0
				elif self.swimmers[i][0][0] > self.width:
					if math.sin(self.swimmers[i][6]) > 0:
						self.swimmers[i][6] = math.acos(-math.cos(self.swimmers[i][6]))
					else:
						self.swimmers[i][6] = -math.acos(-math.cos(self.swimmers[i][6]))
					self.swimmers[i][0][0] = self.width
				elif self.swimmers[i][0][1] < 0:
					if math.cos(self.swimmers[i][6]) > 0:
						self.swimmers[i][6] = math.asin(-math.sin(self.swimmers[i][6]))
					else:
						self.swimmers[i][6] = math.acos(math.sin(self.swimmers[i][6]))
					self.swimmers[i][0][1] = 0
				elif self.swimmers[i][0][1] > self.height:
					if math.cos(self.swimmers[i][6]) > 0:
						self.swimmers[i][6] = math.asin(-math.sin(self.swimmers[i][6]))
					else:
						self.swimmers[i][6] = -math.acos(-math.sin(self.swimmers[i][6]))
					self.swimmers[i][0][1] = self.height
					
				
			self.swimmers[i][3][tp % self.swimmers[i][4]] = [self.swimmers[i][0][0], self.swimmers[i][0][1]]
		
		self.trailPointer += 1

			
	def insertSwimmers(self, n):
		for i in range(n):
			position = numpy.asarray([self.width // 2, self.height // 2])
			color = numpy.asarray(list(numpy.random.choice(range(256), size = 3)))
			size = numpy.asarray(list(numpy.random.choice(range(1, 8), size = 2)))
			trailLength = random.randint(1, 32)
			trails = numpy.asarray([[self.width // 2, self.height // 2]] * trailLength)
			movementVelocity = random.uniform(2,4)
			movementDirection = random.uniform(0, 2 * math.pi) # radian

			self.swimmers[self.writePointer % self.ringBufferSize] = [position, color, size, trails, trailLength, movementVelocity, movementDirection]
			self.writePointer += 1
			
	def getSwimmerPoints(self):
		return self.swimmers[:, :5]
		
if __name__ == '__main__':
	g = graphicHandler()
	g.start()
