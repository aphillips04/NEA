from dataclasses import dataclass
import json

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
    def __init__(self, name, herotype, stats, items):
        self.name = name
        self.herotype = herotype
        self.stats = stats
        self.xp = 0
        self.items = items
        self.gold = 0

    def save_progress(self):
        with open("playerdata.json", "r") as f:
            data = json.load(f)
        data[self.name] = dict(
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
            items = dict(
                dict(
                    name = self.items[0].name,
                    type = self.items[0].itemtype,
                    icon = self.items[0].icon,
                    level = self.items[0].level,
                ),
                dict(
                    name = self.items[1].name,
                    type = self.items[1].itemtype,
                    icon = self.items[1].icon,
                    level = self.items[1].level,
                ),
                dict(
                    name = self.items[2].name,
                    type = self.items[2].itemtype,
                    icon = self.items[2].icon,
                    level = self.items[2].level,
                ),
                dict(
                    name = self.items[3].name,
                    type = self.items[3].itemtype,
                    icon = self.items[3].icon,
                    level = self.items[3].level,
                )
            ),
            gold = self.gold
        )
        json.dump(data, "data.json", indent=4)

class Monster:
    def __init__(self, monstertype, levels):
        self.monstertype = monstertype
        self.levels = levels
