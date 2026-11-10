"""Enumerations for the well-known string values sent by CS2 Game State Integration."""

from __future__ import annotations

from enum import Enum

__all__ = [
    "BombState",
    "CountdownPhase",
    "MapPhase",
    "PlayerActivity",
    "RoundBombState",
    "RoundPhase",
    "Team",
    "WeaponState",
    "WeaponType",
]


class Team(str, Enum):
    """Side a player or team is playing on."""

    T = "T"
    CT = "CT"


class PlayerActivity(str, Enum):
    """What the player is currently doing in the client."""

    PLAYING = "playing"
    MENU = "menu"
    TEXT_INPUT = "textinput"


class MapPhase(str, Enum):
    """Phase of the whole map (``map.phase``)."""

    WARMUP = "warmup"
    LIVE = "live"
    INTERMISSION = "intermission"
    GAME_OVER = "gameover"


class RoundPhase(str, Enum):
    """Phase of the current round (``round.phase``)."""

    FREEZETIME = "freezetime"
    LIVE = "live"
    OVER = "over"


class RoundBombState(str, Enum):
    """Bomb state as reported in the ``round`` section."""

    PLANTED = "planted"
    EXPLODED = "exploded"
    DEFUSED = "defused"


class CountdownPhase(str, Enum):
    """Phase reported in the ``phase_countdowns`` section."""

    WARMUP = "warmup"
    FREEZETIME = "freezetime"
    LIVE = "live"
    BOMB = "bomb"
    DEFUSE = "defuse"
    OVER = "over"
    PAUSED = "paused"
    TIMEOUT_T = "timeout_t"
    TIMEOUT_CT = "timeout_ct"


class BombState(str, Enum):
    """Detailed bomb state from the ``bomb`` section."""

    CARRIED = "carried"
    DROPPED = "dropped"
    PLANTING = "planting"
    PLANTED = "planted"
    DEFUSING = "defusing"
    DEFUSED = "defused"
    EXPLODED = "exploded"


class WeaponState(str, Enum):
    """Whether a weapon is currently in hand."""

    ACTIVE = "active"
    HOLSTERED = "holstered"
    RELOADING = "reloading"


class WeaponType(str, Enum):
    """Weapon category as reported by the game."""

    KNIFE = "Knife"
    PISTOL = "Pistol"
    RIFLE = "Rifle"
    SNIPER_RIFLE = "SniperRifle"
    SUBMACHINE_GUN = "Submachine Gun"
    SHOTGUN = "Shotgun"
    MACHINE_GUN = "Machine Gun"
    GRENADE = "Grenade"
    C4 = "C4"
    STACKABLE_ITEM = "StackableItem"

    @property
    def is_primary(self) -> bool:
        """``True`` for weapons occupying the primary slot."""
        return self in _PRIMARY_TYPES


_PRIMARY_TYPES = frozenset(
    {
        WeaponType.RIFLE,
        WeaponType.SNIPER_RIFLE,
        WeaponType.SUBMACHINE_GUN,
        WeaponType.SHOTGUN,
        WeaponType.MACHINE_GUN,
    }
)
