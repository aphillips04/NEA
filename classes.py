from dataclasses import dataclass
import json
from typing import Dict, List, Tuple, Union
import pygame;pygame.init()

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
        self.dungeonscleared = 0
        self.monsterscleared = 0
        self.bossescleared = 0

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
            ) for key in ("close", "range", "magical", "defence")},
            gold = self.gold,
            dungeonscleared = self.dungeonscleared
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
            ) for key in ("close", "range", "magical", "defence")},
            gold = self.gold,
            dungeonscleared = self.dungeonscleared
        )))

class Monster:
    def __init__(self, monstertype: str, attackname: str, defencename: str, levels: List[Stats]) -> None:
        self.monstertype = monstertype
        self.attackname = attackname
        self.defencename = defencename
        self.levels = levels

class InputBox:
    def __init__(self, x, y, w, h, win, text='', font=None, font_size=32, return_func=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.FONT = pygame.font.Font(font, int(font_size*(win.get_width()/1920)))
        self.color = pygame.Color("black")
        self.text = text
        self.txt_surface = self.FONT.render(text, False, self.color)
        self.active = False
        self.return_func = return_func

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < 10:
                    self.text += event.unicode
                self.txt_surface = self.FONT.render(self.text, False, self.color)

    def draw(self, win):
        win.blit(self.txt_surface, (self.rect.x+5, self.rect.y))
        pygame.draw.rect(win, self.color, self.rect, 3)

class Button:
    def __init__(self, x, y, width, height, win, bg=(255, 255, 255), text="", font=None, font_size=32, font_colour=(0, 0, 0), secondary_size=16, activated_func=None):
        self.rect = pygame.Rect(x, y, width, height)
        if type(bg) == str:
            self.bg = pygame.image.load(bg)
        elif type(bg) == tuple:
            self.bg = pygame.Surface((int(self.rect.width), int(self.rect.height)))
            self.bg.fill(bg)
        self.text = text
        self.font_size = font_size
        self.FONT = pygame.font.Font(font, int(font_size*(win.get_width()/1920)))
        self.FONT2 = pygame.font.Font(font, int(secondary_size*(win.get_width()/1920)))
        self.font_colour = font_colour
        self.activated_func = activated_func
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.activated_func != None:
                    self.activated_func(self)

    def draw(self, win):
        win.blit(self.bg, self.rect)
        for i, line in enumerate(self.text.split("\n")):
            if i < 1:
                txt_surface = self.FONT.render(line, False, self.font_colour)
            else:
                txt_surface = self.FONT2.render(line, False, self.font_colour)
            win.blit(txt_surface, (self.rect.x+10, self.rect.y-5+1.5*self.font_size*i))