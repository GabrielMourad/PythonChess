import numpy as n
import random

x = [[random.randint(1, 50) for i in range(0, 5)] for i in range(0, 5)]

print(n.array(x))

count = 0

for i in x:
    for j in i:
        print(j)


print(f"count = {count}")
