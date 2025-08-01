# THIS IS A GAME I'M MAKING BASED ON GALAGA! THE MAIN USE FOR THE GAME WITH BE TO CREATE AN AI ENVIROMENT FOR TRAINING MY DRL AI.
# IN THE FUTURE, I HOPE TO MAKE THIS GAME A TRUE PIECE OF ART! I'M NOT TRYING TO MAKE MONEY OFF THIS PROJECT SO I TOOK THE LIBERTY OF
# USING SPRITES THAT WERE SIMILAR TO THE ONES IN GALAGA, AS WELL AS VIDEO GAME MUSIC.
#
# TITLE SCREEN => PLAY THIS AT 1.25X SPEED - MIDIJAM BY FAVBEA
# NORMAL GAME BGM => JAZZ FUSION FROM THE INCREDIBLE MACHINE
# BOSS MUSIC => MOBEBIUS BATTLE 2 FROM XENOBLADE CHRONICLES 3


import sys

from time import sleep

import pygame

from pygame.sprite import Group

from settings import Settings

from ship import Ship

import game_functions as gf

from game_stats import GameStats

from button import Button

from image_button import ImageButton

from scoreboard import Scoreboard

def run_game():

    # Initialize game and create screen object
    pygame.init()
    pygame.mixer.init()
    title_screen_music_path = gf.resource_path("Game_Music/Title Screen BGM.mp3")
    pygame.mixer.music.load(title_screen_music_path)
    pygame.mixer.music.play(-1)

    gameSettings = Settings()
    screen = pygame.display.set_mode((gameSettings.screen_width, gameSettings.screen_height))
    pygame.display.set_caption("Untitled Alien Shooter")

    # Create the Play Button, Setting Icon, and Return Icon

    play_button = Button(gameSettings, screen, "Play")

    options_icon_path = gf.resource_path("Game_Images/options_icon.bmp")
    options_icon = ImageButton(screen, options_icon_path, 2)
    options_icon.change_orientation("bottom", "bottom")
    options_icon.change_orientation("left", "left")

    return_icon_path = gf.resource_path("Game_Images/return_icon.bmp")
    return_icon = ImageButton(screen, return_icon_path, 1.5)
    return_icon.change_orientation("bottom", "bottom")
    return_icon.change_orientation("left", "left")

    # Just some small tweaks to the positioning
    return_icon.rect.x += 10
    return_icon.rect.y -= 10

    # Make an instance of game statisitcs and create a scoreboard

    stats = GameStats(gameSettings)
    scoreboard = Scoreboard(gameSettings, screen, stats)

    # Make a Ship Object

    userShip = Ship(gameSettings, screen)

    # Make a group to store bullets and aliens

    bullets = Group()
    aliens = Group()

    # Create the fleet of aliens
    gf.create_fleet(gameSettings, screen, userShip, aliens)

    # Create an icon for the game window
    icon_surface = pygame.image.load(gf.resource_path("Game_Images/ship.bmp"))
    pygame.display.set_icon(icon_surface)


    # Title Screen Loop
    
    # Load and position multiple background images for horizontal scrolling
    title_backgrounds = []
    title_background_path = gf.resource_path("Game_Images/Title_Background.bmp")
    title_background_image = pygame.image.load(title_background_path)
    title_background_width = title_background_image.get_width()

    gf.set_scrolling_rects_title(screen, title_backgrounds, title_background_image, title_background_width)

    while not stats.game_active:

        if not stats.options_active:
            gf.draw_scrolled_background_title(screen, title_backgrounds, 0.25)
            gf.check_events(gameSettings, screen, stats, play_button, options_icon, return_icon, userShip, aliens, bullets)

            # Draw the game title
            text_font_path = gf.resource_path("Text_Font/Emulogic-zrEw.ttf")
            font = pygame.font.Font(text_font_path, 60)
            title_text = font.render("Untitled Alien Shooter", True, (255, 255, 255))   
            title_x = screen.get_width() // 2 - title_text.get_width() // 2
            title_y = screen.get_height() // 4 - title_text.get_height() // 2
            screen.blit(title_text, (title_x, title_y))

            play_button.draw_button()
            options_icon.draw_button()
            pygame.display.flip()
        else:
            gf.draw_scrolled_background_title(screen, title_backgrounds, 0.25)
            gf.check_events(gameSettings, screen, stats, play_button, options_icon, return_icon, userShip, aliens, bullets)

            # Draw the options title
            font = pygame.font.Font(text_font_path, 60)
            title_text = font.render("Options", True, (255, 255, 255)) 
            title_x = screen.get_width() // 2 - title_text.get_width() // 2
            title_y = screen.get_rect().top
            screen.blit(title_text, (title_x, title_y))

            play_button.draw_button()
            return_icon.draw_button()
            pygame.display.flip()

    # End Title Screen BGM
    pygame.mixer.music.fadeout(500)
    gf.fade_out(screen, 0.5, pygame.time.Clock(), (0, 0, 0))

    normal_music_path = gf.resource_path("Game_Music/Normal BGM.mp3")
    pygame.mixer.music.load(normal_music_path)
    pygame.mixer.music.play(-1)

    # Game Loop
    game_backgrounds = []
    game_background_path = gf.resource_path("Game_Images/Space_Background.bmp")
    game_background_image = pygame.image.load(game_background_path)
    game_background_height = game_background_image.get_height()

    gf.set_scrolling_rect_game(screen, game_backgrounds, game_background_image, game_background_height)

    while stats.game_active:
        gf.draw_scrolled_background_game(screen, game_backgrounds, 0.15)
        gf.check_events(gameSettings, screen, stats, play_button, options_icon, return_icon, userShip, aliens, bullets)
        userShip.update()
        gf.update_bullets(gameSettings, screen, stats, scoreboard, userShip, aliens, bullets)
        gf.update_aliens(gameSettings, stats, screen, userShip, aliens, bullets, scoreboard)
        gf.update_screen(gameSettings, screen, stats, scoreboard, userShip, aliens, bullets, play_button)
run_game()