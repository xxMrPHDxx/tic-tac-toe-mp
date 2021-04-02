from .state import State
import pygame

_BLACK = (0, 0, 0)
_WHITE = (255, 255, 255)

class PlayState(State):
	def __init__(self, game):
		State.__init__(self, game)

		# Clear the grid
		game.clear_grid()

		# Grid, Cross and Ellipse surfaces
		self.grid   = pygame.Surface((game.width, game.height))
		self.cross  = pygame.Surface((100, 100))
		self.circle = pygame.Surface((100, 100))

		# Clear surface with white
		for surface in [self.grid, self.cross, self.circle]: 
			surface.fill(_WHITE)

		# Static tic-tac-toe grid
		for i in range(1, 3):
			j = i*120
			pygame.draw.line(self.grid, _BLACK, (10, j), (350, j), 10)
			pygame.draw.line(self.grid, _BLACK, (j, 10), (j, 350), 10)
		
		# Static 'X' surface
		pygame.draw.line(self.cross, _BLACK, (25, 20), (75, 80), 12)
		pygame.draw.line(self.cross, _BLACK, (25, 80), (75, 20), 12)
		
		# Static 'O' surface
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
	def mouse_pressed(self, event):
		left, middle, right = pygame.mouse.get_pressed()
		
		# Ask server for permission to make a move
		if left:
			'''
			# Validate the position and check if the cell is not occupied
			cell = self.game.cell(r, c)
			if not cell.empty(): return
			'''
			
			# Parse row and column
			x, y = event.pos
			r, c = y//120, x//120

			# Send the request
			self.game.client.socket.send(dict(
				type='TRY_MOVE', 
				game_id=self.game.id,
				row=r, col=c
			))

