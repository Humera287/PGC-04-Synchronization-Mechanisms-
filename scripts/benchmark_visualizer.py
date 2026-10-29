import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Create results folder
os.makedirs("results", exist_ok=True)

# Thread counts
threads = [1, 2, 4, 8]

# Execution time data
data = {
    "None": [0.0062, 0.0065, 0.0075, 0.0085],
    "Critical": [0.0899, 0.3084, 0.6648, 1.0195],
    "Atomic": [0.0532, 0.1268, 0.1226, 0.1184],
    "Lock": [0.0894, 0.3643, 0.5535, 0.9216]
}

# Final counter values
counter = {
    "None": [10000000, 10000000, 7545062, 4394535],
    "Critical": [10000000, 10000000, 10000000, 10000000],
    "Atomic": [10000000, 10000000, 10000000, 10000000],
    "Lock": [10000000, 10000000, 10000000, 10000000]
}

# Light pastel colours
colors = {
    "None": "#B7DDE8",
    "Critical": "#F7C9D4",
    "Atomic": "#CDEAC0",
    "Lock": "#D8CCF1"
}

methods = ["None", "Critical", "Atomic", "Lock"]

x = np.arange(len(threads))
width = 0.19

# ------------------------------------------------
# Save benchmark data as CSV
# ------------------------------------------------

rows = []

for i, t in enumerate(threads):
    for method in methods:
        final_count = counter[method][i]

        rows.append({
            "Threads": t,
            "Mechanism": method,
            "Execution_Time": data[method][i],
            "Final_Counter": final_count,
            "Correctness_Percentage": final_count / 10000000 * 100
        })

df = pd.DataFrame(rows)
df.to_csv("results/synchronization_benchmarks.csv", index=False)

print("Benchmark CSV generated successfully!")

# ------------------------------------------------
# GRAPH 1: Execution Time Comparison
# ------------------------------------------------

plt.figure(figsize=(10, 6))

for i, method in enumerate(methods):
    plt.bar(
        x + (i - 1.5) * width,
        data[method],
        width,
        label=method,
        color=colors[method],
        edgecolor="gray"
    )

plt.title("Execution Time vs Number of Threads")
plt.xlabel("Number of Threads")
plt.ylabel("Execution Time (seconds)")
plt.xticks(x, threads)
plt.legend(title="Synchronization Method")
plt.grid(axis="y", linestyle="--", alpha=0.3)

plt.tight_layout()
plt.savefig("results/execution_time_comparison.png", dpi=200)
plt.close()

# ------------------------------------------------
# GRAPH 2: Final Counter Comparison
# ------------------------------------------------

plt.figure(figsize=(10, 6))

for i, method in enumerate(methods):
    values = [v / 1000000 for v in counter[method]]

    plt.bar(
        x + (i - 1.5) * width,
        values,
        width,
        label=method,
        color=colors[method],
        edgecolor="gray"
    )

plt.axhline(
    y=10,
    color="gray",
    linestyle="--",
    label="Expected Counter (10 million)"
)

plt.title("Final Counter Value vs Number of Threads")
plt.xlabel("Number of Threads")
plt.ylabel("Final Counter Value (Millions)")
plt.xticks(x, threads)
plt.legend(title="Synchronization Method")
plt.grid(axis="y", linestyle="--", alpha=0.3)

plt.tight_layout()
plt.savefig("results/final_counter_comparison.png", dpi=200)
plt.close()

# ------------------------------------------------
# GRAPH 3: Counter Correctness Percentage
# ------------------------------------------------

plt.figure(figsize=(10, 6))

for i, method in enumerate(methods):
    values = [
        v / 10000000 * 100
        for v in counter[method]
    ]

    plt.bar(
        x + (i - 1.5) * width,
        values,
        width,
        label=method,
        color=colors[method],
        edgecolor="gray"
    )

plt.title("Counter Correctness vs Number of Threads")
plt.xlabel("Number of Threads")
plt.ylabel("Correctness Percentage (%)")
plt.xticks(x, threads)
plt.ylim(0, 110)
plt.legend(title="Synchronization Method")
plt.grid(axis="y", linestyle="--", alpha=0.3)

plt.tight_layout()
plt.savefig("results/counter_correctness.png", dpi=200)
plt.close()

# ------------------------------------------------
# GRAPH 4: Execution Time of Synchronized Methods
# ------------------------------------------------

sync_methods = ["Critical", "Atomic", "Lock"]

plt.figure(figsize=(10, 6))

for i, method in enumerate(sync_methods):
    plt.bar(
        x + (i - 1) * 0.24,
        data[method],
        0.24,
        label=method,
        color=colors[method],
        edgecolor="gray"
    )

plt.title("Execution Time of Synchronization Methods")
plt.xlabel("Number of Threads")
plt.ylabel("Execution Time (seconds)")
plt.xticks(x, threads)
plt.legend(title="Synchronization Method")
plt.grid(axis="y", linestyle="--", alpha=0.3)

plt.tight_layout()
plt.savefig("results/synchronization_methods_time.png", dpi=200)
plt.close()

# ------------------------------------------------
# Completion
# ------------------------------------------------

print("\nAll 4 graphs generated successfully!")

print("\nFiles saved inside results folder:")
print("1. execution_time_comparison.png")
print("2. final_counter_comparison.png")
print("3. counter_correctness.png")
print("4. synchronization_methods_time.png")
print("5. synchronization_benchmarks.csv")
