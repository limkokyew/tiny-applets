import random
from math import floor
from enum import Enum

class WeaponType(Enum):
    """
    Represents the weapon type a weapon belongs to - for instance,
    Areadbhar is classified as a lance.
    """
    SWORD = 0
    AXE = 1
    LANCE = 2

WEAPON_TRIANGLE = {
    WeaponType.SWORD: WeaponType.AXE,
    WeaponType.AXE: WeaponType.LANCE,
    WeaponType.LANCE: WeaponType.SWORD
}

class Attribute(Enum):
    """
    Contains all attributes a character may possess.
    """
    HP = "HP"
    STRENGTH = "Strength"
    MAGIC = "Magic"
    SKILL = "Skill"
    SPEED = "Speed"
    LUCK = "Luck"
    DEFENSE = "Defense"
    RESISTANCE = "Resistance"
    CHARM = "Charm"
    
    # Anything from here on out is not a character stat, but an attribute
    # resulting from above stats - for example, crit is calculated from luck and
    # other factors
    A_MOVEMENT = "Movement"
    A_HIT = "Hit"
    A_CRIT = "Crit"
    A_AVOID = "Avoid"
    A_CRIT_AVOID = "Crit Avoid"
    A_MT = "Might"

class Class():
    def __init__(
        self,
        name,
        attribute_modifiers,
    ):
        self.attribute_modifiers = attribute_modifiers

class Classes(Enum):
    """
    Contains different classes found in the Fire Emblem games.
    """
    SWORDMASTER = Class(name="Swordmaster", attribute_modifiers={Attribute.A_CRIT: 10})
    SNIPER = Class(name="Sniper", attribute_modifiers={Attribute.A_CRIT: 50})

class Weapon():
    def __init__(
        self,
        mt,
        hit,
        crit,
        w_range,
        weight,
        w_type,
        magic=False,
        brave=False
    ):
        self.mt = mt
        self.hit = hit
        self.crit = crit
        self.w_range = w_range
        self.weight = weight
        self.w_type = w_type
        self.magic = magic
        self.brave = brave

class Unit():
    def __init__(
        self,
        name,
        lvl,
        stats,
        growths,
        weapon=None,
        accessory=None,
        cclass=None,
        crit_quotes=None
    ):
        self.name = name
        self.maxHP = stats[Attribute.HP]
        self.stats = stats
        self.growths = growths
        self.weapon = weapon
        self.accessory = accessory
        self.skills = []
        self.cclass = cclass
        self.crit_quotes = crit_quotes
    
    def create_stats_dict(hp, stre, mag, skl, spd, lck, defe, res, cha):
        return {
            Attribute.HP: hp,
            Attribute.STRENGTH: stre,
            Attribute.MAGIC: mag,
            Attribute.SKILL: skl,
            Attribute.SPEED: spd,
            Attribute.LUCK: lck,
            Attribute.DEFENSE: defe,
            Attribute.RESISTANCE: res,
            Attribute.CHARM: cha,
        }
    
    def _get_skill_bonuses(self, attribute, initiate_only=False, counter_only=False):
        """
        Retrieves all skill bonuses concerning the given attribute.
        
        Args:
            attribute: Attribute
            initiate_only: bool, only consider skills that activate on
                           initiation
            counter_only: bool, only consider skills that activate on
                           counterattacks
        
        Returns:
            int, the
        """
        bonus_total = 0
        for skill in self.skills:
            if skill.attribute == attribute \
                and skill.initiate_only == initiate_only \
                and skill.counter_only == counter_only:
                bonus_total += skill.value
        return bonus_total
    
    def _get_class_bonuses(self, attribute):
        if self.cclass is not None:
            return self.cclass.attribute_modifiers.get(attribute, 0)
        return 0
    
    def damage(self, dmg):
        self.stats[Attribute.HP] -= dmg
    
    def get_stat(self, attribute, initiate_only=False, counter_only=False):
        # In case a secondary attribute is desired, set the initial value to 0
        attribute_val = self.stats.get(attribute, 0)
        attribute_val += self._get_skill_bonuses(attribute, initiate_only, counter_only)
        attribute_val += self._get_class_bonuses(attribute)
        return attribute_val
    
    def get_hit(self, magic=False, initiate_only=False, counter_only=False):
        hit = 0
        if self.weapon is not None:
            if magic:
                hit = (self.get_stat(Attribute.SKILL) + self.get_stat(Attribute.LUCK)) / 2 + self.weapon.hit
            else:
                hit = self.get_stat(Attribute.SKILL) + self.weapon.hit
            hit += self._get_skill_bonuses(Attribute.A_HIT, initiate_only, counter_only)
            return hit
        else:
            return 0
    
    def get_crit(self, initiate_only=False, counter_only=False):
        base_crit = floor((self.get_stat(Attribute.SKILL) + self.get_stat(Attribute.LUCK)) / 2)
        if self.weapon is not None:
            base_crit += self.weapon.crit
            base_crit += self._get_skill_bonuses(Attribute.A_CRIT, initiate_only, counter_only)
            base_crit += self._get_class_bonuses(Attribute.A_CRIT)
            return base_crit
        else:
            return 0
    
    def get_avoid(self, magic=False, initiate_only=False, counter_only=False):
        avoid = 0
        if magic:
            avoid = (self.get_stat(Attribute.SPEED) + self.get_stat(Attribute.LUCK)) / 2
        else:
            avoid = self.get_attack_speed()
        avoid += self._get_skill_bonuses(Attribute.A_AVOID, initiate_only, counter_only)
        return avoid
    
    def get_crit_avoid(self, initiate_only=False, counter_only=False):
        return self.get_stat(Attribute.LUCK) + self._get_skill_bonuses(Attribute.A_CRIT_AVOID, initiate_only, counter_only)
    
    def get_attack_speed(self):
        if self.weapon is not None:
            weight_penalty = max(self.weapon.weight - floor(0.2 * self.stats[Attribute.STRENGTH]), 0)
            return self.get_stat(Attribute.SPEED) - weight_penalty
        else:
            return self.get_stat(Attribute.SPEED)
            
    def get_mt(self, initiate=False, counter=False):
        if self.weapon is not None:
            mt_bonus = self.get_stat(Attribute.A_MT, initiate, counter)
            if self.weapon.magic:
                return self.get_stat(Attribute.MAGIC, initiate, counter) + mt_bonus + self.weapon.mt
            else:
                return self.get_stat(Attribute.STRENGTH, initiate, counter) + mt_bonus + self.weapon.mt
        else:
            return 0
    
    def get_prt(self):
        return self.get_stat(Attribute.DEFENSE)
    
    def get_res(self):
        return self.get_stat(Attribute.RESISTANCE)

    def get_crit_quote(self):
        if self.crit_quotes:
            return random.choice(self.crit_quotes)
        else:
            return None
    
    def equip(self, item):
        if isinstance(item, Weapon):
            self.weapon = item
        # todo: accessory

    def add_skill(self, skill):
        self.skills.append(skill)

    def has_skill(self, skill_name):
        for skill in self.skills:
            if skill.name == skill_name:
                return True
        
        return False

    def reclass(self, cclass):
        self.cclass = cclass

    def __repr__(self):
        return self.name
