import numpy as np
import matplotlib.pyplot as plt
import json

l1 = []
l2 = []
l3 = []
l4 = []
l5 = []
l6 = []
e1 = 0
e2 = 0
e3 = 0
e4 = 0
e5 = 0
e6 = 0

with open("./fitness_evolution/evolution.json", "r") as json_file:
    content: dict = json.loads(json_file.read())
    l1 = content.get("g0", {}).get("f")
    e1 = content.get("g0", {}).get("e")
    print(min(l1))
    # l2 = content.get("c1", {}).get("f")
    # e2 = content.get("c1", {}).get("e")

    l3 = content.get("c2", {}).get("f")
    e3 = content.get("c2", {}).get("e")
    print(min(l3))
    # l4 = content.get("g0", {}).get("f")
    # e4 = content.get("g0", {}).get("e")

    # l5 = content.get("g1", {}).get("f")
    # e5 = content.get("g1", {}).get("e")

    l6 = content.get("g2", {}).get("f")
    e6 = content.get("g2", {}).get("e")
    print(min(l6))
n1 = len(l1)
# n2 = len(l2)
n3 = len(l3)
# n4 = len(l4)
# n5 = len(l5)
n6 = len(l6)

ts1 = e1 / n1 / pow(10, 9)
# ts2 = e2 / n2 / pow(10, 9)
ts3 = e3 / n3 / pow(10, 9)
# ts4 = e4 / n4 / pow(10, 9)
# ts5 = e5 / n5 / pow(10, 9)
ts6 = e6 / n6 / pow(10, 9)

with open("./bonne_solution_100.txt", "r") as f:
        l7 = eval(f.read())

temps = 11557.46733880043
print(min(l7))
n7 = len(l7)
ts7 = temps /n7
# print(f"N {n1} E {e1} TS {ts1}")

# plt.plot([i * ts1 for i in range(n1)], l1, label=f"Classique 1")
# plt.plot([i * ts2 for i in range(n2)], l2, label=f"Classique 2")

plt.plot([i  for i in range(n3)], l3, label=f"Recuit classique")

# plt.plot([i * ts4 for i in range(n4)], l4, label=f"Granulaire 1")
# plt.plot([i * ts5 for i in range(n5)], l5, label=f"Granulaire 2")

plt.plot([i  for i in range(n6)], l6, label=f"Recuit granulaire")

plt.plot([i  for i in range(n7)], l7, label=f"Tabou")
plt.legend()
plt.xlabel("Nombre d'itérations")
plt.ylabel("Fitness")
plt.title("Évolution de la fitness au cours du temps")
plt.show()

# plt.plot([i * ts4 for i in range(n4)], l4, label=f"Granulaire 1")
# plt.plot([i * ts5 for i in range(n5)], l5, label=f"Granulaire 2")
# plt.plot([i * ts6 for i in range(n6)], l6, label=f"Granulaire 3")
# plt.legend()
# plt.xlabel("Temps en ns")
# plt.ylabel("Fitness")
# plt.title("Évolution de la fitness au cours du temps")
# plt.show()