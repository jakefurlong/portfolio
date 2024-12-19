with open('input.txt', 'r') as file:
    lines = file.read().splitlines()

column1 = []
column2 = []

for line in lines:
    col1, col2 = line.split()
    column1.append(int(col1))
    column2.append(int(col2))

sim_index = 0

for i in column1:
    sim_index += column2.count(i) * i

print(sim_index)