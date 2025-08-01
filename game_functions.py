import sys, os

import pygame

from bullet import Bullet

from alien import Alien

from treasure_alien import TreasureAlien

from time import sleep

from math import ceil

from random import randint

from button import Button

from image_button import ImageButton

import utilities as ults

import json 

def check_keydown_events(event, gameSettings, screen, ship, bullets, stats):

    # Respond to key presses

    if event.key == pygame.K_RIGHT:
        # Move the ship to the right
        ship.move_right = True
    elif event.key == pygame.K_LEFT:
        # Move the ship to the left
        ship.move_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(gameSettings, screen, ship, bullets, stats)
    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
        sys.exit()

def check_keyup_events(event, ship):

    # Respond to key releases

    if event.key == pygame.K_RIGHT:
        # Stop moving the ship to the right
        ship.move_right = False
    elif event.key == pygame.K_LEFT:
        # Stop moving the ship to the left
        ship.move_left = False

def check_events(gameSettings, screen, stats, play_button, options_icon, return_icon, ship, aliens, bullets):

    # Responds to keypresses and mouse events

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
           check_keydown_events(event, gameSettings, screen, ship, bullets, stats)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if not stats.options_active:
                check_play_button(gameSettings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y)
                check_options_icon(screen, stats, options_icon, mouse_x, mouse_y)
                check_quit_button(screen, stats, options_icon, mouse_x, mouse_y)
            else:
                check_return_icon(screen, stats, return_icon, mouse_x, mouse_y)

def check_quit_button(screen, stats, quit_button, mouse_x, mouse_y):
    button_clicked = quit_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and stats.game_active:
        stats.game_active = False

def check_return_icon(screen, stats, return_icon, mouse_x, mouse_y):
    button_clicked = return_icon.is_clicked((mouse_x, mouse_y))
    if button_clicked and stats.options_active and not stats.game_active:
        stats.options_active = False

def check_options_icon(screen, stats, options_icon, mouse_x, mouse_y):
    button_clicked = options_icon.is_clicked((mouse_x, mouse_y))
    if button_clicked and not stats.options_active and not stats.game_active:
        stats.options_active = True

def check_play_button(gameSettings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):

    # Start a new game when a player clicks play
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings
        gameSettings.init_dynamic_speed_factors()
        pygame.mouse.set_visible(False)
        stats.game_active = True
        # Reset game stats
        stats.reset_stats()

        # Empty aliens and bullets
        aliens.empty()
        bullets.empty()

        # Make new fleet and center ship
        create_fleet(gameSettings, screen, ship, aliens)
        ship.center_ship()

def update_screen(screen, scoreboard, ship, aliens, bullets):

    # Update images on the screen and flip to the new screen
    # Redraw the screen during each pass through the loop

    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    # Draw the score information
    scoreboard.show_score()

    # Make the most recently drawn screen visible

    pygame.display.flip()

def update_bullets(gameSettings, screen, stats, scoreboard, ship, aliens, bullets):

    # Update bullet positions

    bullets.update()
    
    # Get rid of bullets that have disappeared

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            stats.missed_bullets += 1

    # Check for bullet-alien collisions

    check_bullet_alien_collisions(gameSettings, screen, stats, scoreboard, ship, aliens, bullets)

def fire_bullet(gameSettings, screen, ship, bullets, stats):

    # Fire a bullet if limit isn't reached

    if len(bullets) < gameSettings.bullets_allowed:
            
            # Create a new bullet and add it to the bullets group

            newBullet = Bullet(gameSettings, screen, ship)
            bullets.add(newBullet)
            stats.num_bullets_fired += 1

def create_fleet(gameSettings, screen, ship, aliens):

    # Create a full fleet of aliens + hitbox math

    alien = Alien(gameSettings, screen)
    number_aliens_x = get_number_aliens_x(gameSettings, alien.rect.width)
    number_rows = get_number_rows(gameSettings, ship.rect.height, alien.rect.height)

    # Create the fleet of aliens

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
        
            # Create an alien and place it in the row
            create_alien(gameSettings, screen, aliens, alien_number, row_number)

