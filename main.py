### Imports ###
import json
from classes import *
import pygame;pygame.init()

### Testing ###
# TEST = Hero("Dev", "God", Stats("imgs/god.png", 1000, 100, 100, 100, 1000), {"close": Item("God Sword", "imgs/godsword.png", 1000),
#     "range": Item("God Bow", "imgs/godbow.png", 1000), "mana": Item("God Staff", "imgs/godstaff.png", 1000), "defence": Item("God Armour", "imgs/godarmour.png", 1000)});TEST.xp = 1000;TEST.gold = 1000
# TEST.save_progress()

### Constants ###
heros = [
    Hero(None, "Mage", Stats("imgs/mage.png", 1, 2, 3, 5, 10), dict(
        close = None,
        range = Item("Bow", "imgs/bow.png", 1),
        mana = Item("Wand", "imgs/wand.png", 2),
        defence = Item("Leather", "imgs/leather.png", 1)
    )),
    Hero(None, "Paladin", Stats("imgs/paladin.png", 1, 4, 4, 2, 10), dict(
        close = Item("Short Sword", "imgs/short_sword.png", 1),
        range = None,
        mana = Item("Amulet", "imgs/amulet.png", 1),
        defence = Item("Shield", "imgs/shield.png", 2)
    )),
    Hero(None, "Barbarian", Stats("imgs/barbarian.png", 1, 5, 4, 1, 10), dict(
        close = Item("Sword", "imgs/sword.png", 2),
        range = None,
        mana = Item("Amulet", "imgs/amulet.png", 1),
        defence = Item("Leather", "imgs/leather.png", 1)
    )),
    Hero(None, "Rogue", Stats("imgs/rogue.png", 1, 2, 5, 3, 10), dict(
        close = None,
        range = Item("Crossbow", "imgs/crossbow.png", 2),
        mana = Item("Amulet", "imgs/amulet.png", 1),
        defence = Item("Leather", "imgs/leather.png", 1)
    ))
]
monsters = [
    Monster("Witch", [Stats("imgs/witch.png", 1, 1, 1, 3, 5), Stats("imgs/witch.png", 2, 2, 2, 4, 5), Stats("imgs/witch.png", 3, 2, 2, 4, 10)]),
    Monster("Orc", [Stats("imgs/orc.png", 1, 1, 3, 1, 5), Stats("imgs/orc.png", 2, 2, 4, 2, 5), Stats("imgs/orc.png", 3, 2, 4, 2, 10)]),
    Monster("Ogre", [Stats("imgs/ogre.png", 1, 4, 1, 0, 5), Stats("imgs/ogre.png", 2, 5, 3, 0, 5), Stats("imgs/ogre.png", 3, 5, 3, 0, 10)]),
    Monster("Troll", [Stats("imgs/troll.png", 1, 3, 1, 1, 5), Stats("imgs/troll.png", 2, 4, 2, 2, 5), Stats("imgs/troll.png", 3, 4, 2, 2, 10)]),
    Monster("Wolf", [Stats("imgs/wolf.png", 1, 2, 3, 0, 5), Stats("imgs/wolf.png", 2, 4, 4, 0, 5), Stats("imgs/wolf.png", 3, 4, 4, 0, 10)])
]
bosses = [
    Monster("Dragon", [Stats("imgs/dragon.png", 4, 7, 2, 3, 15)]),
    Monster("Demon", [Stats("imgs/demon.png", 4, 4, 2, 6, 15)]),
    Monster("Basalisk", [Stats("imgs/basalisk.png", 4, 4, 4, 4, 15)])
]
SCALEX = pygame.display.Info().current_w / 1920
SCALEY = pygame.display.Info().current_h / 1080
FPS = 60

### Functions ###
def load_player_data(name: str) -> Hero:
    with open("playerdata.json", "r") as f:
        data = json.load(f)
    if name not in data.keys():
        return None
    playerdata = data[name]
    hero = Hero(name, playerdata["herotype"], Stats(**playerdata["stats"]), {key: Item(**playerdata["items"][key]) for key in playerdata["items"]})
    hero.xp = playerdata["xp"]
    hero.gold = playerdata["gold"]
    return hero

def scale_rect(rect: pygame.Rect) -> pygame.Rect:
    return pygame.Rect(rect.left * SCALEX, rect.top * SCALEY, rect.width * SCALEX, rect.height * SCALEY)

def draw():
    win.fill(pygame.color.THECOLORS["white"])

    pygame.draw.rect(win, pygame.color.THECOLORS["red"], scale_rect(pygame.Rect(250, 175, 250, 150)))

# If playerdata doesn't exist, create populate with an empty array
with open("playerdata.json", "r+") as f:
    if not f.read():
        json.dump({}, f, indent=4)

### Pygame Setup ###
win = pygame.display.set_mode((1200, 675), pygame.FULLSCREEN)
clock = pygame.time.Clock()
run = True

while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False  
    
    draw()
    pygame.display.update()

pygame.quit()