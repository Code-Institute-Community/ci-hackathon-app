from itertools import combinations
import json
import math

LMS_LEVELS = {
    "programme_preliminaries": 1,
    "programming_paradigms": 1,
    "html_fundamentals": 1,
    "css_fundamentals": 1,
    "user_centric_frontend_development": 1,
    "javascript_fundamentals": 2,
    "interactive_frontend_development": 2,
    "python_fundamentals": 3,
    "practical_python": 3,
    "data_centric_development": 3,
    "full_stack_frameworks with django": 4,
    "alumni": 5,
    "staff": 6,
}


def choose_team_sizes(participants, teamsize):
    """ Calculates the number of teams and teamsizes needed based on the amount
    of participants and a given wanted team size

    If the remainder when comparing participants  to the wanted teamsize is 0,
    all teams will be the wanted team size.

    If the the remainder is not 0 and more then half of the wanted team size,
    the remainder will be the size of the last team.

    If the the remainder is not 0, but less then half of the wanted team size,
    the the remainder will be distributed to one or more teams.

    Returns a list where the number of elements is represents the amount of
    teams and the value of each element represents the number of team members
    within that team """
    remainder = len(participants) % teamsize
    num_teams = int(len(participants) / teamsize)
    if remainder > 0:
        split_to_teams = remainder < (teamsize / 2)
        if not split_to_teams:
            return [teamsize for team in range(num_teams)] + [remainder]
        else:
            teams = []
            for team in range(num_teams):
                if remainder > 0:
                    teams.append(teamsize + 1)
                    remainder -= 1
                    continue
                teams.append(teamsize)
            return teams

    # return normal teams based on teamsize
    return [teamsize for team in range(num_teams+1)]


def group_participants(participants, num_teams):
    """ Groups participants into groups based on their progression level
    througout the program

    Returns a dict with the level as key and the grouped student list as value
    and also returns the total level each team should have """
    participant_groups = {}
    hackathon_level = 0
    for participant in participants:
        participant_level = LMS_LEVELS[participant.current_lms_module]
        hackathon_level += participant_level
        participant_groups.setdefault(participant_level, [])
        participant_groups[participant_level].append({
                'name': participant.username,
                'level': participant_level
                })

    team_level = math.floor(hackathon_level/num_teams)
    print(f'Team Level: {team_level}')
    return participant_groups, team_level


def find_all_combinations(group_levels, team_sizes, team_level):
    possible_combinations = {}
    for team_size in list(set(team_sizes)):
        possible_combinations[team_size] = find_combinations(
            group_levels, team_size, team_level)
    return possible_combinations


def find_combinations(group_levels, team_size, team_level):
    choices = [int(progression_level) for progression_level
               in group_levels]
    return [pair for pair in combinations(choices, team_size)
            if sum(pair) == team_level]


def find_tuple_combinations(combination_tuples, team_sizes, hackathon_level):
    combination_list = [list(t) for t in combination_tuples]
    print(combination_tuples)
    print(team_sizes)
    print(hackathon_level)
    team_sizes_dict = {}
    for team_size in team_sizes:
        team_sizes_dict.setdefault(team_size, 0)
        team_sizes_dict[team_size] += 1
    print(team_sizes_dict)
    all_options = {}
    for combination in combination_tuples:
        num_combinations = team_sizes_dict[len(combination)]
        all_options.setdefault(len(combination), {})
        combo_key = ''.join([str(int) for int in list(combination)])
        all_options[len(combination)].setdefault(combo_key, [])
        for i in range(1, num_combinations+1):
            list_of_options = [list(combination) for i in range(i)]
            all_options[len(combination)][combo_key].append(
                list_of_options)
    print(all_options)
    #result = combine(all_options, len(team_sizes), team_sizes, max_level)
    return


def combine(all_options, combinations, num_teams, team_sizes, team_sizes_dict, hackathon_level):
    """ We need to retrieve the combination of teams that have the right skill
    number of teams available with that skill combination and sum overall and


    """
    max_team_size = max(team_sizes)
    min_combination_sum = min([sum(c) for c in combinations
                               if len(c) == max_team_size])
    print(min_combination_sum)
    # for team_size in list(set(team_sizes)):
    #     right_len_combos = [c for c in combinations if len(c) == team_size]
    #     for i, right_len_combo in enumerate(right_len_combos):
    #         combo_key = ''.join([str(int) for int in list(right_len_combo)])
    #         other_combos = [c for c in right_len_combos if c != right_len_combo]
            
    #         print(combo_key)
    #         print(other_combo_keys)
    return



def _combinations(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    #pool = (iterable, )
    pool = iterable
    print(pool)
    n = len(pool)
    #print(n)
    if r > n:
        print(f"{r} > {n}")
        print("return")
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)


def pick_from_participants(combination, participant_groups):
    """ Loop through the combiniaton of progression_levels and pick
    one participant from each of the progression_levels

    Returns the list of picked participants and the updated participant list
    """
    picked_participants = []
    # Check if there is options for each of the progression level in the
    # current combination
    check_sum = sum([
        1 for level in combination
        if participant_groups[level]
    ])
    if check_sum < len(combination):
        return None, participant_groups

    for level in combination:
        participant_list = participant_groups.get(level)
        participant = participant_list.pop()
        picked_participants.append(participant)

    return picked_participants, participant_groups


def pick_teams(participants, teamsize):
    print(len(participants))
    team_sizes = choose_team_sizes(participants, teamsize)
    #team_sizes = sorted(team_sizes, reverse=True)
    print(team_sizes)
    num_teams = len(team_sizes)
    participant_groups, team_level = group_participants(
        participants, num_teams)
    group_levels = list(participant_groups.keys())
    combinations = find_all_combinations(group_levels, team_sizes,
                                         team_level)
    print(combinations)
    teams = []
    c = 0
    next_team = team_sizes.pop()
    combination = combinations[next_team].pop()
    while team_sizes and combination and c < (num_teams * 4):
        print(len(team_sizes))
        picked_participants, participant_groups = pick_from_participants(
            combination=combination, participant_groups=participant_groups)

        if not picked_participants:
            print('did not pick any')
            try:
                combination = combinations[next_team].pop()
            except IndexError:
                combination = None
        else:
            print(picked_participants)
            print("")
            teams.append(picked_participants)
            next_team = team_sizes.pop()
        c += 1
    print(participant_groups)
    # print(num_teams)
    # print(len(teams))
    # while len(teams) < num_teams and combination and c < (num_teams * 4):

    #     picked_participants, participants = pick_from_participants(
    #         combination=combination, participants=participants)

    #     if not picked_participants:
    #         try:
    #             combination = list(combinations.pop())
    #         except IndexError:
    #             combination = None
    #     else:
    #         teams.append(picked_participants)

    #     c += 1
    # print(num_teams)
    # print(len(teams))

    return teams


def find_team_combinations(team_sizes, combinations, participant_groups):
    all_levels = []
    all_combinations = []
    for level, participants in list(participant_groups.items()):
        all_levels += [level for p in participants]
    for combination in combinations.values():
        all_combinations += list(combination)
    combos = find_tuple_combinations(all_combinations, team_sizes,
                                     sum(all_levels))
   # print(team_sizes)
   # print(all_levels)
   # print(combinations)
   # print(all_combinations)
   # print(combos)

    return all_levels


def dupe_combinations(d, sum_to, current=[]):
  if sum(current) == sum_to:
     yield current
  else:
    for i in d:
      if sum(current+[i]) <= sum_to:
         yield from dupe_combinations(d, sum_to, current+[i])