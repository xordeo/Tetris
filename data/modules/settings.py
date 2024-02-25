import configparser
import os

thisfolder = os.path.dirname(os.path.abspath("config.ini"))
initfile = os.path.join(thisfolder, 'config.ini')

config = configparser.RawConfigParser()

config.read(initfile)

screen_size = width, height = config.getint("settings", "screen_width"), config.getint("settings", "screen_height")
fps = config.getint("settings", "FPS")
music_volume = config.getfloat("settings", "music_volume")
SFX_volume = config.getfloat("settings", "SFX_volume")
classic_mode_best_score = config.getint("score", "classic_mode_best_score")
