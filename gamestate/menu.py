from .state import State
from .create_game import CreateGameState
from .join_game import JoinGameState
import pygame

_BLACK = (0, 0, 0)
_WHITE = (255, 255, 255)
_GRAY  = (51, 51, 51)
_RED   = (255, 0, 0)

class MenuState(State):
	def __init__(self, game):
		State.__init__(self, game)
		# Font, title and others
		self.font1      = pygame.font.Font('freesansbold.ttf', 48)
		self.font2      = pygame.font.Font('freesansbold.ttf', 12)
		self.font3      = pygame.font.Font('freesansbold.ttf', 22)
		self.font4      = pygame.font.Font('freesansbold.ttf', 18)
		self.title      = self.font1.render(' Tic-Tac-Toe ', True, _BLACK)
		self.credit     = self.font2.render('Made by xxMrPHDxx', True, _RED)
		self._options   = ['Create', 'Join']
		self._selected  = 0
	def update(self):
		pass
	def draw(self, screen):
		w = self.title.get_rect().width
		screen.blit(self.title, (self.game.width/2-w/2, 70))
		w = self.credit.get_rect().width
		screen.blit(self.credit, (self.game.width/2-w/2, 130))
		for i, option in enumerate(self._options):
			selected = self._selected == i
			font = self.font3 if selected else self.font4
			text = font.render(
				f'[ {option} ]' if selected else option, 
				True, 
				_GRAY if selected else _BLACK
			)
			w = text.get_rect().width
			screen.blit(text, (self.game.width/2-w/2, 210+28*i))
	def key_down(self, event):
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			self.game.should_exit = True
		if event.key == pygame.K_UP:
			self._selected -= 1
		if event.key == pygame.K_DOWN:
			self._selected += 1
		if self._selected <  0: self._selected = 0
		if self._selected >= 2: self._selected = 1
		if event.key == pygame.K_RETURN:
			if self._selected == 0:
				# Go to join server state
				self.game.state.push(CreateGameState)
			elif self._selected == 1:
				# Go to join server state
				self.game.state.push(JoinGameState)

