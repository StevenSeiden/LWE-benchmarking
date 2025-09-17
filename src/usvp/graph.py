import csv
import matplotlib.pyplot as plt
import sys

def make_graph(secret_position, other_var, other_var_name, q, algo):
    y = []
    stddevs = []
    runtimes = []

    with open('experiment.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            y.append(row[1])
            stddevs.append(row[2])
            runtimes.append(row[3])

    print(y)
    print(stddevs)
    print(runtimes)

    plt.title((secret_position + "-Loaded Secret.\n" +
               other_var_name + "=" + str(other_var) + ", Q=" + q + ", Algo=").title() + algo)
    plt.plot(y, stddevs, marker='o')
    plt.xlabel("n")
    plt.ylabel("Standard Deviation")
    plt.grid(True)
    plt.show()

    plt.plot(y, runtimes, marker='o')
    plt.title((secret_position+"-Loaded Secret.\n"+
              other_var_name+"="+str(other_var)+", Q="+q+", Algo=").title()+algo)
    plt.xlabel("n")
    plt.ylabel("Runtime (s)")
    plt.grid(True)
    plt.show()

#run if experiment needs to be preempted
if __name__ == "__main__":
                #secret_position, other_var, other_var_name, q, algo
    make_graph(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])