from .state import State
import pygame

_BLACK = (0, 0, 0)
_WHITE = (255, 255, 255)

class JoinGameState(State):
	def __init__(self, game):
		State.__init__(self, game)
		self.font1   = pygame.font.Font('freesansbold.ttf', 20)
		self.font2   = pygame.font.Font('freesansbold.ttf', 12)
		self.font3   = pygame.font.Font('freesansbold.ttf', 8)
		# Create default bg template
		self.bg = pygame.Surface((self.game.width, self.game.height))
		self.bg.fill(_WHITE)
		title   = self.font1.render('Available games', True, _BLACK)
		self.bg.blit(title, ((self.game.width-title.get_rect().width)/2, 14))
		pygame.draw.line(self.bg, _BLACK, (0, 50), (self.game.width, 50), 6)
		pygame.draw.line(self.bg, _BLACK, (0, 90), (self.game.width, 90), 6)
		headers = [
			(x, self.font2.render(col, True, _BLACK))
			for x, col in [(10, 'No.'), (60, 'Name')]
		]
		for i, (x, header) in enumerate(headers):
			self.bg.blit(header, (x, 64))
			if i == 0: continue
			pygame.draw.line(self.bg, _BLACK, (x-15, 50), (x-15, self.game.height), 6)
	def update(self):
		pass # TODO: Update with server
	def draw(self, screen):
		screen.blit(self.bg, (0, 0))
		# TODO: Draw free server
	def key_down(self, event):
		if event.key == pygame.K_ESCAPE:
			self.game.state.pop()

