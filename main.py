### Imports ###
from pygame.transform import scale
from classes import *

### Testing ###
TEST = Hero("Dev", "God", Stats("imgs/god.png", 1000, 100, 100, 100, 1000), {"close": Item("God Sword", "imgs/godsword.png", 1000),
     "range": Item("God Bow", "imgs/godbow.png", 1000), "magical": Item("God Staff", "imgs/godstaff.png", 1000), "defence": Item("God Armour", "imgs/godarmour.png", 1000)});TEST.xp = 1000;TEST.gold = 1000
TEST.save_progress()

### Constants ###
heros = [
    Hero(None, "Mage", Stats("imgs/mage.png", 1, 2, 3, 5, 10), dict(
        close = Item(None, None, None),
        range = Item("Bow", "imgs/bow.png", 1),
        magical = Item("Wand", "imgs/wand.png", 2),
        defence = Item("Leather", "imgs/leather.png", 1)
    )),
    Hero(None, "Paladin", Stats("imgs/paladin.png", 1, 4, 4, 2, 10), dict(
        close = Item("Short Sword", "imgs/short_sword.png", 1),
        range = Item(None, None, None),
        magical = Item("Amulet", "imgs/amulet.png", 1),
        defence = Item("Shield", "imgs/shield.png", 2)
    )),
    Hero(None, "Barbarian", Stats("imgs/barbarian.png", 1, 5, 4, 1, 10), dict(
        close = Item("Sword", "imgs/sword.png", 2),
        range = Item(None, None, None),
        magical = Item("Amulet", "imgs/amulet.png", 1),
        defence = Item("Leather", "imgs/leather.png", 1)
    )),
    Hero(None, "Rogue", Stats("imgs/rogue.png", 1, 2, 5, 3, 10), dict(
        close = Item(None, None, None),
        range = Item("Crossbow", "imgs/crossbow.png", 2),
        magical = Item("Amulet", "imgs/amulet.png", 1),
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
loadImg = pygame.image.load
scaleImg = pygame.transform.scale
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

def loadGame(obj):
    global name, current_screen
    hero = load_player_data(obj.text)
    if hero == None:
        ... # do a pop up window
    else:
        current_screen = village_screen
    
def newGame(obj):
    global current_screen
    if len(obj.text) > 3 and obj.text.replace(" ", "").isalnum():
        current_screen = hero_selection
    else:
        ... # do a pop up window

def start_screen(event=None):
    if event == None:
        usernameInputBox.draw(win)
        loadBtn.draw(win)
        newBtn.draw(win)
    else:
        usernameInputBox.handle_event(event)
        loadBtn.handle_event(event)
        newBtn.handle_event(event)

def hero_picked(obj):
    global hero, current_screen
    hero = heros[heros.index(obj.text.split("\n")[0])]
    hero.name = usernameInputBox.text
    current_screen = village_screen

def hero_selection(event=None):
    if event == None:
        for i, btn in enumerate(["mage", "paladin", "barbarian", "rogue"]):
            locals()[btn+"Btn"] = Button(*scale_rect((10+477.5*i, 10, 467.5, 1060)), win, (254, 165, 136), " "*(15-len(btn))+f"{btn}\n\n\n\n\n\nStrength: {heros[i].stats.strength}\nAgility: {heros[i].stats.agility}\nMana: {heros[i].stats.mana}\n"+"\n".join(f"{weapontype}: {heros[i].items[weapontype].itemtype}" for weapontype in ["close", "range", "magical", "defence"]), font="Imagine.ttf", font_size=60, secondary_size=40, activated_func=hero_picked)
            locals()[btn+"Btn"].draw(win)
            win.blit(scaleImg(loadImg(heros[i].stats.icon), (450, 450)), scale_rect((20+477.5*i, 25, 0, 0)))
    else:
        try:
            for i, btn in enumerate(["mage", "paladin", "barbarian", "rogue"]):
                locals()[btn+"Btn"].handle_event(event)
        except KeyError:
            pass

def village_screen(event=None):
    if event == None:
        print(hero)
        exit(0)
    else:
        ...

def scale_rect(rect: Union[tuple, pygame.Rect]) -> pygame.Rect:
    return pygame.Rect(rect[0] * SCALEX, rect[1] * SCALEY, rect[2] * SCALEX, rect[3] * SCALEY)


# If playerdata doesn't exist, create and populate with an empty array
with open("playerdata.json", "r+") as f:
    if not f.read():
        json.dump({}, f, indent=4)

### Pygame Setup ###
pygame.init()
win = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h))
clock = pygame.time.Clock()
run = True
frame = 0
current_screen = start_screen
hero = None

usernameInputBox = InputBox(*scale_rect((530, 200, 880, 109)), win, font="Imagine.ttf", font_size=141)
loadBtn = Button(*scale_rect((250, 650, 350, 200)), win, (254, 165, 136), "Load Game", font="Imagine.ttf", font_size=50, activated_func=loadGame)
newBtn = Button(*scale_rect((1320, 650, 350, 200)), win, (254, 165, 136), "New Game", font="Imagine.ttf", font_size=50, activated_func=newGame)

while run:
    frame = (frame + 1) % 60
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        current_screen(event)

    win.fill(pygame.color.THECOLORS["white"])
    current_screen()
    pygame.display.update()

pygame.quit()