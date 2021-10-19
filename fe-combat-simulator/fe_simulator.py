import random

from objects import Unit, Weapon, WeaponType, Classes, Attribute
from skills import Skills
from util import *


if __name__ == "__main__":
    unit_1 = Unit(
        "Corrin",
        39,
        Unit.create_stats_dict(45, 23, 46, 34, 52, 40, 21, 29, 30),
        Unit.create_stats_dict(40, 25, 60, 40, 50, 30, 45, 30, 35),
        crit_quotes=["I make my own fate!", "I won't surrender!", "You won't stop me!"]
    )
    unit_2 = Unit(
        "Ryoma",
        38,
        Unit.create_stats_dict(53, 40, 20, 31, 41, 29, 27, 21, 38),
        Unit.create_stats_dict(50, 60, 20, 30, 25, 25, 55, 25, 35),
        crit_quotes=["You have breathed your last!", "For the glory of Hoshido!",
            "You die - Now!", "You deserve worse!"],
        cclass=Classes.SWORDMASTER
    )
    unit_3 = Unit(
        "Xander",
        39,
        Unit.create_stats_dict(63, 47, 17, 29, 32, 34, 45, 22, 39),
        Unit.create_stats_dict(0, 0, 0, 0, 0, 0, 0, 0, 0),
        crit_quotes=["Begone, wretch!", "Prepare yourself!", "You're right where I want you!"]
    )
    unit_4 = Unit(
        "Edelgard",
        42,
        Unit.create_stats_dict(66, 50, 24, 24, 27, 30, 50, 24, 44),
        Unit.create_stats_dict(0, 0, 0, 0, 0, 0, 0, 0, 0),
        crit_quotes=["You can't stop me!", "No mercy!", "I will show no mercy!"]
    )
    unit_5 = Unit(
        "Ashe",
        40,
        Unit.create_stats_dict(42, 39, 20, 52, 36, 48, 23, 21, 24),
        Unit.create_stats_dict(0, 0, 0, 0, 0, 0, 0, 0, 0),
        crit_quotes=["I've got you!", "Let's finish this!"]
    )
   
    flame_shuriken = Weapon(10, 85, 0, (1, 2), 0, WeaponType.LANCE, magic=True)
    raijinto = Weapon(14, 90, 15, (1, 2), 0, WeaponType.SWORD)
    siegfried = Weapon(18, 80, 10, (1, 2), 0, WeaponType.SWORD)
    aymr = Weapon(25, 70, 10, (1, 1), 0, WeaponType.AXE)
    killer_bow = Weapon(12, 80, 35, (2, 3), 0, WeaponType.AXE)
    unit_1.equip(flame_shuriken)
    unit_2.equip(raijinto)
    unit_3.equip(siegfried)
    unit_4.equip(aymr)
    unit_5.equip(killer_bow)
    unit_5.add_skill(Skills.DEATH_BLOW)

    combat_range = 2
    while unit_5.get_stat(Attribute.HP) > 0 and unit_1.get_stat(Attribute.HP) > 0:
        print("\nStarting combat round!")
        print("-----------------------")
        combat(unit_5, unit_1, combat_range)


