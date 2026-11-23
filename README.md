# Sensor Data Analysis Tool

A Python program that simulates sensor readings, analyses them with NumPy and
plots them with Matplotlib. It can also load readings from an existing CSV file
instead of generating new ones.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python sensor_monitor.py
```

The program first asks what you want to do:

1. **Generate new sensor readings** – you enter the sensor type, the number of
   readings, the minimum and maximum sensor value and the alert threshold.
   The readings are generated with the `random` module and saved to
   `sensor_readings.csv`.
2. **Load readings from an existing CSV file** – you enter the file name, the
   sensor type and the alert threshold. No new readings are generated.

In both cases the program then:

- prints the number of readings, mean, minimum, maximum, standard deviation
  and how many readings are above the alert threshold,
- lists every reading that exceeds the threshold,
- shows a line plot (with the threshold as a horizontal line) and a histogram,
  and saves them as `readings_plot.png` and `readings_histogram.png`.

S

## Notes

- The readings are reproducible: `random.seed(42)` is called before generating,
  so the same inputs always give the same readings.
- The standard deviation is the population standard deviation (NumPy's
  default, `ddof=0`).
- Invalid input (text instead of a number, zero or negative number of
  readings, minimum greater than or equal to maximum, a missing or broken CSV
  file, a CSV file that cannot be saved) produces an error message and the
  program asks again or continues, instead of crashing.