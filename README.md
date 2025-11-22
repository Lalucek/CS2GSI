# CS:GO Game State Integration (GSI) Parser

Knihovna pro parsování CS:GO Game State Integration JSON dat do strukturovaných Python objektů.

## Instalace

```bash
pip install -r requirements.txt
```

## Závislosti

- `aiohttp >= 3.8.0` - pro HTTP server přijímající GSI data

## Použití

### Základní použití parseru

```python
import JSONparser as jp
import json

# Načtení JSON dat
with open('gsi_data.json', 'r') as f:
    json_data = json.load(f)

# Parsování dat
parser = jp.PayloadParser()
game_state = parser.parseData(json_data)

# Přístup k datům
print(f"Hráč: {game_state.player.name}")
print(f"Health: {game_state.player.playerData.health}")
print(f"Money: {game_state.player.playerData.money}")
print(f"Mapa: {game_state.match_info.map_name}")
print(f"Skóre T: {game_state.team_info.team_t['score']}")
print(f"Skóre CT: {game_state.team_info.team_ct['score']}")
```

### Použití GSI Listeneru

```python
from GSIReader import GSIListener

# Vytvoření listeneru na portu 3000
listener = GSIListener("127.0.0.1", 3000)

# Spuštění serveru (blokující)
listener.start()

# Přístup k parsovaným datům
game_state = listener.gs_object
if game_state:
    print(f"Health: {game_state.player.playerData.health}")
```

### Import jako modul

```python
# Pokud je knihovna v Python path
from GameStateData import GameState, Player
from JSONparser import PayloadParser
from GSIReader import GSIListener
```

## Struktura dat

### GameState
Hlavní třída obsahující všechny informace o herním stavu:
- `player` - informace o hráči
- `match_info` - informace o zápase
- `team_info` - informace o týmech
- `phase_info` - informace o fázi hry
- `bomb_info` - informace o bombě
- `round_info` - informace o kole
- `provider_info` - informace o provideru

### Player
- `steamid`, `name`, `team`, `activity`
- `playerData` - health, money, armor, helmet, flashed, smoked, burning, round_kills, round_killhs, equip_value
- `playerStats` - kills, deaths, assists, mvps, score
- `playerWeapons` - weapon_knife, weapon_primary, weapon_secondary, grenade_1-4

### MatchInfo
- `mode`, `map_name`, `phase`, `round`, `num_matches_to_win_series`

### TeamInfo
- `team_t` - skóre a statistiky teroristů
- `team_ct` - skóre a statistiky CT

### BombInfo
- `state`, `countdown`, `position`, `player`

## Konfigurace CS:GO GSI

Pro použití této knihovny musíte nakonfigurovat CS:GO Game State Integration:

1. Vytvořte soubor `gamestate_integration_*.cfg` v adresáři CS:GO:
   ```
   Steam\steamapps\common\Counter-Strike Global Offensive\csgo\cfg\
   ```

2. Obsah souboru:
   ```
   "Game State Integration"
   {
       "uri" "http://127.0.0.1:3000"
       "timeout" "5.0"
       "buffer"  "0.1"
       "throttle" "0.1"
       "heartbeat" "30.0"
       "data"
       {
           "provider"      "1"
           "map"           "1"
           "round"         "1"
           "player_id"     "1"
           "player_state"  "1"
           "player_weapons" "1"
           "player_match_stats" "1"
           "phase_countdowns" "1"
           "bomb"          "1"
           "team"          "1"
       }
   }
   ```

3. Spusťte GSI listener v Pythonu a spusťte CS:GO.

## Licence

Tento projekt je poskytován bez licence nebo jako open source.

