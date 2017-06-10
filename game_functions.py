import sys
import pygame
from bullet import Bullet

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
	# Space - shooting
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)

			
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
				
def update_screen(ai_settings, screen, ship, bullets):
	"""Update images on the screen and flip to the new screen."""
	# Redraw the screen during each pass through the loop
	screen.fill(ai_settings.bg_color)
	
	ship.blitme()
	# Redraw all bullets behind ship and aliens.
	for bullet in bullets.sprites():
		bullet.draw_bullet()
		
	# Make the most recently drawn screen visible
	pygame.display.flip()
	
def update_bullets(bullets):
	"""Update position of the bullets and rid of old bullets."""
	# Update bullet positions.
	bullets.update()
		
	# Get rid of bullets that have disappeared
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
