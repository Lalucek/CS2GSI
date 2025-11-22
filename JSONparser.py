import GameStateData as gsd

class PayloadParser:
    def parseData(self, data: dict):
        gameState = gsd.GameState()
        
        # Provider Info
        if 'provider' in data:
            provider = data['provider']
            gameState.provider_info.name = provider.get('name')
            gameState.provider_info.appid = provider.get('appid')
            gameState.provider_info.version = provider.get('version')
            gameState.provider_info.steamid = provider.get('steamid')
            gameState.provider_info.timestamp = provider.get('timestamp')
        
        # Match Info ('map' in GSI)
        if 'map' in data:
            map_data = data['map']
            gameState.match_info.mode = map_data.get('mode')
            gameState.match_info.map_name = map_data.get('name')
            gameState.match_info.phase = map_data.get('phase')
            gameState.match_info.round = map_data.get('round')
            gameState.match_info.num_matches_to_win_series = map_data.get('num_matches_to_win_series')
        
        # Team Info
        if 'team' in data:
            team_data = data['team']
            if 'T' in team_data:
                t_data = team_data['T']
                gameState.team_info.team_t['score'] = t_data.get('score')
                gameState.team_info.team_t['consecutive_round_losses'] = t_data.get('consecutive_round_losses')
                gameState.team_info.team_t['timeouts_remaining'] = t_data.get('timeouts_remaining')
                gameState.team_info.team_t['matches_won_this_series'] = t_data.get('matches_won_this_series')
            
            if 'CT' in team_data:
                ct_data = team_data['CT']
                gameState.team_info.team_ct['score'] = ct_data.get('score')
                gameState.team_info.team_ct['consecutive_round_losses'] = ct_data.get('consecutive_round_losses')
                gameState.team_info.team_ct['timeouts_remaining'] = ct_data.get('timeouts_remaining')
                gameState.team_info.team_ct['matches_won_this_series'] = ct_data.get('matches_won_this_series')
        
        # Phase Info
        if 'phase_countdowns' in data:
            phase_data = data['phase_countdowns']
            gameState.phase_info.phase = phase_data.get('phase')
            gameState.phase_info.phase_ends_in = phase_data.get('phase_ends_in')
            gameState.phase_info.previous_ends_in = phase_data.get('previous_ends_in')
        
        # Round Info
        if 'round' in data:
            round_data = data['round']
            gameState.round_info.phase = round_data.get('phase')
            gameState.round_info.win_team = round_data.get('win_team')
            gameState.round_info.bomb = round_data.get('bomb')
        
        # Bomb Info
        if 'bomb' in data:
            bomb_data = data['bomb']
            gameState.bomb_info.state = bomb_data.get('state')
            gameState.bomb_info.countdown = bomb_data.get('countdown')
            gameState.bomb_info.position = bomb_data.get('position')
            gameState.bomb_info.player = bomb_data.get('player')
        
        # Player Info
        if 'player' in data:
            player_data = data['player']
            
            # Basic player info
            gameState.player.steamid = player_data.get('steamid')
            gameState.player.name = player_data.get('name')
            gameState.player.observer_slot = player_data.get('observer_slot')
            gameState.player.team = player_data.get('team')
            gameState.player.activity = player_data.get('activity')
            
            # Player state (health, money, armor, etc.)
            if 'state' in player_data:
                state = player_data['state']
                gameState.player.playerData.health = state.get('health')
                gameState.player.playerData.money = state.get('money')
                gameState.player.playerData.armor = state.get('armor')
                gameState.player.playerData.helmet = state.get('helmet')
                gameState.player.playerData.flashed = state.get('flashed')
                gameState.player.playerData.smoked = state.get('smoked')
                gameState.player.playerData.burning = state.get('burning')
                gameState.player.playerData.round_kills = state.get('round_kills')
                gameState.player.playerData.round_killhs = state.get('round_killhs')
                gameState.player.playerData.equip_value = state.get('equip_value')
            
            # Player stats
            if 'match_stats' in player_data:
                stats = player_data['match_stats']
                gameState.player.playerStats.kills = stats.get('kills')
                gameState.player.playerStats.deaths = stats.get('deaths')
                gameState.player.playerStats.assists = stats.get('assists')
                gameState.player.playerStats.mvps = stats.get('mvps')
                gameState.player.playerStats.score = stats.get('score')
            
            # Player weapons
            if 'weapons' in player_data:
                weapons = player_data['weapons']
                grenade_index = 1
                
                for weapon_key, weapon_data in weapons.items():
                    if weapon_data is None:
                        continue
                    
                    weapon_name = weapon_data.get('name', '').lower()
                    weapon_type = weapon_data.get('type', '')
                    
                    # Knife
                    if weapon_type == 'Knife' or 'knife' in weapon_name:
                        gameState.player.playerWeapons.weapon_knife['name'] = weapon_data.get('name')
                        gameState.player.playerWeapons.weapon_knife['paintkit'] = weapon_data.get('paintkit')
                        gameState.player.playerWeapons.weapon_knife['type'] = weapon_data.get('type')
                        gameState.player.playerWeapons.weapon_knife['state'] = weapon_data.get('state')
                    
                    # Primary weapon
                    elif weapon_type == 'Rifle' or weapon_type == 'SniperRifle' or weapon_type == 'Machine Gun' or weapon_type == 'Shotgun' or weapon_type == 'Submachine Gun':
                        gameState.player.playerWeapons.weapon_primary['name'] = weapon_data.get('name')
                        gameState.player.playerWeapons.weapon_primary['paintkit'] = weapon_data.get('paintkit')
                        gameState.player.playerWeapons.weapon_primary['type'] = weapon_data.get('type')
                        gameState.player.playerWeapons.weapon_primary['state'] = weapon_data.get('state')
                        gameState.player.playerWeapons.weapon_primary['ammo_clip'] = weapon_data.get('ammo_clip')
                        gameState.player.playerWeapons.weapon_primary['ammo_reserve'] = weapon_data.get('ammo_reserve')
                        gameState.player.playerWeapons.weapon_primary['ammo_clip_max'] = weapon_data.get('ammo_clip_max')
                    
                    # Secondary weapon (pistol)
                    elif weapon_type == 'Pistol':
                        gameState.player.playerWeapons.weapon_secondary['name'] = weapon_data.get('name')
                        gameState.player.playerWeapons.weapon_secondary['paintkit'] = weapon_data.get('paintkit')
                        gameState.player.playerWeapons.weapon_secondary['type'] = weapon_data.get('type')
                        gameState.player.playerWeapons.weapon_secondary['state'] = weapon_data.get('state')
                        gameState.player.playerWeapons.weapon_secondary['ammo_clip'] = weapon_data.get('ammo_clip')
                        gameState.player.playerWeapons.weapon_secondary['ammo_reserve'] = weapon_data.get('ammo_reserve')
                        gameState.player.playerWeapons.weapon_secondary['ammo_clip_max'] = weapon_data.get('ammo_clip_max')
                    
                    # Grenades
                    elif weapon_type == 'Grenade' or weapon_type == 'C4':
                        grenade_key = f'grenade_{grenade_index}'
                        if grenade_index <= 4:
                            if grenade_key == 'grenade_1':
                                gameState.player.playerWeapons.grenade_1['name'] = weapon_data.get('name')
                                gameState.player.playerWeapons.grenade_1['paintkit'] = weapon_data.get('paintkit')
                                gameState.player.playerWeapons.grenade_1['type'] = weapon_data.get('type')
                                gameState.player.playerWeapons.grenade_1['state'] = weapon_data.get('state')
                                gameState.player.playerWeapons.grenade_1['ammo_reserve'] = weapon_data.get('ammo_reserve')
                            elif grenade_key == 'grenade_2':
                                gameState.player.playerWeapons.grenade_2['name'] = weapon_data.get('name')
                                gameState.player.playerWeapons.grenade_2['paintkit'] = weapon_data.get('paintkit')
                                gameState.player.playerWeapons.grenade_2['type'] = weapon_data.get('type')
                                gameState.player.playerWeapons.grenade_2['state'] = weapon_data.get('state')
                                gameState.player.playerWeapons.grenade_2['ammo_reserve'] = weapon_data.get('ammo_reserve')
                            elif grenade_key == 'grenade_3':
                                gameState.player.playerWeapons.grenade_3['name'] = weapon_data.get('name')
                                gameState.player.playerWeapons.grenade_3['paintkit'] = weapon_data.get('paintkit')
                                gameState.player.playerWeapons.grenade_3['type'] = weapon_data.get('type')
                                gameState.player.playerWeapons.grenade_3['state'] = weapon_data.get('state')
                                gameState.player.playerWeapons.grenade_3['ammo_reserve'] = weapon_data.get('ammo_reserve')
                            elif grenade_key == 'grenade_4':
                                gameState.player.playerWeapons.grenade_4['name'] = weapon_data.get('name')
                                gameState.player.playerWeapons.grenade_4['paintkit'] = weapon_data.get('paintkit')
                                gameState.player.playerWeapons.grenade_4['type'] = weapon_data.get('type')
                                gameState.player.playerWeapons.grenade_4['state'] = weapon_data.get('state')
                                gameState.player.playerWeapons.grenade_4['ammo_reserve'] = weapon_data.get('ammo_reserve')
                            grenade_index += 1
        
        return gameState
