### Imports ###
from tkinter.constants import W
from classes import *
import random
from copy import deepcopy
import tkinter as tk
import tkinter.messagebox as mb
tk.Tk().wm_withdraw()

### Testing ###
TEST = Hero("Dev", "God", Stats("imgs/god.png", 1000, 100, 100, 100, 1000), {"close": Item("God Sword", "imgs/godsword.png", 1000),
     "range": Item("God Bow", "imgs/godbow.png", 1000), "magical": Item("God Staff", "imgs/godstaff.png", 1000), "defence": Item("God Armour", "imgs/godarmour.png", 1000)});TEST.xp = 1000;TEST.gold = 1000;TEST.dungeonscleared = 1000
TEST.save_progress()

### Constants ###
items = dict(
    none = Item(None, None, None),
    shortsword = Item("Short Sword", "imgs/short_sword.png", 1),
    sword = Item("Sword", "imgs/sword.png", 2),
    broadsword = Item("Broad Sword", "imgs/broad_sword.png", 3),
    bow = Item("Bow", "imgs/bow.png", 1),
    crossbow = Item("Crossbow", "imgs/crossbow.png", 2),
    longbow = Item("Long Bow", "imgs/long_bow.png", 3),
    amulet = Item("Amulet", "imgs/amulet.png", 1),
    wand = Item("Wand", "imgs/wand.png", 2),
    staff = Item("Staff", "imgs/staff.png", 3),
    leather = Item("Leather", "imgs/leather.png", 1),
    chainmail = Item("Chain Mail", "imgs/chain_mail.png", 2),
    plate = Item("plate", "imgs/plate_armour.png", 3)
)
heros = [
    Hero(None, "Mage", Stats("imgs/mage.png", 1, 2, 3, 5, 10), dict(
        close = items["none"],
        range = items["bow"],
        magical = items["wand"],
        defence = items["leather"]
    )),
    Hero(None, "Paladin", Stats("imgs/paladin.png", 1, 4, 4, 2, 10), dict(
        close = items["sword"],
        range = items["none"],
        magical = items["amulet"],
        defence = items["chainmail"]
    )),
    Hero(None, "Barbarian", Stats("imgs/barbarian.png", 1, 5, 4, 1, 10), dict(
        close = items["sword"],
        range = items["none"],
        magical = items["amulet"],
        defence = items["leather"]
    )),
    Hero(None, "Rogue", Stats("imgs/rogue.png", 1, 2, 5, 3, 10), dict(
        close = items["none"],
        range = items["crossbow"],
        magical = items["amulet"],
        defence = items["leather"]
    ))
]
monsters = [
    Monster("Witch", "Curse", "Potion", [Stats("imgs/witch.png", 1, 3, 1, 0, 5), Stats("imgs/witch.png", 2, 4, 2, 0, 5), Stats("imgs/witch.png", 3, 4, 2, 0, 10)]),
    Monster("Orc", "Gnaw", "Thicc Skin", [Stats("imgs/orc.png", 1, 1, 3, 0, 5), Stats("imgs/orc.png", 2, 2, 4, 0, 5), Stats("imgs/orc.png", 3, 2, 4, 0, 10)]),
    Monster("Ogre", "Smash", "Rock Fist", [Stats("imgs/ogre.png", 1, 4, 1, 0, 5), Stats("imgs/ogre.png", 2, 5, 3, 0, 5), Stats("imgs/ogre.png", 3, 5, 3, 0, 10)]),
    Monster("Troll", "Club", "Parry", [Stats("imgs/troll.png", 1, 3, 1, 0, 5), Stats("imgs/troll.png", 2, 4, 2, 0, 5), Stats("imgs/troll.png", 3, 4, 2, 0, 10)]),
    Monster("Wolf", "Gorge", "Dodge", [Stats("imgs/wolf.png", 1, 2, 3, 0, 5), Stats("imgs/wolf.png", 2, 4, 4, 0, 5), Stats("imgs/wolf.png", 3, 4, 4, 0, 10)])
]
bosses = [
    Monster("Dragon", "Fire Breath", "Slippery Scale", [Stats("imgs/dragon.png", 4, 7, 2, 0, 15)]*3),
    Monster("Demon", "Putrify", "Dissipate", [Stats("imgs/demon.png", 4, 6, 2, 0, 15)]*3),
    Monster("Basalisk", "Poison Spit", "Constrict", [Stats("imgs/basalisk.png", 4, 4, 4, 4, 15)]*3)
]
dungeonMonsters = [
    (5, 0),
    (7, 0),
    (9, 0),
    (9, 1)
]
levelBoundaries = [
    200,
    500,
    1000
]
maxHealths = [
    10,
    15,
    20
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
    hero.dungeonscleared = playerdata["dungeonscleared"]
    return hero

def loadGame(obj):
    global name, current_screen, hero
    hero = load_player_data(usernameInputBox.text)
    if hero == None:
        mb.showerror("Missing Account", f"No account saved with the name \"{usernameInputBox.text}\"")
    else:
        current_screen = village_screen
    
def newGame(obj):
    global current_screen
    if len(usernameInputBox.text) >= 3 and usernameInputBox.text.replace(" ", "").isalnum():
        current_screen = hero_selection
    else:
        if len(usernameInputBox.text) < 3 and usernameInputBox.text.replace(" ", "").isalnum():
            mb.showerror("Invalid Account Name", f"\"{usernameInputBox.text}\" is too short (less than 3 characters)")
        elif len(usernameInputBox.text) >= 3 and not usernameInputBox.text.replace(" ", "").isalnum():
            mb.showerror("Invalid Account Name", f"\"{usernameInputBox.text}\" contains invalid characters (~`!@#$%^&*()-_+=\\{'{}'}[]|\;:\"<>,./?")
        else:
            mb.showerror("Invalid Account Name", f"\"{usernameInputBox.text}\" is too short (less than 3 characters) and contains invalid characters (~`!@#$%^&*()-_+=\\{'{}'}[]|\;:\"<>,./?")

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

def dungeonEntrance(obj):
    global current_screen
    current_screen = dugeon_screen

def wizardsShop(obj):
    global current_screen
    current_screen = wizards_screen

def blacksmithsShop(obj):
    global current_screen
    current_screen = blacksmiths_screen

def quitGame(obj):
    global run
    surequit = mb.askyesno("Quit?", "Are you sure you want to quit the game?")
    if surequit:
        run = False

def progressBar(colour, x, y, width, height, progress, text="", font=None, font_size=32):
    pygame.draw.rect(win, colour, (x, y, width*progress, height))
    pygame.draw.rect(win, (0,0,0), (x, y, width, height), 3)
    font = pygame.font.Font(font, int(font_size*(win.get_width()/1920)))
    win.blit(font.render(text, False, (0,0,0)), (x+10, y+5))

def village_screen(event=None):
    global run
    if event == None:
        pygame.draw.rect(win, (0, 0, 0), (10, 10, 467.5, 1060), 5)
        win.blit(scaleImg(loadImg(hero.stats.icon), (350*SCALEX,350*SCALEY)), (68, 20))
        progressBar((0,255,0), *scale_rect((30, 385, 427.5, 75)), hero.xp/levelBoundaries[hero.stats.level-1], f"{hero.xp}/{levelBoundaries[hero.stats.level-1]}", "Imagine.ttf", 50)
        font = pygame.font.Font("Imagine.ttf", int(45*(win.get_width()/1920)))
        for i, line in enumerate((f"Strength: {hero.stats.strength}\nAgility: {hero.stats.agility}\nMana: {hero.stats.mana}\n"+"\n".join(f"{weapontype}: {hero.items[weapontype].itemtype}" for weapontype in ["close", "range", "magical", "defence"])+f"\nGold: {hero.gold}").split("\n")):
            txt_surface = font.render(line, False, (0,0,0))
            win.blit(txt_surface, (20, 475+75*i))
        dungeonBtn.draw(win)
        wizardBtn.draw(win)
        blacksmithBtn.draw(win)
        quitBtn.draw(win)
        if hero.dungeonscleared == len(dungeonMonsters) and frame >= 15:
            mb.showinfo("You Win!", "Congratulations, you beat the game! Thanks for playing!")
            hero.dungeonscleared = len(dungeonMonsters)+1
    else:
        if hero.dungeonscleared < len(dungeonMonsters):
            dungeonBtn.handle_event(event)
            wizardBtn.handle_event(event)
            blacksmithBtn.handle_event(event)
        quitBtn.handle_event(event)

def toVillage(obj):
    global current_screen, hero
    hero.stats.health = maxHealths[hero.stats.level-1]
    hero.monsterscleared = 0
    hero.bossescleared = 0
    current_screen = village_screen
    hero.save_progress()

def blacksmiths_screen(event=None):
    if event == None:
        pygame.draw.rect(win, (0, 0, 0), (10, 10, 467.5, 1060), 5)
        win.blit(scaleImg(loadImg(hero.stats.icon), (350*SCALEX,350*SCALEY)), (68, 20))
        progressBar((0,255,0), *scale_rect((30, 385, 427.5, 75)), hero.xp/levelBoundaries[hero.stats.level-1], f"{hero.xp}/{levelBoundaries[hero.stats.level-1]}", "Imagine.ttf", 50)
        title = pygame.font.Font("Imagine.ttf", int(125*(win.get_width()/1920)))
        win.blit(title.render("Blacksmiths", False, (0,0,0)), (810, 7.5))
        font = pygame.font.Font("Imagine.ttf", int(45*(win.get_width()/1920)))
        for i, line in enumerate((f"Health: {hero.stats.health}/{maxHealths[hero.stats.level-1]}\nGold: {hero.gold}").split("\n")):
            txt_surface = font.render(line, False, (0,0,0))
            win.blit(txt_surface, (20, 475+75*i))
        shortswordBtn.draw(win)
        bowBtn.draw(win)
        leatherBtn.draw(win)
        swordBtn.draw(win)
        crossbowBtn.draw(win)
        chainmailBtn.draw(win)
        broadswordBtn.draw(win)
        longbowBtn.draw(win)
        plateBtn.draw(win)
        backBtn.draw(win)
        win.blit(scaleImg(loadImg("imgs/back.png"), (50*SCALEX,50*SCALEY)), (1857.5, 7.5))
    else:
        shortswordBtn.handle_event(event)
        bowBtn.handle_event(event)
        leatherBtn.handle_event(event)
        swordBtn.handle_event(event)
        crossbowBtn.handle_event(event)
        chainmailBtn.handle_event(event)
        broadswordBtn.handle_event(event)
        longbowBtn.handle_event(event)
        plateBtn.handle_event(event)
        backBtn.handle_event(event)

def wizards_screen(event=None):
    if event == None:
        pygame.draw.rect(win, (0, 0, 0), (10, 10, 467.5, 1060), 5)
        win.blit(scaleImg(loadImg(hero.stats.icon), (350*SCALEX,350*SCALEY)), (68, 20))
        progressBar((0,255,0), *scale_rect((30, 385, 427.5, 75)), hero.xp/levelBoundaries[hero.stats.level-1], f"{hero.xp}/{levelBoundaries[hero.stats.level-1]}", "Imagine.ttf", 50)
        title = pygame.font.Font("Imagine.ttf", int(125*(win.get_width()/1920)))
        win.blit(title.render("Wizards", False, (0,0,0)), (960, 7.5))
        font = pygame.font.Font("Imagine.ttf", int(45*(win.get_width()/1920)))
        for i, line in enumerate((f"Health: {hero.stats.health}/{maxHealths[hero.stats.level-1]}\nGold: {hero.gold}").split("\n")):
            txt_surface = font.render(line, False, (0,0,0))
            win.blit(txt_surface, (20, 475+75*i))
        amuletBtn.draw(win)
        wandBtn.draw(win)
        staffBtn.draw(win)
        backBtn.draw(win)
        win.blit(scaleImg(loadImg("imgs/back.png"), (50*SCALEX,50*SCALEY)), (1857.5, 7.5))
    else:
        amuletBtn.handle_event(event)
        wandBtn.handle_event(event)
        staffBtn.handle_event(event)
        backBtn.handle_event(event)

def doAttack(obj):
    global monster, hero, current_screen
    if hero.items[obj.text].itemtype != None:
        dmg = (random.randint(0, 3) + (hero.stats.strength if obj.text != "magical" else hero.stats.mana) // 2 + hero.items[obj.text].level) - monster.levels[hero.stats.level-1].agility
        if dmg >= 0:
            monster.levels[hero.stats.level-1].health -= dmg
        if monster.levels[hero.stats.level-1].health > 0:
            dmg = (monster.levels[hero.stats.level-1].strength + random.randint(0, 3)) - ((hero.stats.agility // (5-hero.stats.level)) + hero.items["defence"].level)
            if dmg >= 0:
                hero.stats.health -= dmg
            if hero.stats.health <= 0:
                hero.gold = 0
                hero.stats.health = 5 + hero.stats.level*5
                toVillage(None)
        else:
            monster = None
            hero.gold += 5

def fleeFight(obj):
    global current_screen
    sureflee = mb.askyesno("Flee?", f"Are you sure you want to flee, you will drop {min(hero.stats.level, hero.gold)} gold in the process?")
    if sureflee:
        if hero.gold >= hero.stats.level:
            hero.gold -= hero.stats.level
        else:
            hero.gold = 0
        toVillage(None)

def dugeon_screen(event=None):
    global monster, hero
    if event == None:
        if monster == None and hero.monsterscleared < dungeonMonsters[hero.dungeonscleared][0]:
            dugeon_screen.monsterIndex = random.randint(0, len(monsters)-1)
            monster = deepcopy(monsters[dugeon_screen.monsterIndex])
            hero.monsterscleared += 1
        elif monster == None and hero.bossescleared < dungeonMonsters[hero.dungeonscleared][1]:
            dugeon_screen.monsterIndex = random.randint(0, len(bosses)-1)
            monster = deepcopy(bosses[dugeon_screen.monsterIndex])
            hero.bossescleared += 1
        elif monster != None:
            pygame.draw.rect(win, (0, 0, 0), (10, 10, 467.5, 1060), 5)
            win.blit(scaleImg(loadImg(hero.stats.icon), (350*SCALEX,350*SCALEY)), (68, 20))
            progressBar((0,255,0), *scale_rect((30, 385, 427.5, 75)), hero.xp/levelBoundaries[hero.stats.level-1], f"{hero.xp}/{levelBoundaries[hero.stats.level-1]}", "Imagine.ttf", 50)
            title = pygame.font.Font("Imagine.ttf", int(125*(win.get_width()/1920)))
            win.blit(title.render(monster.monstertype, False, (0,0,0)), (1010, 7.5))
            win.blit(scaleImg(loadImg(monster.levels[hero.stats.level-1].icon), (450*SCALEX,450*SCALEY)), (950, 225))
            if hero.bossescleared == 0:
                progressBar((255,0,0), *scale_rect((950, 700, 450, 75)), monster.levels[hero.stats.level-1].health/monsters[dugeon_screen.monsterIndex].levels[hero.stats.level-1].health, f"{monster.levels[hero.stats.level-1].health}/{monsters[dugeon_screen.monsterIndex].levels[hero.stats.level-1].health}", "Imagine.ttf", 50)
            else:
                progressBar((0,0,255), *scale_rect((950, 700, 450, 75)), monster.levels[hero.stats.level-1].health/bosses[dugeon_screen.monsterIndex].levels[hero.stats.level-1].health, f"{monster.levels[hero.stats.level-1].health}/{bosses[dugeon_screen.monsterIndex].levels[hero.stats.level-1].health}", "Imagine.ttf", 50)
            monsterFont = pygame.font.Font("Imagine.ttf", int(90*(win.get_width()/1920)))
            win.blit(monsterFont.render(f"{monsters[dugeon_screen.monsterIndex].attackname}     +{monster.levels[hero.stats.level-1].strength}", False, (0,0,0)), (950, 800))
            win.blit(monsterFont.render(f"{monsters[dugeon_screen.monsterIndex].defencename}     +{monster.levels[hero.stats.level-1].agility}", False, (0,0,0)), (950, 900))
            closeBtn.draw(win)
            rangeBtn.draw(win)
            magicBtn.draw(win)
            fleeBtn.draw(win)
            font = pygame.font.Font("Imagine.ttf", int(45*(win.get_width()/1920)))
            for i, line in enumerate((f"Difficulty: {['Easy', 'Medium', 'Hard', 'Boss'][hero.dungeonscleared]}\nHealth: {hero.stats.health}/{maxHealths[hero.stats.level-1]}\nGold: {hero.gold}\n {hero.items['close'].itemtype if hero.items['close'].itemtype != None else ''}\n {hero.items['range'].itemtype if hero.items['range'].itemtype != None else ''}\n {hero.items['magical'].itemtype if hero.items['magical'].itemtype != None else ''}\n Flee").split("\n")):
                txt_surface = font.render(line, False, (0,0,0))
                win.blit(txt_surface, (20, 475+75*i))
        else:
            if hero.stats.level <= len(levelBoundaries) and hero.dungeonscleared < len(dungeonMonsters)-1:
                hero.xp += 5*dungeonMonsters[hero.dungeonscleared][0]
                hero.xp += 15*dungeonMonsters[hero.dungeonscleared][1]
                if hero.stats.level == len(levelBoundaries):
                    hero.xp = levelBoundaries[-1]
                elif hero.xp >= levelBoundaries[hero.stats.level-1]:
                    hero.stats.level += 1
                hero.dungeonscleared = (hero.dungeonscleared + 1) % 4
            else:
                hero.dungeonscleared += 1
            toVillage(None)
    else:
        closeBtn.handle_event(event)
        rangeBtn.handle_event(event)
        magicBtn.handle_event(event)
        fleeBtn.handle_event(event)

def purchase(obj):
    global hero
    item = obj.text.split("\n")[0].replace(" ", "")
    cost = int(obj.text.split("\n")[1].split(" ")[1])
    if hero.gold >= cost:
        hero.gold -= cost
        if item in ["shortsword", "sword", "broadsword"]:
            hero.items["close"] = items[item]
        elif item in ["bow", "crossbow", "longbow"]:
            hero.items["range"] = items[item]
        elif item in ["amulet", "wand", "staff"]:
            hero.items["magical"] = items[item]
        elif item in ["leather", "chaimail", "plate"]:
            hero.items["defence"] = items[item]
        hero.save_progress()
    else:
        mb.showerror("Insufficient Funds", f"You are missing {cost-hero.gold} gold required to buy a \"{item}\"")

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
monster = None

### Visual Entities to be drawn ###
# Start Screen
usernameInputBox = InputBox(*scale_rect((530, 200, 880, 109)), win, font="Imagine.ttf", font_size=141)
loadBtn = Button(*scale_rect((250, 650, 350, 200)), win, (179, 213, 224), "Load Game", font="Imagine.ttf", font_size=50, activated_func=loadGame)
newBtn = Button(*scale_rect((1320, 650, 350, 200)), win, (179, 213, 224), "New Game", font="Imagine.ttf", font_size=50, activated_func=newGame)

# Hero Selection
mageBtn = Button(*scale_rect((10, 10, 467.5, 1060)), win, (179, 213, 224), (" "*11)+f"mage\n\n\n\n\nStrength: {heros[0].stats.strength}\nAgility: {heros[0].stats.agility}\nMana: {heros[0].stats.mana}\n"+"\n".join(f"{weapontype}: {heros[0].items[weapontype].itemtype}" for weapontype in ["close", "range", "magical", "defence"]), font="Imagine.ttf", font_size=60, secondary_size=40, activated_func=heroPicked)
paladinBtn = Button(*scale_rect((487.5, 10, 467.5, 1060)), win, (179, 213, 224), (" "*8)+f"paladin\n\n\n\n\nStrength: {heros[1].stats.strength}\nAgility: {heros[1].stats.agility}\nMana: {heros[1].stats.mana}\n"+"\n".join(f"{weapontype}: {heros[1].items[weapontype].itemtype}" for weapontype in ["close", "range", "magical", "defence"]), font="Imagine.ttf", font_size=60, secondary_size=40, activated_func=heroPicked)
barbarianBtn = Button(*scale_rect((965, 10, 467.5, 1060)), win, (179, 213, 224), (" "*6)+f"barbarian\n\n\n\n\nStrength: {heros[2].stats.strength}\nAgility: {heros[2].stats.agility}\nMana: {heros[2].stats.mana}\n"+"\n".join(f"{weapontype}: {heros[2].items[weapontype].itemtype}" for weapontype in ["close", "range", "magical", "defence"]), font="Imagine.ttf", font_size=60, secondary_size=40, activated_func=heroPicked)
rogueBtn = Button(*scale_rect((1442.5, 10, 467.5, 1060)), win, (179, 213, 224), (" "*10)+f"rogue\n\n\n\n\nStrength: {heros[3].stats.strength}\nAgility: {heros[3].stats.agility}\nMana: {heros[3].stats.mana}\n"+"\n".join(f"{weapontype}: {heros[3].items[weapontype].itemtype}" for weapontype in ["close", "range", "magical", "defence"]), font="Imagine.ttf", font_size=60, secondary_size=40, activated_func=heroPicked)

# Village Screen
dungeonBtn = Button(*scale_rect((800, 150, 300, 300)), win, (255, 255, 0), "dungeon", font="Imagine.ttf", font_size=50, activated_func=dungeonEntrance)
wizardBtn = Button(*scale_rect((1300, 150, 300, 300)), win, (255, 255, 0), "wizards", font="Imagine.ttf", font_size=50, activated_func=wizardsShop)
blacksmithBtn = Button(*scale_rect((800, 630, 300, 300)), win, (255, 255, 0), "black\nsmiths", font="Imagine.ttf", font_size=50, secondary_size=50, activated_func=blacksmithsShop)
quitBtn = Button(*scale_rect((1300, 630, 300, 300)), win, (255, 255, 0), "Sleep", font="Imagine.ttf", font_size=50, activated_func=quitGame)

# Shops
shortswordBtn = Button(*scale_rect((775, 150, 250, 250)), win, (255, 255, 0), f"short sword\ncost: {(items['shortsword'].level**2)*5}", font="Imagine.ttf", font_size=34, secondary_size=24, activated_func=purchase)
swordBtn = Button(*scale_rect((1075, 150, 250, 250)), win, (255, 255, 0), f"sword\ncost: {(items['sword'].level**2)*5}", font="Imagine.ttf", font_size=34, secondary_size=24, activated_func=purchase)
broadswordBtn = Button(*scale_rect((1375, 150, 250, 250)), win, (255, 255, 0), f"broad sword\ncost: {(items['broadsword'].level**2)*5}", font="Imagine.ttf", font_size=34, secondary_size=24, activated_func=purchase)
bowBtn = Button(*scale_rect((775, 450, 250, 250)), win, (255, 255, 0), f"bow\ncost: {(items['bow'].level**2)*5}", font="Imagine.ttf", font_size=34, secondary_size=24, activated_func=purchase)
crossbowBtn = Button(*scale_rect((1075, 450, 250, 250)), win, (255, 255, 0), f"cross bow\ncost: {(items['crossbow'].level**2)*5}", font="Imagine.ttf", font_size=34, secondary_size=24, activated_func=purchase)
longbowBtn = Button(*scale_rect((1375, 450, 250, 250)), win, (255, 255, 0), f"long bow\ncost: {(items['longbow'].level**2)*5}", font="Imagine.ttf", font_size=34, secondary_size=24, activated_func=purchase)
leatherBtn = Button(*scale_rect((775, 750, 250, 250)), win, (255, 255, 0), f"leather\ncost: {(items['leather'].level**2)*5}", font="Imagine.ttf", font_size=34, secondary_size=24, activated_func=purchase)
chainmailBtn = Button(*scale_rect((1075, 750, 250, 250)), win, (255, 255, 0), f"chain mail\ncost: {(items['chainmail'].level**2)*5}", font="Imagine.ttf", font_size=34, secondary_size=24, activated_func=purchase)
plateBtn = Button(*scale_rect((1375, 750, 250, 250)), win, (255, 255, 0), f"plate\ncost: {(items['plate'].level**2)*5}", font="Imagine.ttf", font_size=34, secondary_size=24, activated_func=purchase)
amuletBtn = Button(*scale_rect((775, 450, 250, 250)), win, (255, 255, 0), f"amulet\ncost: {(items['amulet'].level**2)*5}", font="Imagine.ttf", font_size=34, secondary_size=24, activated_func=purchase)
wandBtn = Button(*scale_rect((1075, 450, 250, 250)), win, (255, 255, 0), f"wand\ncost: {(items['wand'].level**2)*5}", font="Imagine.ttf", font_size=34, secondary_size=24, activated_func=purchase)
staffBtn = Button(*scale_rect((1375, 450, 250, 250)), win, (255, 255, 0), f"staff\ncost: {(items['staff'].level**2)*5}", font="Imagine.ttf", font_size=34, secondary_size=24, activated_func=purchase)
backBtn = Button(*scale_rect((1857.5, 7.5, 50, 50)), win, activated_func=toVillage)

# Dungeon
closeBtn = Button(*scale_rect((20, 705, 350, 50)), win, (255, 255, 0), font="Imagine.ttf", text="close", font_colour=(255, 255, 0), activated_func=doAttack)
rangeBtn = Button(*scale_rect((20, 780, 350, 50)), win, (255, 255, 0), font="Imagine.ttf", text="range", font_colour=(255, 255, 0), activated_func=doAttack)
magicBtn = Button(*scale_rect((20, 855, 350, 50)), win, (255, 255, 0), font="Imagine.ttf", text="magical", font_colour=(255, 255, 0), activated_func=doAttack)
fleeBtn  = Button(*scale_rect((20, 930, 350, 50)), win, (255, 255, 0), font="Imagine.ttf", activated_func=fleeFight)

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