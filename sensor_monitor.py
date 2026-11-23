"""Sensor Data Analysis Tool.

Simulates sensor readings (or loads them from a CSV file), analyses them
with NumPy and visualises them with Matplotlib.
"""

import csv
import random

import matplotlib.pyplot as plt
import numpy as np

SEED = 42
CSV_FILE = "sensor_readings.csv"
LINE_PLOT_FILE = "readings_plot.png"
HISTOGRAM_FILE = "readings_histogram.png"


# ---------------------------------------------------------------- input ----

def ask_text(prompt):
    """Ask until the user types something that is not empty."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("  Error: this field cannot be empty.")


def ask_float(prompt):
    """Ask until the user types a valid number."""
    while True:
        text = input(prompt).strip()
        try:
            return float(text)
        except ValueError:
            print(f"  Error: '{text}' is not a number. Please try again.")


def ask_positive_int(prompt):
    """Ask until the user types a whole number greater than zero."""
    while True:
        text = input(prompt).strip()
        try:
            value = int(text)
        except ValueError:
            print(f"  Error: '{text}' is not a whole number. Please try again.")
            continue
        if value <= 0:
            print("  Error: the number of readings must be greater than zero.")
            continue
        return value


def get_menu_choice():
    """Let the user choose between generating new data and loading a file."""
    print("What would you like to do?")
    print("  1 - Generate new sensor readings")
    print("  2 - Load readings from an existing CSV file")
    while True:
        choice = input("Enter 1 or 2: ").strip()
        if choice in ("1", "2"):
            return choice
        print("  Error: please enter 1 or 2.")


def get_user_input():
    """Ask for all the settings needed to generate new readings."""
    sensor_type = ask_text("Sensor type (e.g. temperature, light): ")
    count = ask_positive_int("Number of readings to generate: ")

    while True:
        minimum = ask_float("Minimum sensor value: ")
        maximum = ask_float("Maximum sensor value: ")
        if minimum < maximum:
            break
        print("  Error: the minimum must be smaller than the maximum.")

    threshold = ask_float("Alert threshold: ")
    if threshold < minimum or threshold > maximum:
        print("  Note: the threshold is outside the sensor range.")

    return sensor_type, count, minimum, maximum, threshold


# ----------------------------------------------------------------- data ----

def generate_readings(count, minimum, maximum, seed=SEED):
    """Return a NumPy array of `count` random readings in [minimum, maximum].

    random.seed() makes the same inputs always give the same readings.
    """
    random.seed(seed)
    readings = []
    for _ in range(count):
        readings.append(round(random.uniform(minimum, maximum), 2))
    return np.array(readings)


def save_readings(readings, filename=CSV_FILE):
    """Save readings to a CSV file. Return True if it worked."""
    try:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["sample", "reading"])
            for sample, reading in enumerate(readings, start=1):
                writer.writerow([sample, reading])
    except OSError as error:
        print(f"  Error: could not save '{filename}': {error}")
        return False
    print(f"Readings saved to {filename}")
    return True


def load_readings(filename):
    """Load readings from a CSV file. Return a NumPy array, or None on error."""
    readings = []
    try:
        with open(filename, newline="") as file:
            reader = csv.DictReader(file)
            for line_number, row in enumerate(reader, start=2):
                try:
                    readings.append(float(row["reading"]))
                except (KeyError, TypeError, ValueError):
                    print(f"  Error: line {line_number} of '{filename}' "
                          "has no valid 'reading' value.")
                    return None
    except FileNotFoundError:
        print(f"  Error: the file '{filename}' was not found.")
        return None
    except OSError as error:
        print(f"  Error: could not read '{filename}': {error}")
        return None

    if not readings:
        print(f"  Error: '{filename}' contains no readings.")
        return None
    return np.array(readings)


# ------------------------------------------------------------- analysis ----

def find_outliers(readings, threshold):
    """Return (sample numbers, values) of the readings above the threshold."""
    readings = np.array(readings)
    positions = np.where(readings > threshold)[0]
    return positions + 1, readings[positions]


def calculate_statistics(readings, threshold):
    """Return a dictionary with the main statistics of the readings."""
    readings = np.array(readings)
    return {
        "count": readings.size,
        "mean": np.mean(readings),
        "minimum": np.min(readings),
        "maximum": np.max(readings),
        "std": np.std(readings),
        "above_threshold": int(np.sum(readings > threshold)),
    }


def display_results(sensor_type, stats, threshold, samples, values):
    """Print the statistics and the readings above the threshold."""
    print()
    print(f"--- {sensor_type.capitalize()} sensor analysis ---")
    print(f"Number of readings:        {stats['count']}")
    print(f"Mean:                      {stats['mean']:.2f}")
    print(f"Minimum:                   {stats['minimum']:.2f}")
    print(f"Maximum:                   {stats['maximum']:.2f}")
    print(f"Standard deviation:        {stats['std']:.2f}")
    print(f"Readings above {threshold:g}:".ljust(27) + str(stats["above_threshold"]))

    print()
    if len(values) == 0:
        print("No readings exceed the alert threshold.")
    else:
        print("Readings exceeding the alert threshold:")
        for sample, value in zip(samples, values):
            print(f"  Sample {sample}: {value:.2f}")
    print()


# ---------------------------------------------------------------- plots ----

def plot_readings(readings, threshold, sensor_type, filename=LINE_PLOT_FILE):
    """Line plot of readings against sample number, with the threshold line."""
    samples = np.arange(1, len(readings) + 1)

    plt.figure(figsize=(10, 5))
    plt.plot(samples, readings, marker="o", markersize=3, label="Readings")
    plt.axhline(threshold, color="red", linestyle="--",
                label=f"Alert threshold ({threshold:g})")
    plt.title(f"{sensor_type.capitalize()} sensor readings")
    plt.xlabel("Sample number")
    plt.ylabel(f"{sensor_type.capitalize()} reading")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    save_figure(filename)


def plot_histogram(readings, sensor_type, filename=HISTOGRAM_FILE):
    """Histogram showing the distribution of the readings."""
    plt.figure(figsize=(8, 5))
    plt.hist(readings, bins=10, edgecolor="black")
    plt.title(f"Distribution of {sensor_type} readings")
    plt.xlabel(f"{sensor_type.capitalize()} reading")
    plt.ylabel("Number of readings")
    plt.grid(True)
    plt.tight_layout()
    save_figure(filename)


def save_figure(filename):
    """Save the current figure as an image file."""
    try:
        plt.savefig(filename)
        print(f"Graph saved to {filename}")
    except OSError as error:
        print(f"  Error: could not save '{filename}': {error}")


# ----------------------------------------------------------------- main ----

def main():
    print("=== Sensor Data Analysis Tool ===")
    choice = get_menu_choice()

    if choice == "1":
        sensor_type, count, minimum, maximum, threshold = get_user_input()
        readings = generate_readings(count, minimum, maximum)
        save_readings(readings)
    else:
        readings = None
        while readings is None:
            filename = ask_text(f"CSV file to load (e.g. {CSV_FILE}): ")
            readings = load_readings(filename)
        print(f"Loaded {len(readings)} readings from {filename}")
        sensor_type = ask_text("Sensor type (e.g. temperature, light): ")
        threshold = ask_float("Alert threshold: ")

    stats = calculate_statistics(readings, threshold)
    samples, values = find_outliers(readings, threshold)
    display_results(sensor_type, stats, threshold, samples, values)

    plot_readings(readings, threshold, sensor_type)
    plot_histogram(readings, sensor_type)
    plt.show()


if __name__ == "__main__":
    main()
