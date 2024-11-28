import pywhatkit as kit
import subprocess
import re
import os
import sys

# Read the environment variable and add it to the country code
country_code = '+20'
phone_number = country_code+os.getenv("VALUE_TO_PASS")
location = ()  # location tuple
location_url = ""

def generate_google_maps_link(lat, lng):
    base_url = "https://www.google.com/maps?q="
    return f"{base_url}{lat},{lng}"

def send_link_via_whatsapp(location):
    global location_url
    try:
        kit.sendwhatmsg_instantly(phone_number, location_url)
    except:
        pass

def get_gps_location():
    global location
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
                location = (latitude, longitude)
        else:
            print("No location found")

    except subprocess.CalledProcessError as e:
        print(f"Error executing adb command: {e}")


if __name__ == "__main__":

    try:
        get_gps_location()
        location_url = generate_google_maps_link(location[0], location[1])
        send_link_via_whatsapp(location_url)
        sys.exit(0)
    except:
        pass
