from Lineup import Lineup


class GamePlan:
    def __init__(self, intervals, sub_goalie=False, min_playtime=0, dynamic_positions=False):
        self.intervals = intervals
        self.sub_goalie = sub_goalie
        self.min_playtime = min_playtime
        self.dynamic_positions = dynamic_positions

    def generate_lineup(self, match, team, formation):
        return Lineup(match, team, formation, self.sub_goalie, self.min_playtime, self.dynamic_positions, self.intervals)