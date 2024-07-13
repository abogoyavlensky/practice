# Complete the 'countingValleys' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER steps
#  2. STRING path
#

def countingValleys(steps, path):
    sea_level = 0
    valleys = 0
    current_level = sea_level

    for step in path:
        if step == 'U':
            current_level += 1
            if current_level == sea_level:
                valleys += 1
        elif step == 'D':
            current_level -= 1

    return valleys


print(countingValleys(8, "UDDDUDUU"))
