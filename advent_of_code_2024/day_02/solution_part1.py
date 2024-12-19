# convert part 1 solution to function, iterate over each report popping out elements one at a time
# if any combo returns a score of 3, it's safe

########################################################

# GENERATE A LIST OF REPORTS

with open('input.txt', 'r') as file:
    lines = file.read().splitlines()

reports = []

for line in lines:
    report = []
    for i in line.split():
        report.append(int(i))
    reports.append(report)

########################################################

# PROCESS REPORT FOR SCORING

def is_valid(report):
    if len(set(report)) != len(report):
        return False
    if sorted(report) != report and list(reversed(sorted(report))) != report:
        return False
    for i in range(len(report) - 1):
        if abs(report[i] - report[i+1]) > 3:
            return False
    return True

score = 0

for report in reports:
    if is_valid(report):
        #print("Report:", report, "is valid.")
        score += 1

print("Score:", score)
