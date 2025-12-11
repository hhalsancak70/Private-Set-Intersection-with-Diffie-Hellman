import csv
import matplotlib.pyplot as plt

def read_results(csv_path="results.csv"):
    sizes = []
    overlaps = []
    times = []

    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        next(reader)  # header'ı atla
        for row in reader:
            n = int(row[0])
            o = int(row[1])
            t = float(row[2])
            sizes.append(n)
            overlaps.append(o)
            times.append(t)

    return sizes, overlaps, times


def plot_runtime(sizes, times):
    plt.figure()
    plt.plot(sizes, times, marker="o")
    plt.xlabel("Set size |S_A| = |S_B|")
    plt.ylabel("Average runtime (seconds)")
    plt.title("DH-based PSI runtime vs set size")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("runtime_plot.png", dpi=300)  # rapora koymak için
    plt.show()


def main():
    sizes, overlaps, times = read_results("results.csv")
    print("Loaded data:")
    for n, t in zip(sizes, times):
        print(f"  n = {n:6d}, avg runtime = {t:.6f} s")

    plot_runtime(sizes, times)


if __name__ == "__main__":
    main()
