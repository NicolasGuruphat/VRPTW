from greedy_solution import greedy_solution
from model.VRPTW import VRPTW
from utils import fitness

files = [
    "101",
    "101 short",
    "102",
    "102 short",
    "111",
    "111 short",
    "112",
    "112 short",
    "201",
    "201 short",
    "202",
    "202 short",
    "1101",
    "1101 short",
    "1102",
    "1102 short",
    "1201",
    "1201 short",
    "1202",
    "1202 short",
]

for file in files:
    vrp = VRPTW(f"data{file}.vrp")
    vrp.routes = greedy_solution(vrp)
    fit = fitness(vrp)
    with open("greedy_res_twless.txt", "a") as f:
        f.write(f"File {file} fitness {float(fit)}\n")
