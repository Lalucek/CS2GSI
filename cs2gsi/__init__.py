"""
CS:GO Game State Integration (GSI) Parser Library

Tato knihovna poskytuje parser pro CS:GO GSI JSON data a strukturované datové třídy.
"""

from .GameStateData import (
    GameState,
    Player,
    PlayerData,
    PlayerStats,
    PlayerWeapons,
    MatchInfo,
    TeamInfo,
    PhaseInfo,
    BombInfo,
    RoundInfo,
    ProviderInfo
)

from .JSONparser import PayloadParser
from .GSIReader import GSIListener

__all__ = [
    'GameState',
    'Player',
    'PlayerData',
    'PlayerStats',
    'PlayerWeapons',
    'MatchInfo',
    'TeamInfo',
    'PhaseInfo',
    'BombInfo',
    'RoundInfo',
    'ProviderInfo',
    'PayloadParser',
    'GSIListener'
]

__version__ = '1.0.1'

