import numpy as np
from math import sqrt, log
import csv
# import matplotlib as plt
import matplotlib.pyplot as plt

def centrer_reduire(l: list) -> list:
    r = list()

    n = len(l)

    nb_crit = len(l[0])
    sums = [0 for _ in range(nb_crit)]
    squared_sums = [0 for _ in range(nb_crit)]

    for i in range(n):
        for j in range(nb_crit):
            sums[j] += l[i][j]
            squared_sums[j] += pow(l[i][j], 2)

    g = [e / n for e in sums]

    sigmas = [sqrt(squared_sums[j] / n - pow(g[j], 2)) for j in range(nb_crit)]

    print(sigmas)

    r = [[(row[j] - g[j]) / (sqrt(n) * sigmas[j]) for j in range(nb_crit)] for row in l]

    return r

opt_mapping = {"R": 0, "RS": 1, "RE": 2, "RSE": 3, "RI": 4, "RISE": 5}

f5 = "moyenne_cleared.csv"


l5 = []
l6 = []
l7 = []
l9 = []
l91 = []

with open(f5, "r") as f:
    lines = f.read()
    lines = lines.split("\n")
    for row in lines:
        split_row = row.split(",")
        print(split_row)
        l = [float(i) for i in split_row]
        # MU,OPT_USED,N2,T0,F0,F_AVG,F_MIN,F_MAX,AVG_BEST_AT,MIN_BEST_AT,MAX_BEST_AT,INIT_NB_TRUCKS,AVG_NB_TRUCKS,MIN_NB_TRUCKS,MAX_NB_TRUCKS,AVG_EXEC_T,MIN_EXEC_T,MAX_EXEC_T
        
        l5.append(l)

# print(l5)
# print(l6)
# print(l9)

r5 = centrer_reduire(l5)


# plt.scatter([row[3] for row in l5], [row[4] for row in l5])
# plt.scatter([row[3] for row in r5], [row[4] for row in r5])
# plt.show()

# print(sum([row[3] for row in r5]))
# print(sum([row[4] for row in r5]))

m5 = np.matrix(r5)

print(m5)
# iden = np.identity(len(l5)) * (1 / len(l5))
c5 = np.dot(m5.transpose(), m5)

# c5 = np.dot(c5_temp, m5)
with open("matrice.csv", "w", newline="") as f:
    for row in np.array(c5):
        csv.writer(f).writerow(["%.2f"%(float(e)) for e in row])

f_temp = []
f_f = []
for e in l5:
# for e in l5 + l6 + l7 + l9 + l91:
    f_temp.append(e[0])
    f_f.append(e[4])

l_temp_f = list(zip(f_temp, f_f))

l_temp_f.sort(key = lambda x : x[1])

avg = sum(l_tmp := [e[0] for e in l_temp_f if e[1] <= min([k[1] for k in l_temp_f])]) / len(l_tmp)
print(max(l_tmp))
avg