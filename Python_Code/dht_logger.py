
import serial
import csv
import time
from datetime import datetime
from pathlib import Path

# ESP8266 serial settings
PORT = "COM5"
BAUD_RATE = 115200

# Find the main project folder
project_folder = Path(__file__).resolve().parent.parent

# Dataset folder location
dataset_folder = project_folder / "Dataset"
dataset_folder.mkdir(exist_ok=True)

# CSV file location
filename = dataset_folder / "food_freshness_data.csv"

print("======================================")
print("   FOOD FRESHNESS MONITORING SYSTEM")
print("======================================")

print("Connecting to ESP8266...")

esp = None

try:
    esp = serial.Serial(PORT, BAUD_RATE, timeout=2)

    # Allow ESP8266 to restart
    time.sleep(2)

    # Clear startup messages from serial buffer
    esp.reset_input_buffer()

    print("Connected successfully!")
    print("Collecting temperature and humidity data...")
    print("Saving data in Dataset folder.")
    print("Press Ctrl + C to stop.\n")

    with open(filename, "a", newline="") as file:

        writer = csv.writer(file)

        # Add headings only if the file is empty
        if file.tell() == 0:
            writer.writerow([
                "Timestamp",
                "Temperature_C",
                "Humidity_Percent"
            ])

        while True:

            line = esp.readline().decode(
                "utf-8",
                errors="ignore"
            ).strip()

            if "," in line:

                try:
                    temperature, humidity = map(
                        float,
                        line.split(",")
                    )

                    timestamp = datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )

                    writer.writerow([
                        timestamp,
                        temperature,
                        humidity
                    ])

                    # Save every reading immediately
                    file.flush()

                    print(
                        f"{timestamp} | "
                        f"Temperature: {temperature} C | "
                        f"Humidity: {humidity} %"
                    )

                except ValueError:
                    print("Invalid data received:", line)

except serial.SerialException as error:
    print("Serial connection error:", error)

except KeyboardInterrupt:
    print("\nData collection stopped by user.")

finally:

    if esp is not None and esp.is_open:
        esp.close()
        print("ESP8266 connection closed.")

    print("Data collection program finished.")
