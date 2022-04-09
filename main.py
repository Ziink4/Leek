import matplotlib.pyplot as plt
from tqdm import tqdm
from multiprocessing import Pool

CRITICAL_MULTIPLIER = 1.3


def clamp(v, lower, upper):
    return min(max(v, lower), upper)


def characteristic(points):
    return 2.0 * clamp(points, 0, 100) \
           + clamp(points - 100, 0, 200) \
           + 0.5 * clamp(points - 300, 0, 400) \
           + (1.0 / 3.0) * clamp(points - 700, 0, 1200)


def critical_chance(agility):
    return agility / 1000.0


def damage_multiplier(strength):
    return 1.0 + strength / 100.0


def optimal_strength_agility_split(max_points):
    best_mult = [0, 0, 1]
    for str_points in range(max_points + 1):
        str_stat = characteristic(str_points)
        agi_points = max_points - str_points
        agi_stat = characteristic(agi_points)
        crit_chance = critical_chance(agi_stat)
        str_mult = damage_multiplier(str_stat)
        agi_mult = crit_chance * CRITICAL_MULTIPLIER + (1.0 - crit_chance)
        mult = str_mult * agi_mult
        if mult > best_mult[2]:
            best_mult = [str_points, agi_points, mult]

    return best_mult


if __name__ == '__main__':
    with Pool(10) as p:
        results = list(tqdm(p.imap(optimal_strength_agility_split, range(1, 1001))))

    points_invested = []
    strength_part = []
    agility_part = []
    for str_points, agi_points, mult in results:
        points_invested.append(str_points + agi_points)
        strength_part.append(mult * str_points / (str_points + agi_points))
        agility_part.append(mult * agi_points / (str_points + agi_points))

    fig, ax = plt.subplots()
    ax.bar(points_invested, strength_part, label='Strength')
    ax.bar(points_invested, agility_part, bottom=strength_part, label='Agility')
    ax.set_xlabel('Points Invested')
    ax.set_ylabel('Damage Multiplier')
    ax.set_title('Optimal Strength/Agility Split')
    ax.legend()
    plt.show()