def get_number_aliens_x(gameSettings, alien_width):

    # Figure out how many aliens can fit in a row

    available_space_x = gameSettings.screen_width - (2 * alien_width)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(gameSettings, screen, aliens, alien_number, row_number):

    # Create an alien and place it in the row

    # Roll between having a normal alien or a treasure alien that drops power-ups

    # Treasure aliens have a 2% chance of spawning normally
    if randint(1, 50) == 1:
        alien = TreasureAlien(gameSettings, screen)
    else:
        alien = Alien(gameSettings, screen)
    alien_width = alien.rect.width
    alien.rect.x = alien_width + (2 * alien_width * alien_number)
    alien.x = float(alien.rect.x)
    alien.rect.y = alien.rect.height + (2 * alien.rect.height * row_number)
    aliens.add(alien)

def get_number_rows(gameSettings, ship_height, alien_height):

    # Figure out how many rows of aliens can fit on the screen

    available_space_y = (gameSettings.screen_height) - (3 * alien_height) - (ship_height)
    number_rows = int(available_space_y / (3.5 * alien_height))
    return number_rows

def update_aliens(gameSettings, stats, screen, ship, aliens, bullets, scoreboard):

    # Update the positions of all aliens in the fleet based on environment

    check_fleet_edges(gameSettings, aliens)
    aliens.update()

    # Look for alien-ship collisions

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(gameSettings, stats, screen, ship, aliens, bullets, scoreboard)

    # Look for alien collisions to the bottom screen

    check_aliens_bottom(gameSettings, stats, screen, ship, aliens, bullets)

def check_fleet_edges(gameSettings, aliens):

    # Responds if Aliens have hit an edge

    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(gameSettings, aliens)
            break

def change_fleet_direction(gameSettings, aliens):
    
    # Lower the fleet and change direction!

    for alien in aliens.sprites():
        alien.rect.y += gameSettings.fleet_drop_speed
    
    gameSettings.fleet_direction *= -1

def check_bullet_alien_collisions(gameSettings, screen, stats, scoreboard, ship, aliens, bullets):

    # Respond to any bullets and aliens that have collided

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += gameSettings.alien_points * len(aliens)
            stats.num_aliens_destroyed += len(aliens)
            scoreboard.set_score()
        check_high_score(stats, scoreboard)

    if len(aliens) == 0:

        # Destroy the Remaining Bullets, speed up the game and Create a New Fleet
        bullets.empty()

        # Start a new level and increase the difficulty
        gameSettings.increase_speed()

        create_fleet(gameSettings, screen, ship, aliens)

        stats.stage_number += 1
        scoreboard.set_stage_number()

