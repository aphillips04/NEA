from dataclasses import dataclass
import json
from typing import Annotated

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
    def __init__(self, name: str, herotype: str, stats: Stats, items: Annotated[dict[str, Item], 4]) -> None:
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
    def __init__(self, monstertype: str, levels: Annotated[list[Stats], 3]) -> None:
        self.monstertype = monstertype
        self.levels = levels
