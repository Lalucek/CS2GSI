from __future__ import annotations

from collections.abc import Callable, Mapping
from types import MappingProxyType
from typing import Any, TypeVar

from . import _coerce as c
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
from .exceptions import PayloadError
from .models import (
    BombInfo,
    GameState,
    MapInfo,
    MatchStats,
    PhaseCountdowns,
    Player,
    PlayerState,
    PlayerWeapons,
    ProviderInfo,
    RoundInfo,
    RoundWin,
    TeamStats,
    ThrownGrenade,
    Weapon,
)

__all__ = ["GameStateParser"]

Payload = Mapping[str, Any]
_T = TypeVar("_T")


class GameStateParser:
    def parse(self, payload: Payload) -> GameState:
        if not isinstance(payload, Mapping):
            raise PayloadError(
                f"GSI payload must be a JSON object, got {type(payload).__name__}"
            )

        all_players = c.as_mapping(payload.get("allplayers")) or {}

        return GameState(
            provider=self._section(payload, "provider", self._parse_provider),
            map=self._section(payload, "map", self._parse_map),
            round=self._section(payload, "round", self._parse_round),
            phase_countdowns=self._section(
                payload, "phase_countdowns", self._parse_phase_countdowns
            ),
            bomb=self._section(payload, "bomb", self._parse_bomb),
            player=self._section(payload, "player", self._parse_player),
            all_players=MappingProxyType(
                {
                    str(steam_id): self._parse_player(data, steam_id=str(steam_id))
                    for steam_id, data in all_players.items()
                    if isinstance(data, Mapping)
                }
            ),
            grenades=self._parse_grenades(c.as_mapping(payload.get("grenades")) or {}),
            raw=MappingProxyType(dict(payload)),
        )

    @staticmethod
    def _section(
        payload: Payload, key: str, parse: Callable[[Payload], _T]
    ) -> _T | None:
        data = c.as_mapping(payload.get(key))
        return None if data is None else parse(data)

    def _parse_provider(self, data: Payload) -> ProviderInfo:
        return ProviderInfo(
            name=c.to_str(data.get("name")),
            app_id=c.to_int(data.get("appid")),
            version=c.to_int(data.get("version")),
            steam_id=c.to_str(data.get("steamid")),
            timestamp=c.to_int(data.get("timestamp")),
        )

    def _parse_map(self, data: Payload) -> MapInfo:
        return MapInfo(
            mode=c.to_str(data.get("mode")),
            name=c.to_str(data.get("name")),
            phase=c.to_enum(MapPhase, data.get("phase")),
            round=c.to_int(data.get("round")),
            team_ct=self._parse_team(c.as_mapping(data.get("team_ct")) or {}),
            team_t=self._parse_team(c.as_mapping(data.get("team_t")) or {}),
            num_matches_to_win_series=c.to_int(data.get("num_matches_to_win_series")),
            round_wins=self._parse_round_wins(
                c.as_mapping(data.get("round_wins")) or {}
            ),
        )

    def _parse_team(self, data: Payload) -> TeamStats:
        return TeamStats(
            score=c.to_int(data.get("score")),
            name=c.to_str(data.get("name")),
            consecutive_round_losses=c.to_int(data.get("consecutive_round_losses")),
            timeouts_remaining=c.to_int(data.get("timeouts_remaining")),
            matches_won_this_series=c.to_int(data.get("matches_won_this_series")),
        )

    def _parse_round_wins(self, data: Payload) -> tuple[RoundWin, ...]:
        wins: list[RoundWin] = []
        for round_key, outcome in data.items():
            round_number = c.to_int(round_key)
            outcome_str = c.to_str(outcome)
            if round_number is None or outcome_str is None:
                continue
            wins.append(
                RoundWin(
                    round_number=round_number,
                    outcome=outcome_str,
                    winner=self._winner_from_outcome(outcome_str),
                )
            )
        return tuple(sorted(wins, key=lambda win: win.round_number))

    @staticmethod
    def _winner_from_outcome(outcome: str) -> Team | None:
        prefix = outcome.split("_", 1)[0].upper()
        return c.to_enum(Team, prefix)

    def _parse_round(self, data: Payload) -> RoundInfo:
        return RoundInfo(
            phase=c.to_enum(RoundPhase, data.get("phase")),
            bomb=c.to_enum(RoundBombState, data.get("bomb")),
            win_team=c.to_enum(Team, data.get("win_team")),
        )

    def _parse_phase_countdowns(self, data: Payload) -> PhaseCountdowns:
        return PhaseCountdowns(
            phase=c.to_enum(CountdownPhase, data.get("phase")),
            phase_ends_in=c.to_float(data.get("phase_ends_in")),
        )

    def _parse_bomb(self, data: Payload) -> BombInfo:
        return BombInfo(
            state=c.to_enum(BombState, data.get("state")),
            position=c.to_vector(data.get("position")),
            countdown=c.to_float(data.get("countdown")),
            player=c.to_str(data.get("player")),
        )

    # ------------------------------------------------------------------ players

    def _parse_player(self, data: Payload, steam_id: str | None = None) -> Player:
        state = c.as_mapping(data.get("state"))
        match_stats = c.as_mapping(data.get("match_stats"))
        return Player(
            steam_id=c.to_str(data.get("steamid")) or steam_id,
            name=c.to_str(data.get("name")),
            clan_tag=c.to_str(data.get("clantag")),
            observer_slot=c.to_int(data.get("observer_slot")),
            team=c.to_enum(Team, data.get("team")),
            activity=c.to_enum(PlayerActivity, data.get("activity")),
            state=None if state is None else self._parse_player_state(state),
            match_stats=None
            if match_stats is None
            else self._parse_match_stats(match_stats),
            weapons=self._parse_weapons(c.as_mapping(data.get("weapons")) or {}),
            position=c.to_vector(data.get("position")),
            forward=c.to_vector(data.get("forward")),
            spectator_target=c.to_str(data.get("spectarget")),
        )

    def _parse_player_state(self, data: Payload) -> PlayerState:
        return PlayerState(
            health=c.to_int(data.get("health")),
            armor=c.to_int(data.get("armor")),
            helmet=c.to_bool(data.get("helmet")),
            defuse_kit=c.to_bool(data.get("defusekit")),
            flashed=c.to_int(data.get("flashed")),
            smoked=c.to_int(data.get("smoked")),
            burning=c.to_int(data.get("burning")),
            money=c.to_int(data.get("money")),
            round_kills=c.to_int(data.get("round_kills")),
            round_kill_hs=c.to_int(data.get("round_killhs")),
            round_total_damage=c.to_int(data.get("round_totaldmg")),
            equip_value=c.to_int(data.get("equip_value")),
        )

    def _parse_match_stats(self, data: Payload) -> MatchStats:
        return MatchStats(
            kills=c.to_int(data.get("kills")),
            assists=c.to_int(data.get("assists")),
            deaths=c.to_int(data.get("deaths")),
            mvps=c.to_int(data.get("mvps")),
            score=c.to_int(data.get("score")),
        )

    def _parse_weapons(self, data: Payload) -> PlayerWeapons:
        return PlayerWeapons(
            tuple(
                self._parse_weapon(str(slot), weapon)
                for slot, weapon in data.items()
                if isinstance(weapon, Mapping)
            )
        )

    def _parse_weapon(self, slot: str, data: Payload) -> Weapon:
        return Weapon(
            slot=slot,
            name=c.to_str(data.get("name")),
            paintkit=c.to_str(data.get("paintkit")),
            type=c.to_enum(WeaponType, data.get("type")),
            state=c.to_enum(WeaponState, data.get("state")),
            ammo_clip=c.to_int(data.get("ammo_clip")),
            ammo_clip_max=c.to_int(data.get("ammo_clip_max")),
            ammo_reserve=c.to_int(data.get("ammo_reserve")),
        )

    def _parse_grenades(self, data: Payload) -> tuple[ThrownGrenade, ...]:
        return tuple(
            self._parse_grenade(str(grenade_id), grenade)
            for grenade_id, grenade in data.items()
            if isinstance(grenade, Mapping)
        )

    def _parse_grenade(self, grenade_id: str, data: Payload) -> ThrownGrenade:
        flames = c.as_mapping(data.get("flames")) or {}
        return ThrownGrenade(
            id=grenade_id,
            type=c.to_str(data.get("type")),
            owner=c.to_str(data.get("owner")),
            position=c.to_vector(data.get("position")),
            velocity=c.to_vector(data.get("velocity")),
            lifetime=c.to_float(data.get("lifetime")),
            effect_time=c.to_float(data.get("effecttime")),
            flames=tuple(
                vector
                for vector in map(c.to_vector, flames.values())
                if vector is not None
            ),
        )
