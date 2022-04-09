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
    x = []
    y = []
    ym = []
    z = []
    zm = []
    m = []
    with Pool(10) as p:
        r = list(tqdm(p.imap(optimal_strength_agility_split, range(1, 1001))))

    print(r)

    for i in r:
        x.append(i[0] + i[1])
        y.append(i[0])
        z.append(i[1])
        m.append(i[2])
        ym.append(i[2] * i[0] / (i[0] + i[1]))
        zm.append(i[2] * i[1] / (i[0] + i[1]))

    print(x)
    print(y)
    print(z)
    print(m)
    fig, ax = plt.subplots()
    ax.bar(x, ym, label='Strength')
    ax.bar(x, zm, bottom=ym, label='Agility')
    ax.set_ylabel('Damage multiplier')
    ax.set_title('Best stat points repartition')
    ax.legend()
    plt.show()

    ret = optimal_strength_agility_split(1780)
    print(ret)
    print(characteristic(ret[0]))
    print(characteristic(ret[1]))
