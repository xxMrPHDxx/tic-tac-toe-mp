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
		title   = self.font1.render('Available games', True, _BLACK)
		self.bg.fill(_WHITE)
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
		self.game.client.socket.send(dict(type='LIST_GAME'))
	def draw(self, screen):
		screen.blit(self.bg, (0, 0))
		for i, game in enumerate(self.game.game_list):
			no   = self.font3.render(str(i), True, _BLACK)
			name = self.font3.render(game['id'], True, _BLACK)
			h    = no.get_rect().height
			y    = 110+(10+h)*i
			screen.blit(no, (10, y))
			screen.blit(name, (60, y))
	def key_down(self, event):
		if event.key == pygame.K_ESCAPE:
			self.game.state.pop()
		if False:
			# TODO: Join a session/game
			pass
