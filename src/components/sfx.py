from enum import Enum
import pygame

SHIP_EXPLOSION = "ship_explosion"
ASTEROID_EXPLOSION = "asteroid_explosion"
LASER = "laser"
SELECT = "select"
THRUSTER = "thruster"
SOUND = "sound"
PLAYING = "playing"
CHANNEL = "channel"
MODE = "mode"

class SoundMode(Enum):
    SINGLE = 1
    SLOW = 2
    NORMAL = 3

class Sfx:
    BGM_SOURCE = "sounds/bgm.mp3"
    effects = {
        SHIP_EXPLOSION: {
            SOUND: pygame.mixer.Sound("sounds/explosion_player.ogg"),
            CHANNEL: None,
            PLAYING: False,
            MODE: None,
        },
        ASTEROID_EXPLOSION: {
            SOUND: pygame.mixer.Sound("sounds/explosion_asteroid.ogg"),
            CHANNEL: None,
            PLAYING: False,
            MODE: None,
        },
        LASER: {
            SOUND: pygame.mixer.Sound("sounds/laser.ogg"),
            CHANNEL: None,
            PLAYING: False,
            MODE: None,
        },
        SELECT: {
            SOUND: pygame.mixer.Sound("sounds/option_select.ogg"),
            CHANNEL: None,
            PLAYING: False,
            MODE: None,
        },
        THRUSTER: {
            SOUND: pygame.mixer.Sound("sounds/thruster_loud.ogg"),
            CHANNEL: None,
            PLAYING: False,
            MODE: None,
        },
    }

    def __init__(self, config = {}):
        self.bgm_volume = config.get("bgmVolume", 0.1)
        self.bgm_on = config.get("bgmOn", True)
        self.sfx_volume = config.get("sfxVolume", 0.4)
        self.sfx_on = config.get("sfxOn", True)
        self.fx_played = False

        self.load_bgm()

    def load_bgm(self):
        pygame.mixer.music.load(self.BGM_SOURCE)
        pygame.mixer.music.set_volume(self.bgm_volume)

    def play_bgm(self):
        if self.bgm_on:
            pygame.mixer.music.play(-1, fade_ms = 5_000)

    def stop_bgm(self):
        pygame.mixer.music.stop()

    def stop_sfx(self, effect):
        if not self.effects.get(effect):
            return

        if self.effects[effect][PLAYING]:
            self.effects[effect][PLAYING] = False
            sound: pygame.mixer.Sound = self.effects[effect][SOUND]
            sound.stop()

    def play_sfx(self, effect, mode = SoundMode.NORMAL):
        if not self.sfx_on or not self.effects.get(effect):
            return

        if mode == SoundMode.SINGLE:
            if not self.fx_played:
                self.fx_played = True

                if not self.effects[effect][PLAYING]:
                    self.effects[effect][PLAYING] = True

                    sound: pygame.mixer.Sound = self.effects[effect][SOUND]
                    sound.set_volume(self.sfx_volume)
                    self.effects[effect][CHANNEL] = sound.play()
        elif mode == SoundMode.SLOW:
            if not self.effects[effect][PLAYING]:
                self.effects[effect][PLAYING] = True

                sound: pygame.mixer.Sound = self.effects[effect][SOUND]
                sound.set_volume(self.sfx_volume)
                self.effects[effect][CHANNEL] = sound.play()
        elif mode == SoundMode.NORMAL:
            self.stop_sfx(effect)

            self.effects[effect][PLAYING] = True
            sound: pygame.mixer.Sound = self.effects[effect][SOUND]
            sound.set_volume(self.sfx_volume)
            self.effects[effect][CHANNEL] = sound.play()

    def update(self):
        for _, item in self.effects.items():
            if item[PLAYING]:
                channel : pygame.mixer.Channel = item[CHANNEL]
                if channel is None or not channel.get_busy():
                    item[PLAYING] = False

    