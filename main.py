import matplotlib.pyplot as plt
from tqdm import tqdm
from multiprocessing import Pool


def clamp(v, lower, upper):
    return min(max(v, lower), upper)


def getStatForPoints(pt):
    return 2.0 * clamp(pt, 0, 100) + clamp(pt - 100, 0, 200) + 0.5 * clamp(pt - 300, 0, 400) + (1.0 / 3.0) * clamp(
        pt - 700, 0, 1200)


def bestRepartitionForPoints(maxPoints):
    bestMult = [0, 0, 1]
    for st in range(maxPoints + 1):
        strStat = getStatForPoints(st)
        agi = maxPoints - st
        agiStat = getStatForPoints(agi)
        critProb = agiStat / 1000.0
        strMult = (1.0 + strStat / 100.0)
        agiMult = critProb * 1.3 + (1.0 - critProb)
        mult = strMult * agiMult
        if mult > bestMult[2]:
            bestMult = [st, agi, mult]

    return bestMult


if __name__ == '__main__':
    print(getStatForPoints(100))
    print(getStatForPoints(300))
    print(getStatForPoints(700))
    print(getStatForPoints(1300))

    x = []
    y = []
    ym = []
    z = []
    zm = []
    m = []
    with Pool(10) as p:
        r = list(tqdm(p.imap(bestRepartitionForPoints, range(1, 1001))))

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

    ret = bestRepartitionForPoints(1780)
    print(ret)
    print(getStatForPoints(ret[0]))
    print(getStatForPoints(ret[1]))
