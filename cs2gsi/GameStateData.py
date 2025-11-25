class GameState:
    def __init__(self):
        self.player = Player()
        self.allplayers = {}
        self.match_info = MatchInfo()
        self.team_info = TeamInfo()
        self.phase_info = PhaseInfo()
        self.bomb_info = BombInfo()
        self.round_info = RoundInfo()
        self.provider_info = ProviderInfo()

class Player:
    def __init__(self):
        self.steamid = None
        self.clantag = None
        self.name = None
        self.observer_slot = None
        self.team = None
        self.activity = None
        self.playerData = PlayerData()
        self.playerWeapons = PlayerWeapons()
        self.playerStats = PlayerStats()
class PlayerData:
    def __init__(self):
        self.health = None
        self.money = None
        self.armor = None
        self.helmet = None
        self.flashed = None
        self.smoked = None
        self.burning = None
        self.round_kills = None
        self.round_killhs = None
        self.equip_value = None
class PlayerStats:
    def __init__(self):
        self.kills = None
        self.deaths = None
        self.assists = None
        self.mvps = None
        self.score = None
class PlayerWeapons:
    def __init__(self):
        self.weapon_knife = {
            "name": None,
            "paintkit": None,
            "type": None,
            "state": None
        }
        self.weapon_secondary = {
            "name": None,
            "paintkit": None,
            "type": None,
            "state": None,
            "ammo_clip": None,
            "ammo_reserve": None,
            "ammo_clip_max": None
        }
        self.weapon_primary = {
            "name": None,
            "paintkit": None,
            "type": None,
            "state": None,
            "ammo_clip": None,
            "ammo_reserve": None,
            "ammo_clip_max": None
        }
        self.grenade_1 = {
            "name": None,
            "paintkit": None,
            "type": None,
            "state": None,
            "ammo_reserve": None
        }
        self.grenade_2 = {
            "name": None,
            "paintkit": None,
            "type": None,
            "state": None,
            "ammo_reserve": None
        }
        self.grenade_3 = {
            "name": None,
            "paintkit": None,
            "type": None,
            "state": None,
            "ammo_reserve": None
        }
        self.grenade_4 = {
            "name": None,
            "paintkit": None,
            "type": None,
            "state": None,
            "ammo_reserve": None
        }
class MatchInfo:
    def __init__(self):
        self.mode = None
        self.map_name = None
        self.phase = None
        self.round = None
        self.num_matches_to_win_series = None
class TeamInfo:
    def __init__(self):
        self.team_t = {
            "score": None,
            "consecutive_round_losses": None,
            "timeouts_remaining": None,
            "matches_won_this_series": None
        }
        self.team_ct = {
            "score": None,
            "consecutive_round_losses": None,
            "timeouts_remaining": None,
            "matches_won_this_series": None
        }

class PhaseInfo:
    def __init__(self):
        self.phase = None
        self.phase_ends_in = None
        self.previous_ends_in = None

class BombInfo:
    def __init__(self):
        self.state = None
        self.countdown = None
        self.position = None
        self.player = None
    def getStateAndPlayer(self):
        return self.state, self.player
class RoundInfo:
    def __init__(self):
        self.phase = None
        self.win_team = None
        self.bomb = None
        self.roundHistory = {}

class ProviderInfo:
    def __init__(self):
        self.name = None
        self.appid = None
        self.version = None
        self.steamid = None
        self.timestamp = None