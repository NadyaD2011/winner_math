import random
import itertools


def simulate_matches(teams, num_simulations=1000):
    results = {team: 0 for team in teams}
    matches = list(itertools.combinations(teams.keys(), 2))

    for team1, team2 in matches:
        wins_team1, wins_team2 = 0, 0

        for _ in range(num_simulations):
            p_team1 = teams[team1] / (teams[team1] + teams[team2])
            if random.random() < p_team1:
                wins_team1 += 1
            else:
                wins_team2 += 1

        if wins_team1 > wins_team2:
            results[team1] += 3
        elif wins_team2 > wins_team1:
            results[team2] += 3
        else:
            results[team1] += 1
            results[team2] += 1

    sorted_results = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))
    return {team: rank for rank, team in enumerate(sorted_results, 1)}


def play_match(team1, team2, ratings):
    if ratings[team1] / (ratings[team1] + ratings[team2]) > random.random():
        return team1
    else:
        return team2


def simulate_tournament(groups, num_simulations=10000):
    all_teams = set(team for group in groups.values() for team in group)
    winners = {team: 0 for team in all_teams}
    second_places = {team: 0 for team in all_teams}
    third_places = {team: 0 for team in all_teams}

    for _ in range(num_simulations):
        group_results = {group_name: simulate_matches(group_teams) for group_name, group_teams in groups.items()}

        first_semi_finalist = list(group_results['gruppa_d'].keys())[list(group_results['gruppa_d'].values()).index(1)]
        second_semi_finalist = list(group_results['gruppa_e'].keys())[list(group_results['gruppa_e'].values()).index(2)]
        third_semi_finalist = list(group_results['gruppa_d'].keys())[list(group_results['gruppa_d'].values()).index(2)]
        fourth_semi_finalist = list(group_results['gruppa_e'].keys())[list(group_results['gruppa_e'].values()).index(1)]

        first_semi_final = {first_semi_finalist: groups['gruppa_d'][first_semi_finalist], second_semi_finalist: groups['gruppa_e'][second_semi_finalist]}
        second_semi_final = {third_semi_finalist: groups['gruppa_d'][third_semi_finalist], fourth_semi_finalist: groups['gruppa_e'][fourth_semi_finalist]}

        finalists = [
            play_match(*first_semi_final.keys(), first_semi_final),
            play_match(*second_semi_final.keys(), second_semi_final)
        ]

        third_place_contenders = [team for team in list(first_semi_final.keys()) + list(second_semi_final.keys()) if team not in finalists]

        final_winner = play_match(finalists[0], finalists[1], {**groups['gruppa_d'], **groups['gruppa_e']})
        second_place = [team for team in finalists if team != final_winner][0]
        third_place_winner = play_match(third_place_contenders[0], third_place_contenders[1], {**groups['gruppa_d'], **groups['gruppa_e']})

        winners[final_winner] += 1
        second_places[second_place] += 1
        third_places[third_place_winner] += 1

    return winners, second_places, third_places


def calculate_probabilities(winners, second_places, third_places, num_simulations):
    champions_prob = {team: wins / num_simulations for team, wins in winners.items()}

    finalists_prob = {team: (winners[team] + second_places[team]) / num_simulations for team in winners}

    podium_prob = {team: (winners[team] + second_places[team] + third_places[team]) / num_simulations for team in winners}

    champions_prob = dict(sorted(champions_prob.items(), key=lambda x: x[1], reverse=True))
    finalists_prob = dict(sorted(finalists_prob.items(), key=lambda x: x[1], reverse=True))
    podium_prob = dict(sorted(podium_prob.items(), key=lambda x: x[1], reverse=True))

    return champions_prob, finalists_prob, podium_prob


def main():
    gruppa_d = {'Франция': 90, 'Дания': 85, 'Австралия': 75, 'Тунис': 70}
    gruppa_e = {'Германия': 0.85, 'Япония': 0.65, 'Испания': 0.85, 'Коста-Рика': 0.55}
    groups = {'gruppa_d': gruppa_d, 'gruppa_e': gruppa_e}

    num_simulations = 1000
    winners, second_places, third_places = simulate_tournament(groups, num_simulations)

    champions_prob, finalists_prob, podium_prob = calculate_probabilities(winners, second_places, third_places, num_simulations)

    print(f"Вероятность стать чемпионами:\n{champions_prob}")
    print(f"Вероятность выйти в финал:\n{finalists_prob}")
    print(f"Вероятность попасть на пьедестал:\n{podium_prob}")


if __name__ == "__main__":
    main()
