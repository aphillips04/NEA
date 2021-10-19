from dataclasses import dataclass
import json
from typing import Dict, List, Tuple, Union
import pygame
from pygame.constants import CONTROLLER_BUTTON_RIGHTSHOULDER, TIMER_RESOLUTION;pygame.init()

@dataclass
class Stats:
    icon: str
    level: int
    strength: int
    agility: int
    mana: int
    health: int

@dataclass
class Item:
    itemtype: str
    icon: str
    level: int

class Hero:
    def __init__(self, name: str, herotype: str, stats: Stats, items: Dict[str, Item]) -> None:
        self.name = name
        self.herotype = herotype
        self.stats = stats
        self.xp = 0
        self.items = items
        self.gold = 0

    def save_progress(self) -> None:
        with open("playerdata.json", "r") as f:
            data = json.load(f)
        data[self.name] = dict(
            herotype = self.herotype,
            stats = dict(
                icon = self.stats.icon,
                level = self.stats.level,
                strength = self.stats.strength,
                agility = self.stats.agility,
                mana = self.stats.mana,
                health = self.stats.health
            ),
            xp = self.xp,
            items = {key: dict(
                itemtype = self.items[key].itemtype,
                icon = self.items[key].icon,
                level = self.items[key].level
            ) for key in ("close", "range", "mana", "defence")},
            gold = self.gold
        )
        with open("playerdata.json", "w") as f:
            json.dump(data, f, indent=4)
    
    def __repr__(self):
        return str(json.dumps(dict(
            herotype = self.herotype,
            stats = dict(
                level = self.stats.level,
                icon = self.stats.icon,
                strength = self.stats.strength,
                agility = self.stats.agility,
                mana = self.stats.mana,
                health = self.stats.health
            ),
            xp = self.xp,
            items = {key: dict(
                itemtype = self.items[key].itemtype,
                icon = self.items[key].icon,
                level = self.items[key].level
            ) for key in ("close", "range", "mana", "defence")},
            gold = self.gold
        )))

class Monster:
    def __init__(self, monstertype: str, levels: List[Stats]) -> None:
        self.monstertype = monstertype
        self.levels = levels

class InputBox:
    def __init__(self, x, y, w, h, text='', font=None, font_size=32):
        self.rect = pygame.Rect(x, y, w, h)
        self.FONT = pygame.font.Font(font, font_size)
        self.color = pygame.Color("black")
        self.text = text
        self.txt_surface = self.FONT.render(text, False, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < 11:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.FONT.render(self.text, False, self.color)

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x, self.rect.y))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

class Button:
    def __init__(self, x, y, width, height, bg=(255, 255, 255), text="", font=None, font_size=32):
        self.rect = pygame.Rect(x, y, width, height)
        self.bg = bg
        self.text = text
        self.FONT = pygame.font.Font(font, font_size)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.pressed()
    
    def pressed(self):
        ...

    def draw(self, win):
        win.blit(self.bg)