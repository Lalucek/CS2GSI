from __future__ import annotations

from collections.abc import Iterator, Mapping
from dataclasses import dataclass, field
from datetime import datetime, timezone
from types import MappingProxyType
from typing import Any, NamedTuple

from .enums import (
    BombState,
    CountdownPhase,
    MapPhase,
    PlayerActivity,
    RoundBombState,
    RoundPhase,
    Team,
    WeaponState,
    WeaponType,
)

__all__ = [
    "BombInfo",
    "GameState",
    "MapInfo",
    "MatchStats",
    "PhaseCountdowns",
    "Player",
    "PlayerState",
    "PlayerWeapons",
    "ProviderInfo",
    "RoundInfo",
    "RoundWin",
    "TeamStats",
    "ThrownGrenade",
    "Vector3",
    "Weapon",
]


def _empty_mapping() -> Mapping[Any, Any]:
    return MappingProxyType({})


class Vector3(NamedTuple):
    """A point or direction in 3D world space."""

    x: float
    y: float
    z: float


@dataclass(frozen=True, slots=True, kw_only=True)
class ProviderInfo:
    """Information about the game client that sent the payload."""

    name: str | None = None
    app_id: int | None = None
    version: int | None = None
    steam_id: str | None = None
    timestamp: int | None = None

    @property
    def sent_at(self) -> datetime | None:
        """``timestamp`` converted to an aware UTC :class:`~datetime.datetime`."""
        if self.timestamp is None:
            return None
        return datetime.fromtimestamp(self.timestamp, tz=timezone.utc)


@dataclass(frozen=True, slots=True, kw_only=True)
class TeamStats:
    """Score and series information for one side."""

    score: int | None = None
    name: str | None = None
    consecutive_round_losses: int | None = None
    timeouts_remaining: int | None = None
    matches_won_this_series: int | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class RoundWin:
    """Outcome of a single finished round, e.g. ``ct_win_elimination``."""

    round_number: int
    outcome: str
    winner: Team | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class MapInfo:
    """State of the current map (the ``map`` section)."""

    mode: str | None = None
    name: str | None = None
    phase: MapPhase | None = None
    round: int | None = None
    team_ct: TeamStats = field(default_factory=TeamStats)
    team_t: TeamStats = field(default_factory=TeamStats)
    num_matches_to_win_series: int | None = None
    round_wins: tuple[RoundWin, ...] = ()

    def team(self, side: Team) -> TeamStats:
        """Return the stats of the given ``side``."""
        return self.team_ct if side is Team.CT else self.team_t


@dataclass(frozen=True, slots=True, kw_only=True)
class RoundInfo:
    """State of the current round (the ``round`` section)."""

    phase: RoundPhase | None = None
    bomb: RoundBombState | None = None
    win_team: Team | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class PhaseCountdowns:
    """Current phase and its remaining time (the ``phase_countdowns`` section)."""

    phase: CountdownPhase | None = None
    phase_ends_in: float | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class BombInfo:
    """Detailed bomb information (the ``bomb`` section, spectator only)."""

    state: BombState | None = None
    position: Vector3 | None = None
    countdown: float | None = None
    player: str | None = None
    """Steam ID of the player carrying, planting or defusing the bomb."""


@dataclass(frozen=True, slots=True, kw_only=True)
class PlayerState:
    """Volatile per-round player state (the ``player.state`` section)."""

    health: int | None = None
    armor: int | None = None
    helmet: bool | None = None
    defuse_kit: bool | None = None
    flashed: int | None = None
    smoked: int | None = None
    burning: int | None = None
    money: int | None = None
    round_kills: int | None = None
    round_kill_hs: int | None = None
    round_total_damage: int | None = None
    equip_value: int | None = None

    @property
    def is_alive(self) -> bool | None:
        """``True`` if health is above zero, ``None`` if health is unknown."""
        if self.health is None:
            return None
        return self.health > 0


