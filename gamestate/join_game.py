from .state import State
import pygame

_BLACK = (0, 0, 0)
_WHITE = (255, 255, 255)
_RED   = (255, 0, 0)

class JoinGameState(State):
	def __init__(self, game):
		State.__init__(self, game)
		# Fonts with different sizes
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
		# Game list related variables
		self.__selected = 0
	def update(self):
		self.game.client.socket.send(dict(type='LIST_GAME'))
	def draw(self, screen):
		screen.blit(self.bg, (0, 0))
		for i, game in enumerate(self.game.game_list):
			col  = _RED if self.__selected == i else _BLACK
			no   = self.font3.render(str(i), True, col)
			name = self.font3.render(game['id'], True, col)
			h    = no.get_rect().height
			y    = 110+(10+h)*i
			screen.blit(no, (10, y))
			screen.blit(name, (60, y))
	def key_down(self, event):
		# Back to main menu
		if event.key == pygame.K_ESCAPE:
			self.game.state.pop()
		# Navigate through the list
		if event.key == pygame.K_UP:
			self.__selected -= 1
		if event.key == pygame.K_DOWN:
			self.__selected += 1
		# Constrain the index
		max_idx = len(self.game.game_list) - 1
		if self.__selected < 0: self.__selected = 0
		if self.__selected > max_idx: self.__selected = max_idx
		# Join a session/game
		if event.key == pygame.K_RETURN:
			game_id = self.game.game_list[self.__selected]['id']
			print('Join a session', game_id)
			self.game.client.socket.send(dict(
				type='JOIN_GAME',
				game_id=game_id
			))
