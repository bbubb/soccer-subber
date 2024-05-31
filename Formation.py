class Formation:
    def __init__(self, game_format, sequence, strategy):
        self.game_format = game_format
        self.sequence = sequence
        self.strategy = strategy
        self.positions = self._get_positions(sequence, strategy)

    formation_map = {
        ("3-4-1", "Balanced"): ['GK', 'LB', 'CB', 'RB', 'LM', 'LCM', 'RCM', 'RM', 'F'],
        ("3-4-1", "Offensive"): ['GK', 'LB', 'CB', 'RB', 'LW', 'LAM', 'RAM', 'RW', 'ST'],
        ("3-4-1", "Defensive"): ['GK', 'LB', 'CB', 'RB', 'LM', 'LDM', 'RDM', 'RM', 'CF'],
        ("3-1-2-1-1", "Triangles"): ['GK', 'LB', 'CB', 'RB', 'CDM', 'LM', 'RM', 'CAM', 'ST'],
    }

    def _get_positions(self, sequence, strategy):
        key = (sequence, strategy)
        return self.formation_map.get(key, [])  # Return empty list if not found
