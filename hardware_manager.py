import Adafruit_DHT
import time
from threading import Thread
import board
import busio
from adafruit_pn532.i2c import PN532_I2C
from adafruit_pn532 import exceptions

last_scanned_uid = None

DHT_TYPE = Adafruit_DHT.DHT22
DHT_PIN = 4 

try:
    I2C_BUS = busio.I2C(board.SCL, board.SDA)
    PN532 = PN532_I2C(I2C_BUS, debug=False)
    PN532.SAM_configuration()
    print("NFC PN532 initialized successfully.")
except Exception as e:
    print(f"Error initializing PN532: {e}. NFC functions will be disabled.")
    PN532 = None

def get_current_environment():
    humidity, temperature_c = Adafruit_DHT.read_retry(DHT_TYPE, DHT_PIN)
    if humidity is not None and temperature_c is not None:
        return {
            "temperature_c": round(temperature_c, 1),
            "humidity": round(humidity, 1)
        }
    else:
        return None

def get_music_recommendation_genre(temp):
    if temp >= 25:
        return "Tropical House"
    elif temp >= 20:
        return "Upbeat Pop / Summer Hits"
    elif temp >= 15:
        return "Indie Rock / Electronic"
    else:
        return "Ambient / Classical / Lo-Fi"

def nfc_listen_thread():
    global last_scanned_uid
    if not PN532:
        print("NFC Listener Thread failed to start: PN532 not initialized.")
        return
        
    print("NFC Listener Thread started.")
    
    while True:
        try:
            uid = PN532.read_passive_target(timeout=0.5)
            
            if uid is not None:
                card_id = "".join([hex(i).replace("0x", "").upper().zfill(2) for i in uid])
                last_scanned_uid = card_id
                print(f"NFC Scan: UID {card_id} detected.")
                
            time.sleep(1.5)
            
        except exceptions.NFCCommunicationError as e:
            print(f"NFC Thread Warning (Transient Error): {e}") 
            time.sleep(0.5)
            continue
            
        except Exception as e:
            print(f"NFC Thread CRITICAL ERROR: {e}")
            time.sleep(5)

def get_last_scanned_uid():
    global last_scanned_uid
    uid_to_return = last_scanned_uid
    last_scanned_uid = None
    return uid_to_return

nfc_thread = Thread(target=nfc_listen_thread, daemon=True)
nfc_thread.start()