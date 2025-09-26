import subprocess
import time
import csv
import argparse

def sweep(n,q,hamming,step,filename):
    print("Sweeping...")
    secret_fill = "random_fill"
    secret_position = "front"
    algo = "LLL"

    anchor_bit_values = []
    stddevs = []
    runtimes = []

    highest_anchor_position = -1



    #open(filename, 'a', newline='')

    for anchor_position in range(hamming+10, n, step):
        print("Sweeping with anchor position at: " + str(anchor_position))
        i = 0
        succeeded_once = False
        while i < 5 and not succeeded_once:
            start_time = time.perf_counter()
            print("Round " + str(i) + " of 5.")
            #start_time = time.perf_counter()
            cmd = [
                "python3", "src/usvp/usvp.py",
                "--secret_type", "binary",
                "--N", str(n),
                "--Q", str(q),
                "--algo", algo,
                "--algo2", algo,
                "--hamming", str(hamming),
                "--num_workers", "1",
                "--secret_specs", f"{secret_fill} {secret_position} {anchor_position}",
            ]

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            result = []

            for line in process.stdout:
                print(line, end="")
                result.append(line)

            result = "".join(result)


            current_secret = "null"
            stddev = -1
            for line in result.splitlines():
                if "STDDEV:" in line:
                    stddev = line.split("STDDEV:")[1].strip()
                    break
                if "Secret made: " in line:
                    current_secret = line.split("Secret made: ")[1].strip()

            if "No reduction improvement" in result.split('\n')[-2]:
                # with open('failed_secrets.csv', 'a', newline='') as csvfile:
                #     csv_writer = csv.writer(csvfile)
                #     csv_writer.writerow([current_secret, anchor_position])
                print("Experiment failed. Retrying...")
                i = i + 1
                continue

            runtime = time.perf_counter()  - start_time
            print("Final stddev: ", stddev, "\nSecret spread: ",anchor_position, "\nSecret: ", current_secret)

            with open(filename+"_all.csv", 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["random", runtime, stddev, anchor_position, hamming, current_secret])


            #anchor_bit_values.append(anchor_position)
            #stddevs.append(round(float(stddev),5))
            #runtimes.append(runtime)

            succeeded_once = True

            # with open(filename, 'a', newline='') as csvfile:
            #     csv_writer = csv.writer(csvfile)
            #     csv_writer.writerow([current_secret,anchor_position,stddev,runtime])
            #
            # i = i + 1

        if i == 5 and not succeeded_once:
            return anchor_position
    return n


def test_once(n,q,hamming,secret_specs):
    cmd = [
        "python3", "src/usvp/usvp.py",
        "--secret_type", "binary",
        "--N", str(n),
        "--Q", str(q),
        "--algo", "LLL",
        "--algo2", "LLL",
        "--hamming", str(hamming),
        "--num_workers", "1",
        "--secret_specs", secret_specs,
        "--float_type", "qd"
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    result = []

    for line in process.stdout:
        print(line, end="")
        result.append(line)

    result = "".join(result)

    print("Hamming = " + str(hamming))
    if "No reduction improvement" in result.split('\n')[-2]:
        print("Reduction of fully " + secret_specs + "-loaded secret failed.")
        return False

    print("Reduction of fully " + secret_specs + "-loaded secret succeeded.")
    return True


def experiment(filename,n,q,hamming_min,hamming_max,anchor_step):
    failure_started = False

    num_h_test = 0

    for current_hamming in range(hamming_min, hamming_max, 1):
        print("Testing hamming weight: " + str(current_hamming))
        if not failure_started:
            front = test_once(n, q, current_hamming,"front")
            back = test_once(n, q, current_hamming, "back")
            if front and not back:
                print("Failure started: Front secret reduced, back secret did not.")
                failure_started = True

        if failure_started:
            num_h_test = num_h_test + 1
            max_anchor_position = sweep(n,q,current_hamming,anchor_step,filename)
            print("Finished sweep. For hamming weight " +str(current_hamming) +", max_anchor_position = " + str(max_anchor_position))
            with open(filename+".csv", 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([current_hamming, max_anchor_position])


# if __name__ == "__main__":
#     experiment("test_file.csv",128,3329,10,30,10)
#     #experiment("test file",256,974269,10,30,10)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str)
    parser.add_argument("n", type=int)
    parser.add_argument("q", type=int)
    parser.add_argument("hamming_min", type=int)
    parser.add_argument("hamming_max", type=int)
    parser.add_argument("anchor_step", type=int)

    args = parser.parse_args()
    experiment(args.file, args.n, args.q, args.hamming_min, args.hamming_max, args.anchor_step)