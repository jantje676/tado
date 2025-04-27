"""Example client for PyTado"""

from PyTado.interface.interface import Tado


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


    # Set to 15°C indefinitely (manual mode)
    tado.set_zone_overlay(
        zone=zone_id,
        overlay_mode="MANUAL",
        set_temp=15,  # Celsius
        duration=None,  # No time limit
        device_type="HEATING"
    )
if __name__ == "__main__":
    main()
