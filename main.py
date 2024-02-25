import pygame
from pygame.locals import *
from random import shuffle, choice

from data.modules.cup import *
from data.modules.figures_data import *
from data.modules.functions import *
from data.modules.settings import *

# инициализация pygame
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Tetris")
screen = pygame.display.set_mode(screen_size)
programIcon = pygame.image.load("data/images/icons/icon.png")
pygame.display.set_icon(programIcon)


# начало игры
def start_game():
    # настройки и переменные
    music_volume = config.getfloat("settings", "music_volume")
    SFX_volume = config.getfloat("settings", "SFX_volume")

    cup = TetrisCup()
    running = True
    figures_bag = ["I", "T", "J", "L", "O", "S", "Z"]
    figures_bag_next = ["T", "I", "J", "L", "O", "S", "Z"]

    shuffle(figures_bag)
    shuffle(figures_bag_next)

    current_figure = figures_bag[0]
    figures_bag.remove(current_figure)

    timer = 0

    figure_falling = True
    figure_falling_time = 1000
    timer_for_falling = 0
    x, y = 3, 0

    rotation = False
    rotation_pos = 0
    rotation_to_the = "right"

    take_in_hold = False
    can_take_in_hold = True
    figure_in_hold = ""

    level = 1
    lines_cleared = 0
    lines_required = 3

    # загрузка музыки
    music_list = [
        "data/music/Twenty-First-Century-People_-Omegane-Calm-BGM.mp3",
        "data/music/Cherry-Blossom-Season_-Chika-Calm-BGM.mp3",
        "data/music/Raindrops_-Chika-Calm-BGM.mp3",
        "data/music/Classy-Cat_-Kamoking-Calm-BGM.mp3",
        "data/music/Asphalt_-Chika-Calm-BGM.mp3"
    ]

    pygame.mixer.music.load(choice(music_list))
    pygame.mixer.music.set_volume(music_volume)

    # загрузка звуков
    take_figure_to_hold_sound = pygame.mixer.Sound("data/sounds/take_to_hold_sound.ogg")
    take_figure_to_hold_sound.set_volume(SFX_volume)
    figure_placed_sound = pygame.mixer.Sound("data/sounds/figure_placed_sound.ogg")
    figure_placed_sound.set_volume(SFX_volume)
    rotate_figure_sound = pygame.mixer.Sound("data/sounds/rotate_figure_sound.ogg")
    rotate_figure_sound.set_volume(SFX_volume)
    figure_moving_sound = pygame.mixer.Sound("data/sounds/figure_moving_sound.ogg")
    figure_moving_sound.set_volume(SFX_volume)
    clear_line_sound = pygame.mixer.Sound("data/sounds/clear_line_sound.ogg")
    clear_line_sound.set_volume(SFX_volume)
    clear_lines_sound_1 = pygame.mixer.Sound("data/sounds/clear_lines_sound_1.ogg")
    clear_lines_sound_1.set_volume(SFX_volume)
    clear_lines_sound_2 = pygame.mixer.Sound("data/sounds/clear_lines_sound_2.ogg")
    clear_lines_sound_2.set_volume(SFX_volume)

    pygame.mixer.music.play(-1)

    starttime = pygame.time.get_ticks()

    # цикл игры
    while running:
        # управление
        for event in pygame.event.get():
            # выход из игры
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # поворот вправо на 90°
                if event.key == pygame.K_UP or event.key == pygame.K_x:
                    if not take_in_hold and figure_falling:
                        rotation, rotation_to_the = True, "right"

                # поворот влево на 90°
                if event.key == pygame.K_z:
                    if not take_in_hold and figure_falling:
                        rotation, rotation_to_the = True, "left"

                # быстрый сброс фигуры вниз
                if event.key == pygame.K_SPACE:
                    if not take_in_hold:
                        while figure_falling:
                            for i in range(4):
                                rx, ry = figures_pos[current_figure][rotation_pos][i]
                                if ry + y + 1 < 20:
                                    if cup.cup[ry + y + 1][rx + x] == 0:
                                        figure_falling = True
                                    else:
                                        figure_falling = False
                                        break
                                else:
                                    figure_falling = False
                                    break
                            if figure_falling:
                                y += 1
                                cup.score += 2

                # взятие фигуры в HOLD
                if event.key == pygame.K_c:
                    if can_take_in_hold:
                        take_figure_to_hold_sound.play()
                        take_in_hold = True
                        can_take_in_hold = False
                        figure_falling = False

                # быстрый рестарт
                if event.key == pygame.K_r:
                    return "restart"

                # выход в меню
                if event.key == pygame.K_ESCAPE:
                    return "escape"

        # ускорение падения фигуры
        if pygame.key.get_pressed()[K_DOWN]:
            if not take_in_hold:
                for i in range(4):
                    rx, ry = figures_pos[current_figure][rotation_pos][i]
                    if ry + y + 1 < 20:
                        if cup.cup[ry + y + 1][rx + x] == 0:
                            figure_falling = True
                        else:
                            figure_falling = False
                            break
                    else:
                        figure_falling = False
                        break
                if figure_falling:
                    y += 1
                    cup.score += 1
                    figure_moving_sound.play()

        # передвижение фигуры влево
        if pygame.key.get_pressed()[K_LEFT]:
            if not take_in_hold and figure_falling:
                move_left = True
                for i in range(4):
                    rx, ry = figures_pos[current_figure][rotation_pos][i]
                    if rx + x - 1 > -1:
                        if cup.cup[ry + y][rx + x - 1] != 0:
                            move_left = False
                            break
                    else:
                        move_left = False
                        break
                if move_left:
                    x -= 1
                    figure_moving_sound.play()

        # передвижение фигуры вправо
        if pygame.key.get_pressed()[K_RIGHT]:
            if not take_in_hold and figure_falling:
                move_right = True
                for i in range(4):
                    rx, ry = figures_pos[current_figure][rotation_pos][i]
                    if rx + x + 1 < 10:
                        if cup.cup[ry + y][rx + x + 1] != 0:
                            move_right = False
                            break
                    else:
                        move_right = False
                        break
                if move_right:
                    x += 1
                    figure_moving_sound.play()

        # экран, bg и отрисовка стакана
        screen.fill((0, 0, 0))
        bg = pygame.Surface(screen_size, pygame.SRCALPHA)
        bg.set_alpha(150)
        bg.blit(pygame.transform.scale(load_image("images/backgrounds/space.jpg"), screen_size), (0, 0))
        screen.blit(bg, (0, 0))
        cup.render(screen)

        # отрисовка LEVEL
        font = pygame.font.Font("data/fonts/CyberPrincess.ttf", 17)
        text = font.render("LEVEL", True, (255, 255, 255))
        screen.blit(text, (cup.left - cup.cell_size * 2.5, cup.top + cup.cell_size * 13.5))

        font = pygame.font.Font("data/fonts/Constance-7BLXE.otf", 30)
        text = font.render(str(level), True, (255, 255, 255))
        if len(str(level)) == 1:
            screen.blit(text, (cup.left - cup.cell_size, cup.top + cup.cell_size * 14))
        elif len(str(level)) > 1 and "1" in str(level) and str(level).count("1") == 1:
            screen.blit(text, (cup.left - cup.cell_size * 1.4, cup.top + cup.cell_size * 14))
        elif len(str(level)) > 1 and "1" in str(level) and str(level).count("1") >= 2:
            screen.blit(text, (cup.left - cup.cell_size * 1.2, cup.top + cup.cell_size * 14))
        else:
            screen.blit(text, (cup.left - cup.cell_size * 1.7, cup.top + cup.cell_size * 14))

        # отрисовка LINES
        font = pygame.font.Font("data/fonts/CyberPrincess.ttf", 17)
        text = font.render("LINES", True, (255, 255, 255))
        screen.blit(text, (cup.left - cup.cell_size * 2.5, cup.top + cup.cell_size * 15.7))

        font = pygame.font.Font("data/fonts/Constance-7BLXE.otf", 30)
        text = font.render(str(lines_cleared), True, (255, 255, 255))
        if len(str(lines_cleared)) == 1:
            if "1" not in str(lines_cleared):
                screen.blit(text, (cup.left - cup.cell_size * 1.8, cup.top + cup.cell_size * 16.25))
            else:
                screen.blit(text, (cup.left - cup.cell_size * 1.5, cup.top + cup.cell_size * 16.25))
        else:
            if "1" not in str(lines_cleared):
                screen.blit(text, (cup.left - cup.cell_size * (1.8 + 0.3 * (len(str(lines_cleared)) - 1)),
                                   cup.top + cup.cell_size * 16.25))
            elif "1" in str(lines_cleared) and str(lines_cleared).count("1") > 1:
                screen.blit(text, (cup.left - cup.cell_size * (1.5 + 0.3 * (len(str(lines_cleared)) - 1)),
                                   cup.top + cup.cell_size * 16.25))
            else:
                screen.blit(text, (cup.left - cup.cell_size * (1.8 + 0.3 * (len(str(lines_cleared)) - 1)),
                                   cup.top + cup.cell_size * 16.25))

        if len(str(lines_required)) > 1 and "1" not in str(lines_required):
            font = pygame.font.Font("data/fonts/Constance-7BLXE.otf", 12)
            text = font.render(f"/{str(lines_required)}", True, (255, 255, 255))
            screen.blit(text, (cup.left - cup.cell_size, cup.top + cup.cell_size * 17))
        else:
            font = pygame.font.Font("data/fonts/Constance-7BLXE.otf", 15)
            text = font.render(f"/{str(lines_required)}", True, (255, 255, 255))
            screen.blit(text, (cup.left - cup.cell_size, cup.top + cup.cell_size * 16.8))

        # отрисовка секундомера
        stopwatch_ticks = pygame.time.get_ticks() - starttime
        millis, seconds, minutes = stopwatch_ticks % 1000, int(stopwatch_ticks / 1000 % 60), int(stopwatch_ticks / 60000 % 24)
        stopwatch_out = "{minutes:02d}:{seconds:02d}".format(minutes=minutes, seconds=seconds)[1:]
        stopwatch_millis = ".{millis}".format(millis=millis)

        font = pygame.font.Font("data/fonts/CyberPrincess.ttf", 17)
        text = font.render("TIME", True, (255, 255, 255))
        screen.blit(text, (cup.left - cup.cell_size * 2, cup.top + cup.cell_size * 18))

        font = pygame.font.Font("data/fonts/Constance-7BLXE.otf", 30)
        text = font.render(stopwatch_out, True, (255, 255, 255))
        if "1" in stopwatch_out:
            screen.blit(text, (cup.left - cup.cell_size * (4 - 0.3 * stopwatch_out.count("1")), cup.top + cup.cell_size * 18.6))
        else:
            screen.blit(text, (cup.left - cup.cell_size * 4, cup.top + cup.cell_size * 18.6))
        font = pygame.font.Font("data/fonts/Constance-7BLXE.otf", 15)
        text = font.render(stopwatch_millis, True, (255, 255, 255))
        screen.blit(text, (cup.left - cup.cell_size * 1.5, cup.top + cup.cell_size * 19.2))

        # действие каждый промежуток времени в ms
        if pygame.time.get_ticks() - timer > figure_falling_time:
            if not take_in_hold:
                timer = pygame.time.get_ticks()
                for i in range(4):
                    rx, ry = figures_pos[current_figure][rotation_pos][i]
                    if ry + y + 1 < 20:
                        if cup.cup[ry + y + 1][rx + x] == 0:
                            figure_falling = True
                        else:
                            figure_falling = False
                            break
                    else:
                        figure_falling = False
                        break
                if figure_falling:
                    y += 1

        # ускорение падения фигур с течением времени
        if pygame.time.get_ticks() - timer_for_falling > 30000:
            timer_for_falling = pygame.time.get_ticks()
            if figure_falling_time > 0:
                figure_falling_time -= 200

        # включение клавиши HOLD после падения фигуры
        if not figure_falling and not take_in_hold:
            if not can_take_in_hold:
                can_take_in_hold = True

        # проверка поставлена ли фигура или взятие фигуры в HOLD
        if not figure_falling:
            if not can_take_in_hold and figure_in_hold != "":
                current_figure, figure_in_hold = figure_in_hold, current_figure
                x, y = 3, 0
                can_take_in_hold = False
                take_in_hold = False
                figure_falling = True
                rotation_pos = 0
            else:
                if not take_in_hold:
                    for i in range(4):
                        rx, ry = figures_pos[current_figure][rotation_pos][i]
                        cup.cup[ry + y][rx + x] = current_figure
                else:
                    take_in_hold = False
                    figure_in_hold = current_figure

                x, y = 3, 0
                if len(figures_bag) == 1:
                    current_figure = figures_bag[0]
                    figures_bag.remove(current_figure)
                    figures_bag = figures_bag_next.copy()
                    shuffle(figures_bag_next)
                else:
                    current_figure = figures_bag[0]
                    figures_bag.remove(current_figure)

                figure_falling = True
                rotation = False
                rotation_pos = 0
                figure_placed_sound.play()

        # поворот фигуры
        if rotation:
            change_rotation = True
            if rotation_to_the == "right":
                new_index = rotation_pos + 1 if rotation_pos + 1 != 4 else 0
            else:
                new_index = rotation_pos - 1 if rotation_pos - 1 != -1 else 3
            for i in range(4):
                rx, ry = figures_pos[current_figure][new_index][i]
                if rx + x >= 10 or rx + x <= -1:
                    change_rotation = False
                    break
                if ry + y >= 20:
                    change_rotation = False
                    break
                if cup.cup[ry + y][rx + x] != 0:
                    change_rotation = False
                    break
            if change_rotation:
                rotation_pos = new_index
                rotate_figure_sound.play()
            rotation = False

        # отображение фигур в стакане
        for i in range(len(cup.cup)):
            for j in range(len(cup.cup[i])):
                if cup.cup[i][j] != 0:
                    pygame.draw.rect(screen, colors[cup.cup[i][j]], (
                        j * cup.cell_size + cup.left, i * cup.cell_size + cup.top, cup.cell_size, cup.cell_size))

        # отображение будущей постановки фигуры
        if not take_in_hold:
            current_y = y
            y_maxing = True
            while y_maxing and current_y < 20:
                for i in range(4):
                    rx, ry = figures_pos[current_figure][rotation_pos][i]
                    if ry + current_y + 1 < 20:
                        if cup.cup[ry + current_y + 1][rx + x] == 0:
                            y_maxing = True
                        else:
                            y_maxing = False
                            break
                    else:
                        y_maxing = False
                        break
                if y_maxing:
                    current_y += 1
            for i in range(4):
                rx, ry = figures_pos[current_figure][rotation_pos][i]
                pygame.draw.rect(screen, (49, 49, 49), (
                    (rx + x) * cup.cell_size + cup.left, (ry + current_y) * cup.cell_size + cup.top, cup.cell_size,
                    cup.cell_size))

        # отрисовка фигуры
        for i in range(4):
            rx, ry = figures_pos[current_figure][rotation_pos][i]
            pygame.draw.rect(screen, colors[current_figure], (
                (rx + x) * cup.cell_size + cup.left, (ry + y) * cup.cell_size + cup.top, cup.cell_size,
                cup.cell_size))

        # очистка линий и запись очков за них в SCORE
        cleared = 0
        for i in range(len(cup.cup)):
            if cup.cup[i].count(0) == 0:
                cleared += 1
                cup.cup.pop(i)
                cup.cup.insert(0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        if cleared + lines_cleared >= lines_required:
            lines_cleared = cleared + lines_cleared - lines_required
            lines_required += 2
            level += 1
        else:
            lines_cleared += cleared

        if cleared == 1:
            cup.score += 100 * level
            clear_line_sound.play()
        if cleared == 2:
            cup.score += 300 * level
            clear_lines_sound_1.play()
        if cleared == 3:
            cup.score += 500 * level
            clear_lines_sound_1.play()
        if cleared == 4:
            cup.score += 800 * level
            clear_lines_sound_2.play()

        # отображение фигур в поле HOLD
        if figure_in_hold != "":
            if can_take_in_hold:
                figure_in_hold_color = colors[figure_in_hold]
            else:
                figure_in_hold_color = (49, 49, 49)
            for i in range(4):
                minus_x, minus_y = 0, 0
                if figure_in_hold == "O" or figure_in_hold == "I":
                    minus_x = -15
                if figure_in_hold == "I":
                    minus_y = -15

                for rx, ry in figures_pos[figure_in_hold][0]:
                    pygame.draw.rect(screen, figure_in_hold_color,
                                     (rx * cup.cell_size + cup.left - cup.cell_size * 4 + minus_x,
                                      ry * cup.cell_size + cup.top + cup.cell_size + 5 + minus_y,
                                      cup.cell_size, cup.cell_size))

        # отображение фигур в поле NEXT
        if len(figures_bag) > 4:
            for i in range(5):
                minus_x, minus_y = 0, 0
                if figures_bag[i] == "O" or figures_bag[i] == "I":
                    minus_x = -15
                if figures_bag[i] == "I":
                    minus_y = -15
                for fig_pos in figures_pos[figures_bag[i]][0]:
                    pygame.draw.rect(screen, colors[figures_bag[i]], (
                        cup.left + cup.cell_size * (cup.width + 1 + fig_pos[0]) + minus_x,
                        cup.top + cup.cell_size * (2 + fig_pos[1]) - 25 + cup.cell_size * i * 3 + minus_y,
                        cup.cell_size, cup.cell_size))
        else:
            remains = 5 - len(figures_bag)
            for i in range(len(figures_bag)):
                minus_x, minus_y = 0, 0
                if figures_bag[i] == "O" or figures_bag[i] == "I":
                    minus_x = -15
                if figures_bag[i] == "I":
                    minus_y = -15
                for fig_pos in figures_pos[figures_bag[i]][0]:
                    pygame.draw.rect(screen, colors[figures_bag[i]], (
                        cup.left + cup.cell_size * (cup.width + 1 + fig_pos[0]) + minus_x,
                        cup.top + cup.cell_size * (2 + fig_pos[1]) - 25 + cup.cell_size * i * 3 + minus_y,
                        cup.cell_size, cup.cell_size))

            for i in range(remains):
                for fig_pos in figures_pos[figures_bag_next[i]][0]:
                    minus_x, minus_y = 0, 0
                    if figures_bag_next[i] == "O" or figures_bag_next[i] == "I":
                        minus_x = -15
                    if figures_bag_next[i] == "I":
                        minus_y = -15
                    pygame.draw.rect(screen, colors[figures_bag_next[i]], (
                        cup.left + cup.cell_size * (cup.width + 1 + fig_pos[0]) + minus_x,
                        cup.top + cup.cell_size * (2 + fig_pos[1]) - 25 + (
                                cup.cell_size * ((i + len(figures_bag)) * 3)) + minus_y,
                        cup.cell_size, cup.cell_size))

        # проверка на проигрыш
        if cup.cup[0].count(0) != 10:
            running = False
            pygame.mixer.music.stop()
            if cup.score < classic_mode_best_score:
                pygame.mixer.music.load("data/music/In-Sorrow-And-Pains_-Mirera-Loss-Music.mp3")
            else:
                pygame.mixer.music.load("data/music/Morning-Sun_-Kamoking-Win-Music.mp3")
            pygame.mixer.music.set_volume(music_volume)
            pygame.mixer.music.play(-1)
            cont = True if defeat_screen(cup.score) != "restart" else False
            if not cont:
                return "restart"
            else:
                return "menu"

        pygame.display.flip()
        clock.tick(fps)


mode = "menu"
cont = True
from_settings = False
while cont:
    if mode == "menu":
        mode = menu(from_settings)
        from_settings = False
    if mode == "play_button":
        mode = start_game()
        if mode == "restart":
            mode = "play_button"
        if mode == "escape":
            mode = "menu"
    if mode == "settings":
        mode = settings()
        from_settings = True
