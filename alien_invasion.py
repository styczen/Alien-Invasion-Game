import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien

def run_game():
	# Initialize game and create a screen object
	pygame.init()
	ai_settings = Settings()
	
	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
	
	pygame.display.set_caption("Alien Invasion")
	
	# Make a ship
	ship = Ship(ai_settings, screen)
	
	# Make a group to store bullets in.
	bullets = Group()
	
	# Make a group of aliens.
	aliens = Group()
	
	# Create the fleet of aliens.
	gf.create_fleet(ai_settings, screen, ship, aliens)
	
	# Start the main loop for the game
	while True:
		# Watch for the keyboard and mouse events
		gf.check_events(ai_settings, screen, ship, bullets)
		ship.update()
		gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
		gf.update_aliens(ai_settings, ship, aliens)
		gf.update_screen(ai_settings, screen, ship, aliens, bullets)
		
		#alien = Alien(ai_settings, screen)
		#print(gf.get_number_aliens_x(ai_settings, alien.rect.width))
	
run_game()
