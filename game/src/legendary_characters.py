"""
Legendary Star Wars Characters

Defines unique characteristics, abilities, and stats for iconic Star Wars characters.
"""

from config import *


class CharacterProfile:
    """Profile for a Star Wars character with unique abilities."""

    def __init__(
        self, name, character_type, health, force_energy, special_abilities, stats
    ):
        self.name = name
        self.character_type = character_type
        self.max_health = health
        self.max_force_energy = force_energy
        self.special_abilities = special_abilities
        self.stats = stats


# Legendary Character Profiles
LEGENDARY_CHARACTERS = {
    "luke_skywalker": CharacterProfile(
        name="Luke Skywalker",
        character_type="jedi",
        health=120,
        force_energy=100,
        special_abilities=[
            "force_push",
            "lightsaber_throw",
            "force_heal",
            "jedi_reflexes",
        ],
        stats={
            "speed": 6,
            "force_regen": 2,
            "lightsaber_damage": 25,
            "force_power_bonus": 1.2,
            "description": "The legendary Jedi Knight who brought balance to the Force",
        },
    ),
    "darth_vader": CharacterProfile(
        name="Darth Vader",
        character_type="sith",
        health=150,
        force_energy=120,
        special_abilities=[
            "force_push",
            "force_lightning",
            "lightsaber_throw",
            "dark_fury",
        ],
        stats={
            "speed": 5,
            "force_regen": 1.5,
            "lightsaber_damage": 30,
            "force_power_bonus": 1.3,
            "description": "The Dark Lord of the Sith, master of the dark side",
        },
    ),
    "yoda": CharacterProfile(
        name="Master Yoda",
        character_type="jedi",
        health=100,
        force_energy=150,
        special_abilities=[
            "force_push",
            "lightsaber_throw",
            "force_heal",
            "master_wisdom",
        ],
        stats={
            "speed": 8,
            "force_regen": 3,
            "lightsaber_damage": 20,
            "force_power_bonus": 1.5,
            "description": "Grand Master of the Jedi Order, wise and powerful",
        },
    ),
    "emperor_palpatine": CharacterProfile(
        name="Emperor Palpatine",
        character_type="sith",
        health=110,
        force_energy=180,
        special_abilities=["force_lightning", "dark_side_mastery", "force_storm"],
        stats={
            "speed": 4,
            "force_regen": 4,
            "lightsaber_damage": 15,
            "force_power_bonus": 2.0,
            "description": "Supreme ruler of the Empire, master of the dark side",
        },
    ),
    "obi_wan_kenobi": CharacterProfile(
        name="Obi-Wan Kenobi",
        character_type="jedi",
        health=110,
        force_energy=90,
        special_abilities=["force_push", "lightsaber_throw", "defensive_mastery"],
        stats={
            "speed": 5,
            "force_regen": 2,
            "lightsaber_damage": 22,
            "force_power_bonus": 1.1,
            "description": "Jedi Master and mentor, defensive combat specialist",
        },
    ),
    "darth_maul": CharacterProfile(
        name="Darth Maul",
        character_type="sith",
        health=130,
        force_energy=80,
        special_abilities=["force_push", "double_lightsaber", "berserker_rage"],
        stats={
            "speed": 7,
            "force_regen": 1,
            "lightsaber_damage": 28,
            "force_power_bonus": 0.9,
            "description": "Zabrak Sith Lord with deadly double-bladed lightsaber",
        },
    ),
    "mace_windu": CharacterProfile(
        name="Mace Windu",
        character_type="jedi",
        health=125,
        force_energy=95,
        special_abilities=["force_push", "lightsaber_throw", "vaapad_mastery"],
        stats={
            "speed": 6,
            "force_regen": 2,
            "lightsaber_damage": 27,
            "force_power_bonus": 1.2,
            "description": "Jedi Master with unique purple lightsaber and Vaapad style",
        },
    ),
    "count_dooku": CharacterProfile(
        name="Count Dooku",
        character_type="sith",
        health=115,
        force_energy=110,
        special_abilities=["force_lightning", "force_push", "elegant_dueling"],
        stats={
            "speed": 5,
            "force_regen": 2.5,
            "lightsaber_damage": 24,
            "force_power_bonus": 1.3,
            "description": "Former Jedi turned Sith Lord, elegant duelist",
        },
    ),
    "anakin_skywalker": CharacterProfile(
        name="Anakin Skywalker",
        character_type="jedi",
        health=135,
        force_energy=85,
        special_abilities=["force_push", "lightsaber_throw", "chosen_one_power"],
        stats={
            "speed": 7,
            "force_regen": 1.5,
            "lightsaber_damage": 26,
            "force_power_bonus": 1.4,
            "description": "The Chosen One, powerful but conflicted Jedi",
        },
    ),
    "kylo_ren": CharacterProfile(
        name="Kylo Ren",
        character_type="sith",
        health=125,
        force_energy=90,
        special_abilities=["force_push", "unstable_lightsaber", "rage_power"],
        stats={
            "speed": 6,
            "force_regen": 1.8,
            "lightsaber_damage": 25,
            "force_power_bonus": 1.1,
            "description": "Dark side warrior with unstable crossguard lightsaber",
        },
    ),
}


def get_character_profile(character_key):
    """Get character profile by key."""
    return LEGENDARY_CHARACTERS.get(character_key, None)


def get_all_jedi():
    """Get all Jedi characters."""
    return {
        key: char
        for key, char in LEGENDARY_CHARACTERS.items()
        if char.character_type == "jedi"
    }


def get_all_sith():
    """Get all Sith characters."""
    return {
        key: char
        for key, char in LEGENDARY_CHARACTERS.items()
        if char.character_type == "sith"
    }


def apply_character_profile(entity, character_key):
    """Apply character profile to an entity."""
    profile = get_character_profile(character_key)
    if profile:
        entity.character_name = profile.name
        entity.max_health = profile.max_health
        entity.health = profile.max_health
        entity.max_force_energy = profile.max_force_energy
        entity.force_energy = profile.max_force_energy
        entity.speed = profile.stats["speed"]
        entity.lightsaber_damage_bonus = profile.stats["lightsaber_damage"] - 20
        entity.force_power_bonus = profile.stats["force_power_bonus"]
        entity.force_regen_rate = profile.stats["force_regen"]
        entity.special_abilities = profile.special_abilities
        entity.character_description = profile.stats["description"]
        return True
    return False
