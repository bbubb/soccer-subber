class Player:
    def __init__(self, player_id, name, max_playtime, preferred_positions=None, dynamic_positions=None, min_playtime=None):
        self.id = player_id
        self.name = name
        self.max_playtime = max_playtime
        self.preferred_positions = preferred_positions or {}
        self.dynamic_positions = dynamic_positions if dynamic_positions is not None else None
        self.min_playtime = min_playtime if min_playtime is not None else None

    def __repr__(self):
        return f"Player({self.id}, {self.name})"
