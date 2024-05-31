# def soccer_substitution_algorithm(total_game_time, num_players, formation, intervals, sub_goalie):
#     interval_duration = total_game_time // intervals
#     halftime = total_game_time // 2

#     playtime = [0] * num_players
#     positions = {i: [] for i in range(num_players)}
#     intervals_log = {i: [] for i in range(num_players)}
#     substitutions = []

#     if sub_goalie:
#         goalkeeper_1 = 0
#         goalkeeper_2 = 1
#         playtime[goalkeeper_1] = halftime
#         playtime[goalkeeper_2] = halftime
#         positions[goalkeeper_1].append("GK")
#         positions[goalkeeper_2].append("GK")
#         field_players = list(range(2, num_players))
#     else:
#         goalkeeper = 0
#         playtime[goalkeeper] = total_game_time
#         positions[goalkeeper].append("GK")
#         field_players = list(range(1, num_players))

#     print("Field players:", field_players)

#     total_field_playtime = sum(count * total_game_time for count in formation)
#     print("Total field playtime:", total_field_playtime)
#     min_playtime = halftime
#     print("Minimum playtime per player:", min_playtime)
#     extra_intervals = (total_field_playtime - (min_playtime * len(field_players))) // interval_duration
#     print("Extra intervals:", extra_intervals)

#     # Create position array for each interval
#     interval_positions = []
#     for _ in range(intervals):
#         interval_positions.append([position for i, count in enumerate(formation) for position in ["D", "M", "F"][i:i + 1] * count])

#     print("Interval positions:", interval_positions)

#     # Assign players to positions based on conditions
#     for interval_index in range(intervals):
#         current_positions = interval_positions[interval_index]
#         for position in current_positions:
#             assigned = False
#             for player in field_players:
#                 if player not in [p for p, pos in positions.items() if interval_index in intervals_log[p]]:
#                     if (playtime[player] < total_game_time and 
#                         (position not in positions[player] or len(set(positions[player])) < len(formation))):
#                         playtime[player] += interval_duration
#                         positions[player].append(position)
#                         intervals_log[player].append(interval_index)
#                         assigned = True
#                         break
#             if not assigned:
#                 for player in field_players:
#                     if playtime[player] < total_game_time:
#                         playtime[player] += interval_duration
#                         positions[player].append(position)
#                         intervals_log[player].append(interval_index)
#                         break

#     # Ensure minimum playtime
#     for player in field_players:
#         while playtime[player] < min_playtime:
#             for interval_index in range(intervals):
#                 if interval_index not in intervals_log[player]:
#                     playtime[player] += interval_duration
#                     positions[player].append(positions[player][-1])  # Keep the same position
#                     intervals_log[player].append(interval_index)
#                     if playtime[player] >= min_playtime:
#                         break

#     # Distribute extra intervals evenly among eligible players
#     extra_interval_players = [player for player in field_players if playtime[player] < total_game_time]
#     for _ in range(extra_intervals):
#         if extra_interval_players:
#             player = extra_interval_players.pop(0)
#             playtime[player] += interval_duration
#             if playtime[player] < total_game_time:
#                 extra_interval_players.append(player)

#     print("Playtime after distributing extra intervals:", playtime)

#     return playtime, positions, intervals_log, substitutions

# # Parameters
# total_game_time = 60
# num_players = 14
# formation = [3, 4, 1]
# intervals = 6
# sub_goalie = False

# # Run the algorithm
# playtime, positions, intervals_log, substitutions = soccer_substitution_algorithm(total_game_time, num_players, formation, intervals, sub_goalie)

# # Prepare results
# results = []
# for i in range(num_players):
#     results.append(f"Player {i + 1}: Playtime = {playtime[i]} minutes, Positions = {positions[i]}, Intervals = {intervals_log[i]}")

# # Print results
# for result in results:
#     print(result)

# # Print substitutions in structured format
# print("\nSubstitutions:")
# for subs in substitutions:
#     print(subs)