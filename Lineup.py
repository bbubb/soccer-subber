import logging
from Interval import Interval

class Lineup:
    def __init__(self, match, team, formation, sub_goalie, min_playtime, dynamic_positions, intervals):
        self.match = match
        self.team = team
        self.formation = formation
        self.sub_goalie = sub_goalie
        self.min_playtime = min_playtime
        self.dynamic_positions = dynamic_positions
        self.intervals = [Interval(i + 1, match.game.total_game_time // intervals) for i in range(intervals)]
        self.lineups = []
        self.playtime = {player.id: 0 for player in team.squad}
        self.play_log = {player.id: [] for player in team.squad}
        self.total_field_playtime = 0
        self.position_high_scores = {}  # Track highest scores for each position
        self.calculate_total_field_playtime()
        self.assign_players()

    def calculate_total_field_playtime(self):
        self.total_field_playtime = len(self.formation.positions) * self.match.game.total_game_time
        logging.info(f"Total field playtime: {self.total_field_playtime}")
        interval_duration = self.match.game.total_game_time // len(self.intervals)
        logging.info(f"Interval duration: {interval_duration}")

    def assign_players(self):
        logging.info("Assigning players.")
        for interval in self.intervals:
            logging.info(f"Assigning players for Interval {interval.interval_number}")
            self.position_high_scores = {position: (None, -float('inf')) for position in self.formation.positions}  # Reset high scores
            players = self.assign_interval(interval)
            self.lineups.append({'interval': interval, 'players': players})
            logging.info("#############################################################################################################")

    def assign_interval(self, interval):
        position_scores = {position: [] for position in self.formation.positions}
        all_scores = []
        for position in self.formation.positions:
            logging.info("*****************************************************************************************************************")
            for player in self.team.squad:
                score = self.calculate_score(player, position, interval.interval_number)
                position_scores[position].append((player, score))
                all_scores.append((player, position, score))

        # Log scores for each player before sorting
        logging.info("*****************************************************************************************************************")

        self.log_scores(all_scores, interval.interval_number)

        all_scores.sort(key=lambda x: x[2], reverse=True)

        assigned_players = {}
        assigned_positions = set()
        assigned_players_set = set()

        for player, position, score in all_scores:
            if position not in assigned_positions and player not in assigned_players_set:
                assigned_players[position] = player
                assigned_positions.add(position)
                assigned_players_set.add(player)
                self.update_playtime_and_log(player.id, interval.interval_number, position)

        for position in self.formation.positions:
            if position not in assigned_positions:
                logging.warning(f"No available position {position} at interval {interval.interval_number}")

        return assigned_players

    def log_scores(self, all_scores, interval_number):
        scores_by_player = {}
        for player, position, score in all_scores:
            if player.id not in scores_by_player:
                scores_by_player[player.id] = []
            scores_by_player[player.id].append((position, score))

        for player_id, scores in scores_by_player.items():
            highest_score = max(score for _, score in scores)
            formatted_scores = [
                (position, f"*{score}*" if score == highest_score else score)
                for position, score in scores
            ]
            formatted_scores_str = [f'{pos:<4}{score:<6}' for pos, score in formatted_scores]  # Align positions and scores
            logging.info(f"Interval:{interval_number:<2} - Player {player_id:<2} scores: {formatted_scores_str}")

    def calculate_score(self, player, position, interval_number):
        score = 0
        min_playtime = player.min_playtime if player.min_playtime is not None else self.min_playtime
        score_min_playtime = (min_playtime - self.playtime[player.id]) if self.playtime[player.id] < min_playtime else 0
        score_max_playtime = (player.max_playtime - self.playtime[player.id])
        if position in player.preferred_positions:
            priority = player.preferred_positions[position]
            if position == 'GK' : score_preferred_positions = round(100 / priority)
            else : score_preferred_positions = round(100 / (priority * 5))
        else:
            score_preferred_positions = 0
        if self.lineups and player not in self.lineups[-1]['players'].values():
            score_sub = 20
        else:
            score_sub = 0
        if self.lineups and player in self.lineups[-1]['players'].values():
            score_position_continuity = 10 
        else:
            score_position_continuity = 0
        dynamic_positions = player.dynamic_positions if player.dynamic_positions is not None else self.dynamic_positions
        if dynamic_positions and not self.has_played_position_type(player, position):
            score_dynamic_positions = 10
        else:
            score_dynamic_positions = 0

        score = score_min_playtime + score_max_playtime + score_preferred_positions + score_sub + score_position_continuity + score_dynamic_positions

        # Update highest score for the position
        current_high_score = self.position_high_scores[position][1]
        if score > current_high_score:
            self.position_high_scores[position] = (player.id, score)

        player_log = f"Interval:{interval_number:<2} - Player {player.id:<2} - Position:{position:<3} - Score: {score:<3} = MinPlaytime({score_min_playtime:<2})+MaxPlaytime({score_max_playtime:<2})+PreferredPositions({score_preferred_positions:<3})+Sub({score_sub:<2})+PositionContinuity({score_position_continuity:<2})+DynamicPositions({score_dynamic_positions:<2})-DP:{dynamic_positions:<1}has_played_position_type:{self.has_played_position_type(player, position):<1}"
        if player.id == self.position_high_scores[position][0]:
            player_log = f"Interval:{interval_number:<2} **Player {player.id:<2}** Position:{position:<3} - Score: {score:<3} = MinPlaytime({score_min_playtime:<2})+MaxPlaytime({score_max_playtime:<2})+PreferredPositions({score_preferred_positions:<3})+Sub({score_sub:<2})+PositionContinuity({score_position_continuity:<2})+DynamicPositions({score_dynamic_positions:<2})-DP:{dynamic_positions:<1}has_played_position_type:{self.has_played_position_type(player, position):<1}"

        logging.info(player_log)
        
        return score

    def update_playtime_and_log(self, player_id, interval_number, position):
        self.playtime[player_id] += self.intervals[0].duration
        self.play_log[player_id].append((interval_number, position))
        logging.info(f"Interval:{interval_number:<2} - Player {player_id:<2} - Position:{position:<4} - Playtime({self.playtime[player_id]:<2})")

    def has_played_position_type(self, player, position):
        position_type = self.determine_position_type(position)
        for interval, pos in self.play_log[player.id]:
            if position_type == 'offensive' and (self.determine_position_type(pos) == 'offensive' or self.determine_position_type(pos) == 'mixed'):
                return True
            if position_type == 'defensive' and (self.determine_position_type(pos) == 'defensive' or self.determine_position_type(pos) == 'mixed'):
                return True
        return False

    @staticmethod
    def determine_position_type(position):
        mixed_keywords = ['M', 'G']
        offensive_keywords = ['S', 'F', 'A', 'W']
        defensive_keywords = ['B', 'D']

        if any(keyword in position for keyword in mixed_keywords):
            return 'mixed'
        if any(keyword in position for keyword in offensive_keywords):
            return 'offensive'
        if any(keyword in position for keyword in defensive_keywords):
            return 'defensive'
        return 'unknown'


    def get_lineups(self):
        return self.lineups

    def get_player_summary(self):
        summary = {}
        for player in self.team.squad:
            summary[player.name] = {
                'playtime': self.playtime[player.id],
                'play_log': self.play_log[player.id]
            }
        return summary

# import logging
# from Interval import Interval

# class Lineup:
#     def __init__(self, match, team, formation, sub_goalie, min_playtime, dynamic_positions, intervals):
#         self.match = match
#         self.team = team
#         self.formation = formation
#         self.sub_goalie = sub_goalie
#         self.min_playtime = min_playtime
#         self.dynamic_positions = dynamic_positions
#         self.intervals = [Interval(i + 1, match.game.total_game_time // intervals) for i in range(intervals)]
#         self.lineups = []
#         self.playtime = {player.id: 0 for player in team.squad}
#         self.play_log = {player.id: [] for player in team.squad}
#         self.total_field_playtime = 0
#         self.calculate_total_field_playtime()
#         self.assign_players()

#     def calculate_total_field_playtime(self):
#         self.total_field_playtime = len(self.formation.positions) * self.match.game.total_game_time
#         logging.info(f"Total field playtime: {self.total_field_playtime}")
#         interval_duration = self.match.game.total_game_time // len(self.intervals)
#         logging.info(f"Interval duration: {interval_duration}")
        
#     def assign_players(self):
#         logging.info("Assigning players.")
#         for interval in self.intervals:
#             logging.info(f"Assigning players for Interval {interval.interval_number}")
#             players = self.assign_interval(interval)
#             self.lineups.append({'interval': interval, 'players': players})

#     def assign_interval(self, interval):
#         all_scores = []
#         for position in self.formation.positions:
#             for player in self.team.squad:
#                 # if player not in self.injured_players:
#                     score = self.calculate_score(player, position, interval.interval_number)
#                     all_scores.append((player, position, score))
                    
#         # Log scores for each player before sorting
#         self.log_scores(all_scores, interval.interval_number)

#         all_scores.sort(key=lambda x: x[2], reverse=True)

#         assigned_players = {}
#         assigned_positions = set()
#         assigned_players_set = set()

#         for player, position, score in all_scores:
#             if position not in assigned_positions and player not in assigned_players_set:
#                 assigned_players[position] = player
#                 assigned_positions.add(position)
#                 assigned_players_set.add(player)
#                 self.update_playtime_and_log(player.id, interval.interval_number, position)

#         for position in self.formation.positions:
#             if position not in assigned_positions:
#                 logging.warning(f"No available position {position} at interval {interval.interval_number}")

#         return assigned_players
    
#     def log_scores(self, all_scores, interval_number):
#         scores_by_player = {}
#         for player, position, score in all_scores:
#             if player.id not in scores_by_player:
#                 scores_by_player[player.id] = []
#             scores_by_player[player.id].append((position, score))

#         for player_id, scores in scores_by_player.items():
#             scores.sort(key=lambda x: x[1], reverse=True)
#             highest_score = scores[0][1]
#             formatted_scores = [
#                 (f"***('{position}', {score})***" if score == highest_score else (position, score))
#                 for position, score in scores
#             ]
#             logging.info(f"Interval {interval_number} - Player {player_id} scores: {formatted_scores}")

#     def calculate_score(self, player, position, interval_number):
#         score = 0
#         min_playtime = player.min_playtime if player.min_playtime is not None else self.min_playtime
#         score_min_playtime = (min_playtime - self.playtime[player.id]) if self.playtime[player.id] < min_playtime else 0
#         score_max_playtime = (player.max_playtime - self.playtime[player.id])
#         if position in player.preferred_positions:
#             priority = player.preferred_positions[position]
#             if position == 'GK' : score_preferred_positions = round(100 / priority)
#             else : score_preferred_positions = round(100 / (priority * 5))
#         else: score_preferred_positions = 0
#         if self.lineups and player not in self.lineups[-1]['players'].values():
#             score_sub = 20
#         else: score_sub = 0
#         if self.lineups and player in self.lineups[-1]['players'].values():
#             score_position_continuity = 10 
#         else: score_position_continuity = 0
#         dynamic_positions = player.dynamic_positions if player.dynamic_positions is not None else self.dynamic_positions
#         if dynamic_positions and not self.has_played_position_type(player, position):
#             score_dynamic_positions = 10
#         else: score_dynamic_positions = 0
#         score = score_min_playtime + score_max_playtime + score_preferred_positions + score_sub + score_position_continuity + score_dynamic_positions
#         logging.info(f"Player:{player.id} - Position:{position} - Score:{score}=MinPlaytime({score_min_playtime})+MaxPlaytime({score_max_playtime})+PreferredPositions({score_preferred_positions})+Sub({score_sub})+PositionContinuity({score_position_continuity})+DynamicPositions({score_dynamic_positions}) - DP:{dynamic_positions} has_played_position_type: {self.has_played_position_type(player, position)})")
#         return score

#     def update_playtime_and_log(self, player_id, interval_number, position):
#         self.playtime[player_id] += self.intervals[0].duration
#         self.play_log[player_id].append((interval_number, position))
#         logging.info(f"Interval:{interval_number} - Player:{player_id} - Position:{position} - Playtime({self.playtime[player_id]})")

#     def has_played_position_type(self, player, position):
#         position_type = self.determine_position_type(position)
#         for interval, pos in self.play_log[player.id]:
#             if position_type == 'offensive' and self.determine_position_type(pos) == 'offensive' or self.determine_position_type(pos) == 'mixed':
#                 return True
#             if position_type == 'defensive' and self.determine_position_type(pos) == 'defensive'or self.determine_position_type(pos) == 'mixed':
#                 return True
#         return False

#     @staticmethod
#     def determine_position_type(position):
#         mixed_keywords = ['M', 'G']
#         offensive_keywords = ['S', 'F', 'A', 'W']
#         defensive_keywords = ['B', 'D']

#         if any(keyword in position for keyword in mixed_keywords):
#             return 'mixed'
#         if any(keyword in position for keyword in offensive_keywords):
#             return 'offensive'
#         if any(keyword in position for keyword in defensive_keywords):
#             return 'defensive'
#         return 'unknown'

#     def get_lineups(self):
#         return self.lineups

#     def get_player_summary(self):
#         summary = {}
#         for player in self.team.squad:
#             summary[player.name] = {
#                 'playtime': self.playtime[player.id],
#                 'play_log': self.play_log[player.id]
#             }
#         return summary
