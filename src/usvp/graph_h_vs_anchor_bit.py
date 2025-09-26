import csv
import matplotlib.pyplot as plt

y = []
x = []

with open('max_anchor_1.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        x.append(int(row[0]))
        y.append(int(row[1]))

print(x)
print(y)


plt.title("n=256, q=974269, anchor_step = 10")
plt.plot(x, y, marker='o')
plt.xticks(range(min(x), max(x)+1))
plt.xlabel("Hamming Weight")
plt.ylabel("Anchor Bit Position \n(Displacement From the Left)")
plt.grid(True)
plt.show()