import logging
from GamePlan import GamePlan
from Game import Game
from Match import Match
from Team import Team
from Formation import Formation
from Player import Player

logging.basicConfig(level=logging.INFO)

# Define the game
game = Game(total_game_time=60, format="9v9")  # Assuming total game time in minutes

# Define players
players_home = [
    Player(player_id=1, name="Player 1", max_playtime=60, preferred_positions={'GK': 1}),
    Player(player_id=2, name="Player 2", max_playtime=40, preferred_positions={'LB': 1, 'LM': 2}),
    Player(player_id=3, name="Player 3", max_playtime=40, preferred_positions={'CB': 1, 'F': 2, 'LCM': 3}),
    Player(player_id=4, name="Player 4", max_playtime=40, preferred_positions={'RB': 1, }),
    Player(player_id=5, name="Player 5", max_playtime=40, preferred_positions={'LM': 1, 'LCM': 2, 'F': 3}),
    Player(player_id=6, name="Player 6", max_playtime=40, preferred_positions={'LCM': 1, 'D': 2, 'B': 2}),
    Player(player_id=7, name="Player 7", max_playtime=40, preferred_positions={'RCM': 1, 'RB': 2}),
    Player(player_id=8, name="Player 8", max_playtime=40, preferred_positions={'RM': 1}),
    Player(player_id=9, name="Player 9", max_playtime=40, preferred_positions={'F': 1, 'LM': 2, 'LCM': 3}),
    Player(player_id=10, name="Player 10", max_playtime=40, preferred_positions={'F': 1, 'RCM': 2}),
    Player(player_id=11, name="Player 11", max_playtime=30, preferred_positions={'LB': 1, 'LM': 2}),
    Player(player_id=12, name="Player 12", max_playtime=30, preferred_positions={'CM': 1, 'F': 2, 'LCM': 3}),
    Player(player_id=13, name="Player 13", max_playtime=30, preferred_positions={'RM': 1, 'RB': 2}),
    Player(player_id=14, name="Player 14", max_playtime=30, preferred_positions={'LM': 1, 'LCM': 2, 'F': 3}),
]

# Define teams
home_team = Team(name="Home Team", squad=players_home)

# Define formation
formation = Formation(game_format="9v9", sequence="3-4-1", strategy="Balanced")

# Define match
match = Match(game=game, home_team=home_team, away_team=None)  # Assuming only home team for simplicity

# Define game plan
game_plan = GamePlan(sub_goalie=False, min_playtime=10, dynamic_positions=True, intervals=6)

# Generate lineup for home team
lineup_home = game_plan.generate_lineup(match, home_team, formation)

# Print player summaries
logging.info("Player Summaries:")
for player_summary in lineup_home.get_player_summary().items():
    logging.info(f"Player: {player_summary[0]}, Playtime: {player_summary[1]['playtime']}, Play Log: {player_summary[1]['play_log']}")
