from .state import State
import pygame

_BLACK = (0, 0, 0)
_WHITE = (255, 255, 255)

class PlayState(State):
	def __init__(self, game):
		State.__init__(self, game)
		# Grid, Cross and Ellipse surfaces
		self.grid   = pygame.Surface((game.width, game.height))
		self.cross  = pygame.Surface((100, 100))
		self.circle = pygame.Surface((100, 100))

		# Clear surface with white
		for surface in [self.grid, self.cross, self.circle]: 
			surface.fill(_WHITE)

		# Draw grid
		for i in range(1, 3):
			j = i*120
			pygame.draw.line(self.grid, _BLACK, (10, j), (350, j), 10)
			pygame.draw.line(self.grid, _BLACK, (j, 10), (j, 350), 10)
		# Draw cross
		pygame.draw.line(self.cross, _BLACK, (20, 20), (80, 80), 10)
		pygame.draw.line(self.cross, _BLACK, (20, 80), (80, 20), 10)
		# Draw circle
		pygame.draw.circle(self.circle, _BLACK, (50, 50), 30, 8)
	def draw(self, screen):
		screen.blit(self.grid, (0, 0))
		for row in range(3):
			for col in range(3):
				cell = self.game.cell(row, col)
				if cell.empty(): continue
				x, y = col*120, row*120
				screen.blit(
					self.cross
					if cell.value == 'X'
					else self.circle, (10+x, 10+y)
				)
