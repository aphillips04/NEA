### Imports ###
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
levelBoundaries = [
    200,
    500,
    1000
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
    global name, current_screen, hero
    hero = load_player_data(usernameInputBox.text)
    if hero == None:
        print("no account with that name")
        ... # do a pop up window
    else:
        current_screen = village_screen
    
def newGame(obj):
    global current_screen
    if len(usernameInputBox.text) >= 3 and usernameInputBox.text.replace(" ", "").isalnum():
        current_screen = hero_selection
    else:
        print("name is invalid")
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

def heroPicked(obj):
    global hero, current_screen
    hero = heros[["mage", "paladin", "barbarian", "rogue"].index(obj.text.strip().split("\n")[0])]
    hero.name = usernameInputBox.text
    current_screen = village_screen

def hero_selection(event=None):
    if event == None:
        mageBtn.draw(win)
        paladinBtn.draw(win)
        barbarianBtn.draw(win)
        rogueBtn.draw(win)
    else:
        mageBtn.handle_event(event)
        paladinBtn.handle_event(event)
        barbarianBtn.handle_event(event)
        rogueBtn.handle_event(event)

def quitGame(obj):
    global run
    run = False

def progressBar(colour, x, y, width, height, progress):
    pygame.draw.rect(win, colour, (x, y, width*progress, height))
    pygame.draw.rect(win, (0,0,0), (x, y, width, height), 3)

def village_screen(event=None):
    if event == None:
        pygame.draw.rect(win, (0, 0, 0), (10, 10, 467.5, 1060), 5)
        win.blit(scaleImg(loadImg("imgs/placeholder.png"), (350*SCALEX,350*SCALEY)), (68, 20))
        progressBar((0,255,0), *scale_rect((30, 385, 427.5, 75)), hero.xp/levelBoundaries[hero.stats.level-1])
        font = pygame.font.Font("Imagine.ttf", int(45*(win.get_width()/1920)))
        for i, line in enumerate((f"Strength: {hero.stats.strength}\nAgility: {hero.stats.agility}\nMana: {hero.stats.mana}\n"+"\n".join(f"{weapontype}: {hero.items[weapontype].itemtype}" for weapontype in ["close", "range", "magical", "defence"])+f"\nGold: {hero.gold}").split("\n")):
            txt_surface = font.render(line, False, (0,0,0))
            win.blit(txt_surface, (20, 475+75*i))
        dungeonBtn.draw(win)
        wizardBtn.draw(win)
        blacksmithBtn.draw(win)
        quitBtn.draw(win)
    else:
        dungeonBtn.handle_event(event)
        wizardBtn.handle_event(event)
        blacksmithBtn.handle_event(event)
        quitBtn.handle_event(event)

def scale_rect(rect: Union[tuple, pygame.Rect]) -> pygame.Rect:
    return pygame.Rect(rect[0] * SCALEX, rect[1] * SCALEY, rect[2] * SCALEX, rect[3] * SCALEY)

# If playerdata doesn't exist, create and populate with an empty array
with open("playerdata.json", "r+") as f:
    if not f.read():
        json.dump({}, f, indent=4)

### Pygame Setup ###
pygame.init()
win = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), display=0)
clock = pygame.time.Clock()
run = True
frame = 0
current_screen = start_screen
hero = None

usernameInputBox = InputBox(*scale_rect((530, 200, 880, 109)), win, font="Imagine.ttf", font_size=141)
loadBtn = Button(*scale_rect((250, 650, 350, 200)), win, (179, 213, 224), "Load Game", font="Imagine.ttf", font_size=50, activated_func=loadGame)
newBtn = Button(*scale_rect((1320, 650, 350, 200)), win, (179, 213, 224), "New Game", font="Imagine.ttf", font_size=50, activated_func=newGame)

mageBtn = Button(*scale_rect((10, 10, 467.5, 1060)), win, (179, 213, 224), (" "*11)+f"mage\n\n\n\n\nStrength: {heros[0].stats.strength}\nAgility: {heros[0].stats.agility}\nMana: {heros[0].stats.mana}\n"+"\n".join(f"{weapontype}: {heros[0].items[weapontype].itemtype}" for weapontype in ["close", "range", "magical", "defence"]), font="Imagine.ttf", font_size=60, secondary_size=40, activated_func=heroPicked)
paladinBtn = Button(*scale_rect((487.5, 10, 467.5, 1060)), win, (179, 213, 224), (" "*8)+f"paladin\n\n\n\n\nStrength: {heros[1].stats.strength}\nAgility: {heros[1].stats.agility}\nMana: {heros[1].stats.mana}\n"+"\n".join(f"{weapontype}: {heros[1].items[weapontype].itemtype}" for weapontype in ["close", "range", "magical", "defence"]), font="Imagine.ttf", font_size=60, secondary_size=40, activated_func=heroPicked)
barbarianBtn = Button(*scale_rect((965, 10, 467.5, 1060)), win, (179, 213, 224), (" "*6)+f"barbarian\n\n\n\n\nStrength: {heros[2].stats.strength}\nAgility: {heros[2].stats.agility}\nMana: {heros[2].stats.mana}\n"+"\n".join(f"{weapontype}: {heros[2].items[weapontype].itemtype}" for weapontype in ["close", "range", "magical", "defence"]), font="Imagine.ttf", font_size=60, secondary_size=40, activated_func=heroPicked)
rogueBtn = Button(*scale_rect((1442.5, 10, 467.5, 1060)), win, (179, 213, 224), (" "*10)+f"rogue\n\n\n\n\nStrength: {heros[3].stats.strength}\nAgility: {heros[3].stats.agility}\nMana: {heros[3].stats.mana}\n"+"\n".join(f"{weapontype}: {heros[3].items[weapontype].itemtype}" for weapontype in ["close", "range", "magical", "defence"]), font="Imagine.ttf", font_size=60, secondary_size=40, activated_func=heroPicked)

dungeonBtn = Button(*scale_rect((800, 150, 300, 300)), win, (255, 255, 0), "dungeon", font="Imagine.ttf", font_size=50, activated_func=None)
wizardBtn = Button(*scale_rect((1300, 150, 300, 300)), win, (255, 255, 0), "wizards", font="Imagine.ttf", font_size=50, activated_func=None)
blacksmithBtn = Button(*scale_rect((800, 630, 300, 300)), win, (255, 255, 0), "black\nsmiths", font="Imagine.ttf", font_size=50, secondary_size=50, activated_func=None)
quitBtn = Button(*scale_rect((1300, 630, 300, 300)), win, (255, 255, 0), "Sleep", font="Imagine.ttf", font_size=50, activated_func=quitGame)

print(SCALEX, SCALEY)
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