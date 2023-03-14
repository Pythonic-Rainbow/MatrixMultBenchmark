np = int(input('Enter the first number of the Matrices class: '))
m = int(input('Enter the second number of the Matrices class: '))

computation = np ** 2 * m
print(str(computation) + ' computations')

t = float(input('Enter time: '))
power = float(input('Enter power: '))

comp_per_time = int(computation / t / 1000)
print(str(comp_per_time) + ' computations per second')

comp_per_j = int(computation / (power * t) / 1000)
print(str(comp_per_j) +' computations per joule')