import subprocess
import time
import csv

def experiment(filename,secret_position,n,step,hamming,q):
    #secret_position = "back"
    secret_fill = "random_fill"
    secret_spread = 15
    #hamming = "10"
    #q = "3329"
    algo = "LLL"
    #n = 64

    secret_spreads = []
    stddevs = []
    runtimes = []

    #filename = "experiment.csv"
    open(filename, 'w', newline='')

    #change depending on dependent variable type
    for secret_spread in range(n, 10, step):
        i = 0
        while i < 5:
            start_time = time.perf_counter()
            cmd = [
                "python3", "src/usvp/usvp.py",
                "--secret_type", "binary",
                "--N", str(n),
                "--Q", str(q),
                "--algo", algo,
                "--algo2", algo,
                "--hamming", str(hamming),
                "--num_workers", "1",
                "--secret_specs", f"{secret_fill} {secret_position} {secret_spread}",
            ]

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            #result = subprocess.run(cmd, capture_output=True, text=True).stdout

            result = []

            for line in process.stdout:
                print(line, end="")
                result.append(line)

            result = "".join(result)

            #print(result)

            current_secret = "null"
            stddev = -1
            failed = False
            for line in result.splitlines():
                if "STDDEV:" in line:
                    stddev = line.split("STDDEV:")[1].strip()
                    break
                if "Secret made: " in line:
                    current_secret = line.split("Secret made: ")[1].strip()

            if "No reduction improvement" in result.split('\n')[-2]:
                with open('failed_secrets.csv', 'a', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow([current_secret, secret_spread])
                print("Experiment failed. Retrying...")
                i = i + 1
                continue

            runtime = time.perf_counter()  - start_time
            print("Final stddev: ", stddev, "\nRuntime: ", runtime, "\nSecret spread: ",secret_spread, "\nSecret: ", current_secret)


            secret_spreads.append(secret_spread)
            stddevs.append(round(float(stddev),5))
            runtimes.append(runtime)

            with open(filename, 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([current_secret,secret_spread,stddev,runtime])

            i = i + 1


    print(secret_spreads)
    print(stddevs)

if __name__ == "__main__":
    # experiment("experiment random_fill back 64.csv", "back", 64, -4)
    # experiment("experiment random_fill front 64.csv", "front", 64, -4)
    # experiment("experiment random_fill front 64 15.csv", "front", 64, -6,15)
    # experiment("experiment random_fill back 64 15.csv", "back", 64, -6,15)

    experiment("experiment random_fill back 64 15.csv", "back", 256, -6, 10, 974269)