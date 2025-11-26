import time
import board
import adafruit_dht

dht_device = adafruit_dht.DHT22(board.D4)

print("Reading sensor... (Press Ctrl+C to stop)")

while True:
    try:
        temperature_c = dht_device.temperature
        humidity = dht_device.humidity

        if humidity is not None and temperature_c is not None:
            print(f"Temp: {temperature_c:.1f}C  |  Humidity: {humidity:.1f}%")
        else:
            print("Reading failed, retrying...")

    except RuntimeError as error:
        print(f"Sensor error: {error.args[0]}")
        time.sleep(2.0)
        continue
    except Exception as error:
        dht_device.exit()
        raise error
    except KeyboardInterrupt:
        print("\nExiting.")
        break

    time.sleep(2.0)