@dataclass(frozen=True, slots=True, kw_only=True)
class MatchStats:
    """Cumulative player statistics for the match."""

    kills: int | None = None
    assists: int | None = None
    deaths: int | None = None
    mvps: int | None = None
    score: int | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class Weapon:
    """A single weapon or item in a player's inventory."""

    slot: str
    """Key of the weapon in the payload, e.g. ``weapon_0``."""
    name: str | None = None
    paintkit: str | None = None
    type: WeaponType | None = None
    state: WeaponState | None = None
    ammo_clip: int | None = None
    ammo_clip_max: int | None = None
    ammo_reserve: int | None = None

    @property
    def is_active(self) -> bool:
        """``True`` if the weapon is currently in hand."""
        return self.state in (WeaponState.ACTIVE, WeaponState.RELOADING)

    @property
    def is_knife(self) -> bool:
        """``True`` for knives (including ones with an unknown ``type``)."""
        return self.type is WeaponType.KNIFE or (
            self.name is not None and "knife" in self.name.lower()
        )


@dataclass(frozen=True, slots=True)
class PlayerWeapons:
    """Ordered collection of a player's weapons with convenient slot accessors."""

    items: tuple[Weapon, ...] = ()

    def __iter__(self) -> Iterator[Weapon]:
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)

    @property
    def active(self) -> Weapon | None:
        """The weapon currently in hand."""
        return next((w for w in self.items if w.is_active), None)

    @property
    def knife(self) -> Weapon | None:
        return next((w for w in self.items if w.is_knife), None)

    @property
    def primary(self) -> Weapon | None:
        return next(
            (w for w in self.items if w.type is not None and w.type.is_primary), None
        )

    @property
    def secondary(self) -> Weapon | None:
        return self._first_of(WeaponType.PISTOL)

    @property
    def grenades(self) -> tuple[Weapon, ...]:
        return tuple(w for w in self.items if w.type is WeaponType.GRENADE)

    @property
    def c4(self) -> Weapon | None:
        return self._first_of(WeaponType.C4)

    @property
    def has_c4(self) -> bool:
        return self.c4 is not None

    def _first_of(self, weapon_type: WeaponType) -> Weapon | None:
        return next((w for w in self.items if w.type is weapon_type), None)


@dataclass(frozen=True, slots=True, kw_only=True)
class Player:
    """A player, either the observed one (``player``) or one of ``allplayers``."""

    steam_id: str | None = None
    name: str | None = None
    clan_tag: str | None = None
    observer_slot: int | None = None
    team: Team | None = None
    activity: PlayerActivity | None = None
    state: PlayerState | None = None
    match_stats: MatchStats | None = None
    weapons: PlayerWeapons = field(default_factory=PlayerWeapons)
    position: Vector3 | None = None
    forward: Vector3 | None = None
    spectator_target: str | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class ThrownGrenade:
    """A grenade currently flying or active in the world (spectator only)."""

    id: str
    type: str | None = None
    owner: str | None = None
    """Steam ID of the player who threw the grenade."""
    position: Vector3 | None = None
    velocity: Vector3 | None = None
    lifetime: float | None = None
    effect_time: float | None = None
    flames: tuple[Vector3, ...] = ()


@dataclass(frozen=True, slots=True, kw_only=True)
class GameState:
    """A complete, immutable snapshot of one GSI payload.

    Sections that were not present in the payload are ``None``. The original
    payload is kept in :attr:`raw` for access to fields not modelled here.
    """

    provider: ProviderInfo | None = None
    map: MapInfo | None = None
    round: RoundInfo | None = None
    phase_countdowns: PhaseCountdowns | None = None
    bomb: BombInfo | None = None
    player: Player | None = None
    all_players: Mapping[str, Player] = field(default_factory=_empty_mapping)
    grenades: tuple[ThrownGrenade, ...] = ()
    raw: Mapping[str, Any] = field(
        default_factory=_empty_mapping, repr=False, compare=False
    )

    def players_on(self, side: Team) -> tuple[Player, ...]:
        """Return all players from :attr:`all_players` playing on ``side``."""
        return tuple(p for p in self.all_players.values() if p.team is side)
