import subprocess
import time
import csv
import graph

secret_specs = "front"
hamming = "10"
q = "3329"
algo = "LLL"
n = 60

n_val = []
stddevs = []
runtimes = []

open('experiment.csv', 'w', newline='')

#change depending on dependent variable type
for n in range(40, 110, 10):
    start_time = time.perf_counter()
    cmd = [
        "python3", "src/usvp/usvp.py",
        "--secret_type", "binary",
        "--N", str(n),
        "--Q", q,
        "--algo", algo,
        "--algo2", algo,
        "--hamming", str(hamming),
        "--num_workers", "1",
        "--secret_specs", secret_specs
    ]

    result = subprocess.run(cmd, capture_output=True, text=True).stdout

    print(result)

    stddev = -1
    for line in result.splitlines():
        if "STDDEV:" in line:
            stddev = line.split("STDDEV:")[1].strip()
            break

    print("Final stddev: ", stddev, "N: ",n)

    runtime = time.perf_counter()  - start_time

    n_val.append(n)
    stddevs.append(round(float(stddev),5))
    runtimes.append(runtime)

    with open('experiment.csv', 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([n,stddev,runtime])


print(n_val)
print(stddevs)

#change depending on dependent variable type
graph.make_graph(secret_specs, hamming, "Hamming Weight", q, algo)
#graph.make_graph(secret_specs, n, "N", q, algo)