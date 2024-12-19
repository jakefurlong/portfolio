# GENERATE A LIST OF REPORTS

with open('test.txt', 'r') as file:
    lines = file.read().splitlines()

reports = []

for line in lines:
    report = []
    for i in line.split():
        report.append(int(i))
    reports.append(report)

# VALIDATION FUNCTION

def is_valid(report):
    if len(set(report)) != len(report):
        return False
    if sorted(report) != report and list(reversed(sorted(report))) != report:
        return False
    for i in range(len(report) - 1):
        if abs(report[i] - report[i+1]) > 3:
            return False
    return True


# PROCESS REPORTS FOR SCORING

score = 0

for report in reports:
    if is_valid(report):
        score += 1
    else:
        for i in range(len(report)):
            n = (report[i])
            report.remove(report[i])
            if is_valid(report):
                score += 1
                break
            else:
                report.insert(i, n)

print("Score:", score)