"""Example client for PyTado"""

from PyTado.interface.interface import Tado

import pandas as pd
from datetime import datetime



# Create or append to DataFrame
def log_temperature(temp, asked_temp, file='output_data/temperature_log.csv'):
    now = datetime.now()
    df = pd.DataFrame([[now, temp, asked_temp]], columns=['timestamp', 'temperature', 'temperatureAsked'])

    # Append to CSV
    df.to_csv(file, mode='a', header=not pd.io.common.file_exists(file), index=False)


def set_temperature(tado, zone_id, file="input_data/temp_schema.csv"):
    df = pd.read_csv(file, delimiter=';')  
    
    print(df)
    current_hour = datetime.now().hour
    
    current_hour = 24 if current_hour == 0 else current_hour  # convert 0 to 24 if needed

    temp_row = df[df['Hour'] == current_hour]

    if not temp_row.empty:
        temperature = temp_row.iloc[0]['Temperature']

        # Set to 15°C indefinitely (manual mode)
        tado.set_zone_overlay(
            zone=zone_id,
            overlay_mode="MANUAL",
            set_temp=float(temperature),  # Celsius
            duration=None,  # No time limit
            device_type="HEATING"
        )

        print(f"Temperature for hour {current_hour} is set to: {temperature}°C")
    else:
        print(f"No temperature data for hour {current_hour}")

    return temperature

def main() -> None:
    """Retrieve all zones, once successfully logged in"""
    tado = Tado()

    print("Device activation status: ", tado.device_activation_status())
    print("Device verification URL: ", tado.device_verification_url())

    print("Starting device activation")
    tado.device_activation()

    print("Device activation status: ", tado.device_activation_status())

    zones = tado.get_zones()

    heating_zone = next(zone for zone in zones if zone["type"] == "HEATING")
    zone_id = heating_zone["id"]# Get current zone state and extract temperature
    state  = tado.get_state(zone_id)
    current_temp = state["sensorDataPoints"]["insideTemperature"]["celsius"]
    print(f"Current zone temperature: {current_temp}°C")

    asked_temperature = set_temperature(tado, zone_id)

    log_temperature(current_temp, asked_temperature)

if __name__ == "__main__":
    main()
