import json
from classes import *

# TEST = Hero("Dev", "God", Stats("imgs/god.png", 1000, 100, 100, 100, 1000), {"close": Item("God Sword", "imgs/godsword.png", 1000),
#     "range": Item("God Bow", "imgs/godbow.png", 1000), "mana": Item("God Staff", "imgs/godstaff.png", 1000), "defence": Item("God Armour", "imgs/godarmour.png", 1000)});TEST.xp = 1000;TEST.gold = 1000
# TEST.save_progress()

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

with open("playerdata.json", "r+") as f:
    if not f.read():
        json.dump({}, f, indent=4)

heros = [
    Hero(None, "Mage", Stats("img/mage.", 1, 2, 3, 5), dict(
        close = None,
        range = Item("Bow", "img/bow.", 1),
        mana = Item("Wand", "img/wand.", 1),
        defence = Item("Leather", "img/leather.", 1)
    )),
    Hero(None, "Paladin", Stats("img/paladin.", 1, 4, 4, 2), dict(
        close = Item("Short Sword", "img/short_sword.", 1),
        range = None,
        mana = Item("Amulet", "img/amulet.", 1),
        defence = Item("Shield", "img/shield.", 1)
    )),
    Hero(None, "Barbarian", Stats("img/barbarian.", 1, 5, 4, 1), dict(
        close = Item("Sword", "img/sword.", 1),
        range = None,
        mana = Item("Amulet", "img/amulet.", 1),
        defence = Item("Leather", "img/leather.", 1)
    )),
    Hero(None, "Rogue", Stats("img/rogue.", 1, 2, 5, 3), dict(
        close = None,
        range = Item("Crossbow", "img/crossbow.", 1),
        mana = Item("Amulet", "img/amulet.", 1),
        defence = Item("Leather", "img/leather.", 1)
    ))
]

monsters = [
    Monster("Skeleton", [Stats("imgs/skeleton.", 1, ), Stats("imgs/skeleton.", 2, ), Stats("imgs/skeleton.", 3, )]),
    Monster("Orc", [Stats("imgs/orc.", 1, ), Stats("imgs/orc.", 2, ), Stats("imgs/orc.", 3, )]),
    Monster("Ogre", [Stats("imgs/ogre.", 1, ), Stats("imgs/ogre.", 2, ), Stats("imgs/ogre.", 3, )]),
    Monster("Troll", [Stats("imgs/troll.", 1, ), Stats("imgs/troll.", 2, ), Stats("imgs/troll.", 3, )]),
    Monster("Wolf", [Stats("imgs/wolf.", 1, ), Stats("imgs/wolf.", 2, ), Stats("imgs/wolf.", 3, )])
]

bosses = [
    Monster("Dragon", [Stats("imgs/dragon.", 1, ), Stats("imgs/dragon.", 2, ), Stats("imgs/dragon.", 3, )]),
    Monster("Demon", [Stats("imgs/demon.", 1, ), Stats("imgs/demon.", 2, ), Stats("imgs/demon.", 3, )]),
    Monster("Basalisk", [Stats("imgs/basalisk.", 1, ), Stats("imgs/basalisk.", 2, ), Stats("imgs/basalisk.", 3, )])
]