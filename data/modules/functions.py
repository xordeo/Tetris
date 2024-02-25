import sys
import pygame
import os

from data.modules.settings import *


def load_image(name, color_key=None):
    fullname = os.path.join('data/', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


# экран поражения
def defeat_screen(score):
    global classic_mode_best_score
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    running = True
    menu_button_sound = True
    restart_button_sound = True
    change_text = True if score <= classic_mode_best_score else False
    change_config = True

    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # обработка нажатия на кнопку RESTART
                if 20 <= mouse_x <= 520 and 350 <= mouse_y <= 475:
                    return "restart"
                # обработка нажатия на кнопку MENU
                if 20 <= mouse_x <= 520 and 500 <= mouse_y <= 625:
                    return "menu"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key == pygame.K_ESCAPE:
                    return "menu"

        # отрисовка экрана и bg
        screen.fill((0, 0, 0))
        bg = pygame.Surface(screen_size, pygame.SRCALPHA)
        bg.set_alpha(150)
        bg.blit(pygame.transform.scale(load_image("images/backgrounds/space.jpg"), screen_size), (0, 0))
        screen.blit(bg, (0, 0))

        buttons = pygame.sprite.Group()

        button_sound = pygame.mixer.Sound("data/sounds/figure_moving_sound.ogg")
        button_sound.set_volume(SFX_volume)

        # формирование SCORE
        font = pygame.font.Font("data/fonts/ConnectionIii-Rj3W.otf", 30)
        text = font.render("YOUR SCORE:", True, (107, 103, 205))
        screen.blit(text, (40, 180))
        font = pygame.font.Font("data/fonts/ConnectionIii-Rj3W.otf", 30)
        text = font.render(str(score), True, (107, 103, 205))
        screen.blit(text, (40, 210))

        if score > classic_mode_best_score or not change_text:
            font = pygame.font.Font("data/fonts/ConnectionIii-Rj3W.otf", 80)
            text = font.render("NEW SCORE!", True, (172, 217, 83))
            screen.blit(text, (40, 40))

            if change_config:
                thisfolder = os.path.dirname(os.path.abspath("config.ini"))
                initfile = os.path.join(thisfolder, 'config.ini')
                config.set("score", "classic_mode_best_score", str(score))
                with open(initfile, "w") as config_file:
                    config.write(config_file)
                classic_mode_best_score = config.getint("score", "classic_mode_best_score")
                change_config = False
        else:
            if change_text:
                font = pygame.font.Font("data/fonts/ConnectionIii-Rj3W.otf", 80)
                text = font.render("YOU LOSE!", True, (215, 71, 78))
                screen.blit(text, (40, 40))

        font = pygame.font.Font("data/fonts/ConnectionIii-Rj3W.otf", 30)
        text = font.render("YOUR BEST SCORE:", True, (107, 103, 205))
        screen.blit(text, (40, 260))
        font = pygame.font.Font("data/fonts/ConnectionIii-Rj3W.otf", 30)
        text = font.render(str(classic_mode_best_score), True, (107, 103, 205))
        screen.blit(text, (40, 290))

        # кнопка RESTART
        restart_button = pygame.sprite.Sprite()
        restart_button.image = pygame.transform.scale(load_image("images/buttons/restart_button.png"), (500, 125))
        restart_button.rect = restart_button.image.get_rect()
        restart_button.rect.x, restart_button.rect.y = 20, 350
        buttons.add(restart_button)
        if 20 <= mouse_x <= 520 and 350 <= mouse_y <= 475:
            if restart_button_sound:
                button_sound.play()
                restart_button_sound = False
            while restart_button.rect.x < 100:
                restart_button.rect.x += 1
        else:
            restart_button.rect.x = 20
            restart_button_sound = True

        # кнопка MENU
        menu_button = pygame.sprite.Sprite()
        menu_button.image = pygame.transform.scale(load_image("images/buttons/menu_button.png"), (500, 125))
        menu_button.rect = menu_button.image.get_rect()
        menu_button.rect.x, menu_button.rect.y = 20, 500
        buttons.add(menu_button)
        if 20 <= mouse_x <= 520 and 500 <= mouse_y <= 625:
            if menu_button_sound:
                button_sound.play()
                menu_button_sound = False
            while menu_button.rect.x < 100:
                menu_button.rect.x += 1
        else:
            menu_button.rect.x = 20
            menu_button_sound = True

        buttons.draw(screen)

        pygame.display.flip()
        clock.tick(fps)


# настройки игры
def settings():
    # инициализация pygame
    global music_volume
    global SFX_volume
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    running = True
    menu_button_sound = True

    button_sound = pygame.mixer.Sound("data/sounds/figure_moving_sound.ogg")
    button_sound.set_volume(SFX_volume)

    # слайдер MUSIC
    music_slider_components = pygame.sprite.Group()
    moving_music_slider = False

    music_slider = pygame.sprite.Sprite()
    music_slider.image = pygame.transform.scale(load_image("images/sound_slider/slider.png"), (520, 20))
    music_slider.rect = music_slider.image.get_rect()
    music_slider.rect.x, music_slider.rect.y = 260, 185
    music_slider_components.add(music_slider)

    music_slider_button = pygame.sprite.Sprite()
    music_slider_button.image = pygame.transform.scale(load_image("images/sound_slider/slider_button.png"), (30, 30))
    music_slider_button.rect = music_slider_button.image.get_rect()
    music_slider_button.rect.x, music_slider_button.rect.y = 260 + (music_volume * 500), 180
    music_slider_components.add(music_slider_button)

    music_slider_sound = pygame.sprite.Sprite()
    music_slider_sound.image = pygame.transform.scale(load_image("images/sound_slider/sound_sprite_1.png"), (60, 50))
    music_slider_sound.rect = music_slider_sound.image.get_rect()
    music_slider_sound.rect.x, music_slider_sound.rect.y = 785, 170
    music_slider_components.add(music_slider_sound)

    # слайдер SFX
    sfx_slider_components = pygame.sprite.Group()
    moving_sfx_slider = False

    sfx_slider = pygame.sprite.Sprite()
    sfx_slider.image = pygame.transform.scale(load_image("images/sound_slider/slider.png"), (520, 20))
    sfx_slider.rect = sfx_slider.image.get_rect()
    sfx_slider.rect.x, sfx_slider.rect.y = 260, 225
    sfx_slider_components.add(sfx_slider)

    sfx_slider_button = pygame.sprite.Sprite()
    sfx_slider_button.image = pygame.transform.scale(load_image("images/sound_slider/slider_button.png"), (30, 30))
    sfx_slider_button.rect = sfx_slider_button.image.get_rect()
    sfx_slider_button.rect.x, sfx_slider_button.rect.y = 260 + (SFX_volume * 500), 220
    sfx_slider_components.add(sfx_slider_button)

    sfx_slider_sound = pygame.sprite.Sprite()
    sfx_slider_sound.image = pygame.transform.scale(load_image("images/sound_slider/sound_sprite_1.png"), (60, 50))
    sfx_slider_sound.rect = sfx_slider_sound.image.get_rect()
    sfx_slider_sound.rect.x, sfx_slider_sound.rect.y = 785, 210
    sfx_slider_components.add(sfx_slider_sound)

    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if music_slider_button.rect.collidepoint(event.pos):
                    moving_music_slider = True
                if sfx_slider_button.rect.collidepoint(event.pos):
                    moving_sfx_slider = True

                # обработка нажатия на кнопку MENU
                if 20 <= mouse_x <= 520 and 500 <= mouse_y <= 625:
                    return "menu"

            if event.type == pygame.MOUSEMOTION:
                # обработка MUSIC слайдера
                if moving_music_slider:
                    if 260 <= music_slider_button.rect.x + event.rel[0] <= 760:
                        music_slider_button.rect.move_ip(event.rel[0], 0)
                        button_sound.play()
                    elif music_slider_button.rect.x + event.rel[0] > 760:
                        music_slider_button.rect.x = 760
                        button_sound.play()
                    elif music_slider_button.rect.x + event.rel[0] < 260:
                        music_slider_button.rect.x = 260
                        button_sound.play()
                    thisfolder = os.path.dirname(os.path.abspath("config.ini"))
                    initfile = os.path.join(thisfolder, 'config.ini')
                    config.set("settings", "music_volume", str((music_slider_button.rect.x - 260) / 500))
                    with open(initfile, "w") as config_file:
                        config.write(config_file)
                    music_volume = config.getfloat("settings", "music_volume")
                    pygame.mixer.music.set_volume(music_volume)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"

                # обработка SFX слайдера
                if moving_sfx_slider:
                    if 260 <= sfx_slider_button.rect.x + event.rel[0] <= 760:
                        sfx_slider_button.rect.move_ip(event.rel[0], 0)
                        button_sound.play()
                    elif sfx_slider_button.rect.x + event.rel[0] > 760:
                        sfx_slider_button.rect.x = 760
                        button_sound.play()
                    elif sfx_slider_button.rect.x + event.rel[0] < 260:
                        sfx_slider_button.rect.x = 260
                        button_sound.play()
                    thisfolder = os.path.dirname(os.path.abspath("config.ini"))
                    initfile = os.path.join(thisfolder, 'config.ini')
                    config.set("settings", "SFX_volume", str((sfx_slider_button.rect.x - 260) / 500))
                    with open(initfile, "w") as config_file:
                        config.write(config_file)
                    SFX_volume = config.getfloat("settings", "SFX_volume")
                    button_sound.set_volume(SFX_volume)

            if event.type == pygame.MOUSEBUTTONUP:
                moving_music_slider = False
                moving_sfx_slider = False

        # отрисовка экрана и bg
        screen.fill((0, 0, 0))
        bg = pygame.Surface(screen_size, pygame.SRCALPHA)
        bg.set_alpha(150)
        bg.blit(pygame.transform.scale(load_image("images/backgrounds/space.jpg"), screen_size), (0, 0))
        screen.blit(bg, (0, 0))

        buttons = pygame.sprite.Group()

        # надпись SETTINGS
        title = pygame.transform.scale(load_image("images/icons/settings_title.png"), (600, 150))
        screen.blit(title, (20, 0))

        # надпись MUSIC VOLUME
        font = pygame.font.Font("data/fonts/ConnectionIii-Rj3W.otf", 30)
        text = font.render("MUSIC VOLUME", True, (107, 103, 205))
        screen.blit(text, (40, 180))

        # слайдер MUSIC VOLUME
        if music_volume == 0:
            music_slider_sound.image = pygame.transform.scale(load_image("images/sound_slider/sound_sprite_1.png"),
                                                              (60, 50))
        elif 0 < music_volume <= 0.33:
            music_slider_sound.image = pygame.transform.scale(load_image("images/sound_slider/sound_sprite_2.png"),
                                                              (60, 50))
        elif 0.33 < music_volume <= 0.66:
            music_slider_sound.image = pygame.transform.scale(load_image("images/sound_slider/sound_sprite_3.png"),
                                                              (60, 50))
        elif 0.66 < music_volume <= 1.0:
            music_slider_sound.image = pygame.transform.scale(load_image("images/sound_slider/sound_sprite_4.png"),
                                                              (60, 50))

        # текущее значение MUSIC VOLUME
        font = pygame.font.Font("data/fonts/ConnectionIii-Rj3W.otf", 30)
        text = font.render(str(int(config.getfloat("settings", "music_volume") * 100)) + "%", True, (107, 103, 205))
        screen.blit(text, (850, 182))

        music_slider_components.draw(screen)
        music_slider_components.update()

        # надпись SFX VOLUME
        font = pygame.font.Font("data/fonts/ConnectionIii-Rj3W.otf", 30)
        text = font.render("SFX VOLUME", True, (107, 103, 205))
        screen.blit(text, (40, 220))

        # слайдер SFX VOLUME
        if SFX_volume == 0:
            sfx_slider_sound.image = pygame.transform.scale(load_image("images/sound_slider/sound_sprite_1.png"),
                                                            (60, 50))
        elif 0 < SFX_volume <= 0.33:
            sfx_slider_sound.image = pygame.transform.scale(load_image("images/sound_slider/sound_sprite_2.png"),
                                                            (60, 50))
        elif 0.33 < SFX_volume <= 0.66:
            sfx_slider_sound.image = pygame.transform.scale(load_image("images/sound_slider/sound_sprite_3.png"),
                                                            (60, 50))
        elif 0.66 < SFX_volume <= 1.0:
            sfx_slider_sound.image = pygame.transform.scale(load_image("images/sound_slider/sound_sprite_4.png"),
                                                            (60, 50))

        # текущее значение SFX VOLUME
        font = pygame.font.Font("data/fonts/ConnectionIii-Rj3W.otf", 30)
        text = font.render(str(int(config.getfloat("settings", "SFX_volume") * 100)) + "%", True, (107, 103, 205))
        screen.blit(text, (850, 222))

        sfx_slider_components.draw(screen)
        sfx_slider_components.update()

        # кнопка MENU
        menu_button = pygame.sprite.Sprite()
        menu_button.image = pygame.transform.scale(load_image("images/buttons/menu_button.png"), (500, 125))
        menu_button.rect = menu_button.image.get_rect()
        menu_button.rect.x, menu_button.rect.y = 20, 500
        buttons.add(menu_button)
        if 20 <= mouse_x <= 520 and 500 <= mouse_y <= 625:
            if menu_button_sound:
                button_sound.play()
                menu_button_sound = False
            while menu_button.rect.x < 100:
                menu_button.rect.x += 1
        else:
            menu_button.rect.x = 20
            menu_button_sound = True

        buttons.draw(screen)

        pygame.display.flip()
        clock.tick(fps)


# меню игры
def menu(from_settings):
    # инициализация pygame
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()

    # настройка музыки и звука
    if not from_settings:
        pygame.mixer.music.load("data/music/Success-Story_-Akiko-Shioyama-Menu-Music.mp3")
        pygame.mixer.music.set_volume(music_volume)
        pygame.mixer.music.play(-1)

    # параметры
    running = True
    play_button_sound = True
    settings_button_sound = True
    exit_button_sound = True

    button_sound = pygame.mixer.Sound("data/sounds/figure_moving_sound.ogg")
    button_sound.set_volume(SFX_volume)

    # цикл меню
    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # обработка нажатия на кнопку PLAY
                if 20 <= mouse_x <= 520 and 200 <= mouse_y <= 325:
                    return "play_button"
                # обработка нажатия на кнопку SETTINGS
                if 20 <= mouse_x <= 520 and 350 <= mouse_y <= 475:
                    return "settings"
                # обработка нажатия на кнопку EXIT
                if 20 <= mouse_x <= 520 and 500 <= mouse_y <= 625:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return "play_button"

                if event.key == pygame.K_s:
                    return "settings"

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # отрисовка экрана и bg
        screen.fill((0, 0, 0))
        bg = pygame.Surface(screen_size, pygame.SRCALPHA)
        bg.set_alpha(150)
        bg.blit(pygame.transform.scale(load_image("images/backgrounds/space.jpg"), screen_size), (0, 0))
        screen.blit(bg, (0, 0))

        # логотип TETRIS
        logo = pygame.transform.scale(load_image("images/icons/logo.png"), (450, 150))
        screen.blit(logo, (0, 0))

        buttons = pygame.sprite.Group()

        # кнопка PLAY
        play_button = pygame.sprite.Sprite()
        play_button.image = pygame.transform.scale(load_image("images/buttons/play_button.png"), (500, 125))
        play_button.rect = play_button.image.get_rect()
        play_button.rect.x, play_button.rect.y = 20, 200
        buttons.add(play_button)
        if 20 <= mouse_x <= 520 and 200 <= mouse_y <= 325:
            if play_button_sound:
                button_sound.play()
                play_button_sound = False
            while play_button.rect.x < 100:
                play_button.rect.x += 1
        else:
            play_button.rect.x = 20
            play_button_sound = True

        # кнопка SETTINGS
        settings_button = pygame.sprite.Sprite()
        settings_button.image = pygame.transform.scale(load_image("images/buttons/settings_button.png"), (500, 125))
        settings_button.rect = settings_button.image.get_rect()
        settings_button.rect.x, settings_button.rect.y = 20, 350
        buttons.add(settings_button)
        if 20 <= mouse_x <= 520 and 350 <= mouse_y <= 475:
            if settings_button_sound:
                button_sound.play()
                settings_button_sound = False
            while settings_button.rect.x < 100:
                settings_button.rect.x += 1
        else:
            settings_button.rect.x = 20
            settings_button_sound = True

        # кнопка EXIT
        exit_button = pygame.sprite.Sprite()
        exit_button.image = pygame.transform.scale(load_image("images/buttons/exit_button.png"), (500, 125))
        exit_button.rect = exit_button.image.get_rect()
        exit_button.rect.x, exit_button.rect.y = 20, 500
        buttons.add(exit_button)
        if 20 <= mouse_x <= 520 and 500 <= mouse_y <= 625:
            if exit_button_sound:
                button_sound.play()
                exit_button_sound = False
            while exit_button.rect.x < 100:
                exit_button.rect.x += 1
        else:
            exit_button.rect.x = 20
            exit_button_sound = True

        buttons.draw(screen)

        pygame.display.flip()
        clock.tick(fps)
