import csv

data=[]
def q(f, t):
    return (1/(f*10+t)) * 1000000

with open("./moyenne_100_cleared.csv", "r") as f:
    l = f.read()
    lines = l.split("\n")
    for row in lines:
        split_row = row.split(",")
        fl = [float(i) for i in split_row]
        data.append([fl[0],fl[1],fl[2],fl[8]])
with open("./quality_100_x10.csv", "w", newline="") as f:
    for line in data:
        csv.writer(f).writerow([line[0], line[1],  q(line[2], line[3]), line[2], line[3]])
