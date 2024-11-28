import subprocess
import time
import re

def get_gps_location():
    try:
        # using Android Debug Bridge (ADB)
        # adb shell dumpsys location  findstr gps Lo"
        result = subprocess.run(["adb", "shell", "dumpsys", "location"], capture_output=True, text=True)
        output = result.stdout

        # Regex to match lines with last location
        location_pattern = re.compile(r"last location=Location\[(\w+) (\d+\.\d+),(\d+\.\d+)")
        matches = location_pattern.findall(output)

        if matches:
            for match in matches:
                provider, latitude, longitude = match
                print(f"Provider: {provider}, Latitude: {latitude}, Longitude: {longitude}")
        else:
            print("No location found")

    except subprocess.CalledProcessError as e:
        print(f"Error executing adb command: {e}")

if __name__ == "__main__":
    while True:
        get_gps_location()
        time.sleep(1)
