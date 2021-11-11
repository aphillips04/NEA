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
    def __init__(self, x, y, w, h, screen, text='', font=None, font_size=32, return_func=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.FONT = pygame.font.Font(font, font_size*screen.get_height()//1080)
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
                if event.key == pygame.K_RETURN:
                    if self.return_func != None:
                        self.return_func()
                    else:
                        print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < 10:
                    self.text += event.unicode
                self.txt_surface = self.FONT.render(self.text, False, self.color)
    
    def scale_font(self, screen):
        twidth, theight = self.txt_surface.get_size()
        swidth, sheight = screen.get_size()
        self.txt_surface = pygame.transform.smoothscale(self.txt_surface, (twidth * swidth // 1920, theight * sheight // 1080))

    def draw(self, screen):
        #self.scale_font(screen)
        screen.blit(self.txt_surface, (self.rect.x, self.rect.y))
        pygame.draw.rect(screen, self.color, self.rect, 2)

class Button:
    def __init__(self, x, y, width, height, bg=(255, 255, 255), text="", font=None, font_size=32):
        self.rect = pygame.Rect(x, y, width, height)
        if type(bg) == str:
            self.bg = pygame.image.load(bg)
        elif type(bg) == tuple:
            self.bg = pygame.Surface((int(self.rect.width), int(self.rect.height)))
            self.bg.fill(bg)
        self.text = text
        self.FONT = pygame.font.Font(font, font_size)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.pressed()
    
    def pressed(self):
        ...

    def draw(self, win):
        win.blit(self.bg, self.rect)