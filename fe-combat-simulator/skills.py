from enum import Enum
from objects import Attribute

class Skill():
    def __init__(
        self,
        name,
        attribute=None,
        value=0,
        initiate_only=False,
        counter_only=False,
        hp_threshold=None,
        hp_threshold_leq=False
    ):
        self.name = name
        self.attribute = attribute
        self.value = value
        self.initiate_only = initiate_only
        self.counter_only = counter_only
        self.hp_threshold = hp_threshold
        self.hp_threshold_leq = hp_threshold_leq

class Skills(Enum):
    VANTAGE = Skill(name="Vantage")
    DESPERATION = Skill(name="Desperation")
    STR2 = Skill(name="Strength +2", attribute=Attribute.STRENGTH, value=2)
    MAG2 = Skill(name="Magic +2", attribute=Attribute.MAGIC, value=2)
    SKL4 = Skill(name="Skill +4", attribute=Attribute.SKILL, value=4)
    SPD2 = Skill(name="Speed +2", attribute=Attribute.SPEED, value=2)
    LCK4 = Skill(name="Luck +4", attribute=Attribute.LUCK, value=4)
    DEF2 = Skill(name="Defense +2", attribute=Attribute.DEFENSE, value=2)
    RES2 = Skill(name="Resistance +2", attribute=Attribute.RESISTANCE, value=2)
    MOV1 = Skill(name="Movement +1", attribute=Attribute.A_MOVEMENT, value=1)
    CRIT20 = Skill(name="Crit +20", attribute=Attribute.A_CRIT, value=20)
    DEATH_BLOW = Skill(name="Death Blow", attribute=Attribute.STRENGTH, value=6, initiate_only=True)
    FIENDISH_BLOW = Skill(name="Fiendish Blow", attribute=Attribute.MAGIC, value=6, initiate_only=True)
    ARMORED_BLOW = Skill(name="Armored Blow", attribute=Attribute.DEFENSE, value=6, initiate_only=True)
    WARDING_BLOW = Skill(name="Warding Blow", attribute=Attribute.RESISTANCE, value=6, initiate_only=True)
    DARTING_BLOW = Skill(name="Darting Blow", attribute=Attribute.SPEED, value=6, initiate_only=True)
    UNCANNY_BLOW = Skill(name="Uncanny Blow", attribute=Attribute.A_HIT, value=30, initiate_only=True)
    STRONG_RIPOSTE = Skill(name="Strong Riposte", attribute=Attribute.A_MT, value=4, counter_only=True)