def ship_hit(gameSettings, stats, screen, ship, aliens, bullets, scoreboard):

    if stats.ships_left - 1 > 0: # Added -1 because the game loop flag is lowered in the loop
        # Decrement the ships left
        stats.ships_left -= 1
        scoreboard.set_lives_left()

        # Empty aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create new fleet and center the ship
        create_fleet(gameSettings, screen, ship, aliens)
        ship.center_ship()

        # Pause the game for a moment to show collision
        sleep(1)
    else:
        fade_out(screen, 0.5, pygame.time.Clock(), (0, 0, 0))
        stats.game_over = True
        while stats.game_over: # Game Over Menu
            text_font_path = ults.resource_path("Text_Font/Emulogic-zrEw.ttf")
            title_font = pygame.font.Font(text_font_path, 60)
            text_font = pygame.font.Font(text_font_path, 24)

            title_text = title_font.render("Game Over", True, (255, 255, 255)) 
            title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4))
            screen.blit(title_text, title_rect)

            score_text = text_font.render(f"Score:{stats.score}", True, (255, 255, 255)) 
            score_rect = score_text.get_rect(center=(screen.get_width() // 2, title_rect.bottom + 30))
            screen.blit(score_text, score_rect)

            accuracy_text = text_font.render(f"Aliens Destroyed:{stats.num_aliens_destroyed}", True, (255, 255, 255)) 
            accuracy_rect = accuracy_text.get_rect(center=(screen.get_width() // 2, score_rect.bottom + 30))
            screen.blit(accuracy_text, accuracy_rect)

            num_bullet_collisions = stats.num_bullets_fired - stats.missed_bullets
            num_bullets_fired = stats.num_bullets_fired
            try:
                shooting_accuracy = (num_bullet_collisions / num_bullets_fired) * 100
            except ZeroDivisionError:
                shooting_accuracy = 0

            aliens_text = text_font.render(f"Accuracy:{shooting_accuracy:.2f}%", True, (255, 255, 255)) 
            aliens_rect = aliens_text.get_rect(center=(screen.get_width() // 2, accuracy_rect.bottom + 30))
            screen.blit(aliens_text, aliens_rect)

            play_again_button = Button(gameSettings, screen, "Play Again")
            play_again_button.rect.top = aliens_rect.bottom + 30
            play_again_button.message_image_rect.center = play_again_button.rect.center
            play_again_button.draw_button()

            quit_button = Button(gameSettings, screen, "Retry")
            quit_button.rect.top = play_again_button.rect.bottom + 30
            quit_button.message_image_rect.center = quit_button.rect.center
            quit_button.draw_button()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if quit_button.rect.collidepoint(mouse_x, mouse_y):
                        stats.game_active = False
                        stats.game_over = False
                    elif play_again_button.rect.collidepoint(mouse_x, mouse_y):
                        # Game Start up again on a reset
                        stats.game_active = False
                        stats.game_over = False


            pygame.display.flip()
            pygame.mouse.set_visible(True)

def check_aliens_bottom(gameSettings, stats, screen, ship, aliens, bullets):

    # Check if aliens have reached the bottom of the screen

    screen_rect = screen.get_rect()

    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(gameSettings, stats, screen, ship, aliens, bullets)
            break

def set_scrolling_rects_title(screen, backgrounds, background_image, background_width):
    # Find the number of background and set their rects
    screen_rect = screen.get_rect()
    num_backgrounds = ceil(screen_rect.width / background_width) + 1
    for i in range(num_backgrounds):
        background_rect = background_image.get_rect()
        background_rect.x = i * background_width
        background_rect.y = 0

        backgrounds.append({"background_image" : background_image,
                            "background_rect" : background_rect,
                            "x_pos_float" : float(background_rect.x)
                            })

def draw_scrolled_background_title(screen, backgrounds, scroll_speed):
    screen_rect = screen.get_rect()

    for background in backgrounds:
        
        # Update the floating position
        background["x_pos_float"] += scroll_speed
        background["background_rect"].x = int(background["x_pos_float"])

        # If the image has moved completely off the right side, move it to the left of the leftmost image
        
        if background["background_rect"].x > screen_rect.width:
            leftmost_x = min(background["x_pos_float"] for background in backgrounds)
            background["x_pos_float"] = leftmost_x - background["background_rect"].width
            background["background_rect"].x = int(background["x_pos_float"])

        screen.blit(background["background_image"], background["background_rect"])

def set_scrolling_rect_game(screen, backgrounds, background_image, background_height):
    # Find the number of background and set their rects
    screen_rect = screen.get_rect()
    num_backgrounds = ceil(screen_rect.height / background_height) + 1
    for i in range(num_backgrounds):
        background_rect = background_image.get_rect()
        background_rect.x = 0
        background_rect.y = i * background_height

        backgrounds.append({"background_image" : background_image,
                            "background_rect" : background_rect,
                            "y_pos_float" : float(background_rect.y)
                            })

def draw_scrolled_background_game(screen, backgrounds, scroll_speed):
    screen_rect = screen.get_rect()

    for background in backgrounds:
        
        # Update the floating position
        background["y_pos_float"] += scroll_speed
        background["background_rect"].y = int(background["y_pos_float"])

        # If the image has moved completely off the right side, move it to the left of the leftmost image
        
        if background["background_rect"].y > screen_rect.height:
            leftmost_y = min(background["y_pos_float"] for background in backgrounds)
            background["y_pos_float"] = leftmost_y - background["background_rect"].height
            background["background_rect"].y = int(background["y_pos_float"])
        screen.blit(background["background_image"], background["background_rect"])

def fade_out(screen, duration, clock, final_color):
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface.fill(final_color)
    fade_surface.set_alpha(0)

    total_frames = int(duration * 60)
    for frame in range(total_frames):
        alpha = int((frame / total_frames) * 255)
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)

def check_high_score(stats, scoreboard):
    # Load saved high score
    try:
        high_score_json_path = ults.resource_path("Saves/high_score.json")
        with open(high_score_json_path, "r") as file:
            file_contents = json.load(file)
            file_high_score = file_contents.get("high_score", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        file_high_score = 0

    stats.high_score = max(stats.high_score, file_high_score)

    # If new high score
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        with open(high_score_json_path, "w") as file:
            json.dump({"high_score": stats.high_score}, file)

    # Render image (now that high_score is fully up to date)
    scoreboard.set_high_score()

def resource_path(relative_path):
    # Get absolute path to resource
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # When running normally (not bundled)
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)