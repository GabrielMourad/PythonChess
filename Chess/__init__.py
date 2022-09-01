import numpy as n
import random

x = [[random.randint(1,50) for i in range(0, 5)] for i in range(0, 5)]

print(n.array(x))
print(x[1][0])

count = 0

for i in range(0,30):
    
    if i % 2 == 0:
            if i == 12:
                break
       
    count +=1

print(f"count = {count}")
        
