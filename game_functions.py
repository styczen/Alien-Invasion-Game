import sys
import pygame
from bullet import Bullet
from alien import Alien

def get_number_aliens_x(ai_settings, alien_width):
	"""Determine the number of aliens which fit in the row."""
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x
	
def get_number_rows(ai_settings, ship_height, alien_height):
	"""Determine the number of rows of aliens that fit in the screen."""
	available_space_y = (ai_settings.screen_height-(3*alien_height)-ship_height)
	number_rows = int(available_space_y/(2*alien_height))
	return number_rows
	
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""Create an alien and place it in the row of aliens."""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height+2*alien.rect.height*row_number
	aliens.add(alien)	
	
def create_fleet(ai_settings, screen, ship, aliens):
	"""Create a full fleet of aliens."""
	# Create an alien and find the number of aliens in a row.
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
	
	# Create the fleet of aliens.
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number, row_number)
			
def check_fleet_edges(ai_settings, aliens):
	"""Act properly when alien hits an edge."""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break
			
def change_fleet_direction(ai_settings, aliens):
	"""Drop the entire fleet and change its' direction."""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1 # to change direction in next drop
			
def update_aliens(ai_settings, ship, aliens):
	"""Check if the fleet is at an edge and update the positions of all aliens in the fleet"""
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	
	# Look for alien-ship collisions.
	if pygame.sprite.spritecollideany(ship, aliens):
		print("Ship hit!!!")

def check_events(ai_settings, screen, ship, bullets):
	"""Respond to keypressed and mouse events."""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)	
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
				
def check_keydown_events(event, ai_settings, screen, ship, bullets):
	"""Respond to keypresses."""
	# Right - Left
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	# Up - Down
	elif event.key == pygame.K_UP:
		ship.moving_up = True
	elif event.key == pygame.K_DOWN:
		ship.moving_down = True
	# Spacebar - shooting
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		sys.exit()

			
def fire_bullet(ai_settings, screen, ship, bullets):
	"""Fire a bullet if limit is not reached yet."""
	# Create a new bullet and add it to the bullets group
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)
		
def check_keyup_events(event, ship):
	"""Respond to key releases."""
	# Right - Left
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
		
	# Up - Down
	if event.key == pygame.K_UP:
		ship.moving_up = False
	elif event.key == pygame.K_DOWN:
		ship.moving_down = False
				
def update_screen(ai_settings, screen, ship, aliens, bullets):
	"""Update images on the screen and flip to the new screen."""
	# Redraw the screen during each pass through the loop
	screen.fill(ai_settings.bg_color)
	
	# Redraw all bullets behind ship and aliens.
	for bullet in bullets.sprites():
		bullet.draw_bullet()

	ship.blitme()
	aliens.draw(screen)
		
	# Make the most recently drawn screen visible
	pygame.display.flip()
	
def update_bullets(ai_settings, screen, ship, aliens, bullets):
	"""Update position of the bullets and rid of old bullets."""
	# Update bullet positions.
	bullets.update()
		
	# Get rid of bullets that have disappeared
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	
	check_bullet_alien_collision(ai_settings, screen, ship, aliens, bullets)
			
def check_bullet_alien_collision(ai_settings, screen, ship, aliens, bullets):
	"""Respond to bullet-alien collision."""
	# Remove any bullets and aliens that have collided.
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True) # reference in Pygame docs
	
	if len(aliens) == 0:
		# Destroy existing bullets and create new fleet.
		bullets.empty()
		create_fleet(ai_settings, screen, ship, aliens)
