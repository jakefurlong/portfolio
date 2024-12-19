
with open('input.txt', 'r') as file:
    lines = file.read().splitlines()

column1 = []
column2 = []

for line in lines:
    col1, col2 = line.split()
    column1.append(int(col1))
    column2.append(int(col2))

sorted_column1 = sorted(column1)
sorted_column2 = sorted(column2)


total = 0

for i in range(len(sorted_column1)):
    total += abs(sorted_column2[i] - sorted_column1[i])

print(total)