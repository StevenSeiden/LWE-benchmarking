import csv
import matplotlib.pyplot as plt
import sys
import pandas as pd
position = "back"
n = "64"
hw = "15"
data = pd.read_csv(f"experiment random_fill {position} {n} {hw}.csv")
x = data.columns[1]
stddevs = data.columns[2]
runtimes = data.columns[3]



if position == "front":
    primary_color = "pink"
    secondary_color = "red"
    highlight_color = "blue"
    anchor = "Right"
else:
    primary_color = "lightblue"
    secondary_color = "blue"
    highlight_color = "red"
    anchor = "Left"

plt.figure(figsize=(8, 6))
boxplot = data.boxplot(column=stddevs,
                        by=x,
                        patch_artist = True,
                        boxprops=dict(facecolor=primary_color, color=secondary_color),
                        whiskerprops=dict(color=secondary_color),
                        capprops=dict(color=secondary_color),
                        medianprops=dict(color=highlight_color)
)


plt.title(f"Standard Deviation as Secret Spreads From the {position}")
plt.suptitle(f"n={n}, HW = {hw}, q = 3329, algo = LLL")
plt.ylabel("Standard Deviation")
plt.xlabel(f"{anchor} Anchor Bit Position")
plt.xticks(rotation=45)
plt.tight_layout()

plt.ylim(.25, .75)

plt.show()


plt.figure(figsize=(8, 6))
boxplot = data.boxplot(column=runtimes,
                        by=x,
                        patch_artist = True,
                        boxprops = dict(facecolor=primary_color, color=secondary_color),
                        whiskerprops = dict(color=secondary_color),
                        capprops = dict(color=secondary_color),
                        medianprops = dict(color=highlight_color),
                       )



plt.title(f"Runtimes as Secret Spreads From the {position}")
plt.suptitle(f"n={n}, HW = {hw}, q = 3329, algo = LLL")
plt.ylabel("Runtime (s)")
plt.xlabel(f"{anchor} Anchor Bit Position")
plt.xticks(rotation=45)
plt.tight_layout()

plt.ylim(1, 15)
plt.show()
