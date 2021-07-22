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

"""
heros = [
    Hero(None, "Mage", Stats("imgs/mage.", 1, ), dict(
        close = Item("", "imgs/", 1),
        range = Item("", "imgs/", 1),
        mana = Item("", "imgs/", 1),
        defence = Item("", "imgs/", 1)
    )),
    Hero(None, "Warrior", Stats("imgs/warrior.", 1, ), dict(
        close = Item("", "imgs/", 1),
        range = Item("", "imgs/", 1),
        mana = Item("", "imgs/", 1),
        defence = Item("", "imgs/", 1)
    )),
    Hero(None, "", Stats("imgs/", 1, ), dict(
        close = Item("", "imgs/", 1),
        range = Item("", "imgs/", 1),
        mana = Item("", "imgs/", 1),
        defence = Item("", "imgs/", 1)
    )),
    Hero(None, "", Stats("imgs/", 1, ), dict(
        close = Item("", "imgs/", 1),
        range = Item("", "imgs/", 1),
        mana = Item("", "imgs/", 1),
        defence = Item("", "imgs/", 1)
    ))
]

monsters = [
    Monster("Skeleton", [Stats(1, "imgs/skeleton."), Stats(2, "imgs/skeleton."), Stats(3, "imgs/skeleton.")]),
    Monster("Orc", [Stats(1, "imgs/orc."), Stats(2, "imgs/orc."), Stats(3, "imgs/orc.")]),
    Monster("Ogre", [Stats(1, "imgs/ogre."), Stats(2, "imgs/ogre."), Stats(3, "imgs/ogre.")]),
    Monster("Troll", [Stats(1, "imgs/troll."), Stats(2, "imgs/troll."), Stats(3, "imgs/troll.")]),
    Monster("Wolf", [Stats(1, "imgs/wolf."), Stats(2, "imgs/wolf."), Stats(3, "imgs/wolf.")])
]

bosses = [
    Monster("Dragon", [Stats(1, "imgs/dragon."), Stats(2, "imgs/dragon."), Stats(3, "imgs/dragon.")]),
    Monster("Demon", [Stats(1, "imgs/demon."), Stats(2, "imgs/demon."), Stats(3, "imgs/demon.")]),
    Monster("Basalisk", [Stats(1, "imgs/basalisk."), Stats(2, "imgs/basalisk."), Stats(3, "imgs/basalisk.")])
]"""